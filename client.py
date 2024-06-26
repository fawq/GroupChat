import os.path
import threading
from datetime import datetime
from tkinter import END, Entry, Frame, Label, Text, Tk, simpledialog

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import chat.chat_pb2 as chat
import chat.chat_pb2_grpc as chat_grpc


class Client:
    ADDRESS: str = "localhost"
    PORT: int = 11912

    FRAME_WIDTH = 300
    FRAME_HEIGHT = 300

    def __init__(self, address: str = ADDRESS, port: int = PORT):
        self.username = ""
        self.frame = None

        self.address = address
        self.port = port
        self.conn = None

    def run(self, ca_cert="certificate/client.pem"):
        if os.path.exists(ca_cert):
            root_certs = open(ca_cert, "rb").read()
            credentials = grpc.ssl_channel_credentials(root_certs)
            channel = grpc.secure_channel(f"{self.address}:{self.port}", credentials)
            print("Secure client started")
        else:
            channel = grpc.insecure_channel(f"{self.address}:{self.port}")
            print("Insecure client started. Please pass ca_cert path")
        self.conn = chat_grpc.ChatServerStub(channel)

        self.__setup_ui()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        self.frame.mainloop()

    def listen_for_messages(self):
        for message in self.conn.ChatStream(chat.Empty()):
            timestamp = message.timestamp.seconds + message.timestamp.nanos / 1e9
            self.chat_list.insert(
                END,
                f"[{datetime.fromtimestamp(timestamp)} {message.name}] {message.message}\n",
            )

    def send_message(self, event):
        message_text = self.entry_message.get()
        self.entry_message.delete(0, END)
        if message_text != "":
            proto_timestamp = Timestamp()
            proto_timestamp.GetCurrentTime()
            self.conn.SendNote(
                chat.Note(
                    name=self.username, message=message_text, timestamp=proto_timestamp
                )
            )

    def __setup_ui(self):
        root = Tk()
        self.frame = Frame(root, width=Client.FRAME_WIDTH, height=Client.FRAME_HEIGHT)
        self.frame.pack()
        root.withdraw()
        self.username = simpledialog.askstring(
            "Username", "What's your username?", parent=root
        )
        root.deiconify()

        self.chat_list = Text()
        self.chat_list.pack()
        lbl_username = Label(self.frame, text=self.username)
        lbl_username.pack()
        self.entry_message = Entry(self.frame, width=50)
        self.entry_message.bind("<Return>", self.send_message)
        self.entry_message.focus()
        self.entry_message.pack()


if __name__ == "__main__":
    client = Client()
    client.run()
