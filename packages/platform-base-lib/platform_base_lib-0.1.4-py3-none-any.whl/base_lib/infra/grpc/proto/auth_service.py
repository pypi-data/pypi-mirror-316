import grpc
import time
import jwt  # Install with `pip install pyjwt`
from concurrent import futures
from auth_pb2 import TokenResponse
from auth_pb2_grpc import AuthServicer, add_AuthServicer_to_server

# Secret key for JWT token generation (replace with your secure secret)
SECRET_KEY = "your_jwt_secret_key"


class AuthService(AuthServicer):
    def GenerateToken(self, request, context):
        """
        Implements the GenerateToken RPC method.
        This generates a JWT token based on the incoming JWTTokenInfo request.
        """
        # Extract the required information from the request
        payload = {
            "userId": request.userId,
            "organizationId": request.organizationId,
            "externalUserId": request.externalUserId,
            "role": request.role,
            "authType": request.authType,
            "exp": (
                request.exp if request.exp > 0 else int(time.time()) + 3600
            ),  # Default expiration is 1 hour
            "iat": (
                request.iat if request.iat > 0 else int(time.time())
            ),  # Issued at time
        }

        # Generate JWT token
        try:
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            expires_in = payload["exp"] - payload["iat"]

            # Return the generated token and expiration metadata
            return TokenResponse(access_token=token, expires_in=expires_in)
        except Exception as e:
            # Handle token generation errors
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to generate token: " + str(e))
            return TokenResponse()


def serve():
    """
    Starts the gRPC server and binds the Auth service to the server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AuthServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    print("Auth Service is running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
