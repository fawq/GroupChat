from client import Client
from server import Server
import typer

app = typer.Typer()


class GroupChat:
    ADDRESS: str = "localhost"
    PORT: int = 11912

    @staticmethod
    @app.command()
    def run_client(address=ADDRESS, port=PORT):
        client = Client(address, port)
        client.run()

    @staticmethod
    @app.command()
    def run_server(port=PORT):
        server = Server(port)
        server.run()
