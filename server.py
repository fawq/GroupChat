import threading
from concurrent import futures

import grpc

import chat.chat_pb2 as chat
import chat.chat_pb2_grpc as chat_grpc


class Server(chat_grpc.ChatServerServicer):
    PORT = 11912

    def __init__(self, port = PORT):
        self.chats = []
        self._chats_lock = threading.Lock()
        self.port = port

    def ChatStream(self, request, context):
        last_index = 0
        while True:
            while len(self.chats) > last_index:
                message = self.chats[last_index]
                last_index += 1
                yield message

    def SendNote(self, request: chat.Note, context):
        with self._chats_lock:
            self.chats.append(request)
        return chat.Empty()

    def run(self):
        chat_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chat_grpc.add_ChatServerServicer_to_server(Server(), chat_server)
        print('Starting server. Listening...')
        keyfile = 'certificate/server.key'
        certfile = 'certificate/server.pem'
        private_key = open(keyfile, 'rb').read()
        certificate_chain = open(certfile, 'rb').read()
        credentials = grpc.ssl_server_credentials(
            [(private_key, certificate_chain)]
        )
        chat_server.add_secure_port(f"[::]:{self.port}", credentials)
        chat_server.start()
        chat_server.wait_for_termination()


if __name__ == '__main__':
    server = Server()
    server.run()
