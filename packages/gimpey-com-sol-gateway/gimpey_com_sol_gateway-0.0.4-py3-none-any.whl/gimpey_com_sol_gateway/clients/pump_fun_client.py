import grpc
from ..generated.pumpfun_pb2 import (
    BuyRequest,
    SellRequest,
    CreateTokenRequest,
    SendRequest
)
from ..generated.pumpfun_pb2_grpc import PumpFunStub


class PumpFunClient:
    def __init__(self, address: str, api_key: str = None, secure: bool = True):
        """Initializes the gRPC client."""
        if secure:
            creds = grpc.ssl_channel_credentials()
            self.channel = grpc.secure_channel(address, creds)
        else:
            self.channel = grpc.insecure_channel(address)

        self.client = PumpFunStub(self.channel)
        self.api_key = api_key

    def _call_method(self, method, request):
        """A generic private helper function to call a gRPC method with an optional API key."""
        metadata = []
        if self.api_key:
            metadata.append(('x-api-key', self.api_key))

        try:
            response = method(request, metadata=metadata)
            return response
        except grpc.RpcError as e:
            raise Exception(f"gRPC error: {e.details()}") from e
    
    def buy(self, request: BuyRequest):
        """Sends a buy request to the PumpFun service."""
        return self._call_method(self.client.buy, request)

    def sell(self, request: SellRequest):
        """Sends a sell request to the PumpFun service."""
        return self._call_method(self.client.sell, request)

    def create_token(self, request: CreateTokenRequest):
        """Sends a create token request to the PumpFun service."""
        return self._call_method(self.client.createToken, request)

    def send(self, request: SendRequest):
        """Sends a send request to the PumpFun service."""
        return self._call_method(self.client.send, request)