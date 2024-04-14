import typer

from client import Client
from server import Server

app = typer.Typer()


class GroupChat:
    ADDRESS: str = "localhost"
    PORT: int = 11912

    @staticmethod
    @app.command()
    def run_client(address=ADDRESS, port=PORT, ca_cert="certificate/client.pem"):
        client = Client(address, port)
        client.run(ca_cert)

    @staticmethod
    @app.command()
    def run_server(
        port=PORT, keyfile="certificate/server.key", certfile="certificate/server.pem"
    ):
        server = Server(port)
        server.run(keyfile, certfile)
