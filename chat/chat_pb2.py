# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\x1a\x1fgoogle/protobuf/timestamp.proto\"\x07\n\x05\x45mpty\"T\n\x04Note\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12-\n\ttimestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2Z\n\nChatServer\x12\'\n\nChatStream\x12\x0b.chat.Empty\x1a\n.chat.Note0\x01\x12#\n\x08SendNote\x12\n.chat.Note\x1a\x0b.chat.Emptyb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=53
  _EMPTY._serialized_end=60
  _NOTE._serialized_start=62
  _NOTE._serialized_end=146
  _CHATSERVER._serialized_start=148
  _CHATSERVER._serialized_end=238
# @@protoc_insertion_point(module_scope)
