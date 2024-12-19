import grpc
import auth_pb2
import auth_pb2_grpc


def run():
    # Create a channel to communicate with the gRPC server
    channel = grpc.insecure_channel(
        "localhost:50051"
    )  # Ensure the server is running on this port
    stub = auth_pb2_grpc.AuthStub(channel)

    # Login request example
    print("Attempting Login...")
    login_request = auth_pb2.JWTTokenInfo(userId=123)
    try:
        login_response = stub.GenerateToken(login_request)
        print(
            f"Login Response: Token: {login_response.token}, Message: {login_response.message}"
        )
    except grpc.RpcError as e:
        print(f"Login Failed: {e.details()} (Error Code: {e.code()})")


if __name__ == "__main__":
    import time

    while True:
        run()
        time.sleep(2)
