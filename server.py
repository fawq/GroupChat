import threading
from concurrent import futures

import grpc

import chat.chat_pb2 as chat
import chat.chat_pb2_grpc as chat_grpc


class ChatServer(chat_grpc.ChatServerServicer):
    def __init__(self):
        self.chats = []
        self._chats_lock = threading.Lock()

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


if __name__ == '__main__':
    port = 11912
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print('Starting server. Listening...')
    keyfile = 'certificate/server.key'
    certfile = 'certificate/server.pem'
    private_key = open(keyfile, 'rb').read()
    certificate_chain = open(certfile, 'rb').read()
    credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )
    server.add_secure_port(f"[::]:{port}", credentials)
    server.start()
    server.wait_for_termination()
