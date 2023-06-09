# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: setting.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='setting.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n\025sawtooth.sdk.protobufP\001Z\013setting_pb2',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rsetting.proto\"O\n\x07Setting\x12\x1f\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x0e.Setting.Entry\x1a#\n\x05\x45ntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tB&\n\x15sawtooth.sdk.protobufP\x01Z\x0bsetting_pb2b\x06proto3'
)




_SETTING_ENTRY = _descriptor.Descriptor(
  name='Entry',
  full_name='Setting.Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Setting.Entry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='Setting.Entry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=96,
)

_SETTING = _descriptor.Descriptor(
  name='Setting',
  full_name='Setting',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entries', full_name='Setting.entries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SETTING_ENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=96,
)

_SETTING_ENTRY.containing_type = _SETTING
_SETTING.fields_by_name['entries'].message_type = _SETTING_ENTRY
DESCRIPTOR.message_types_by_name['Setting'] = _SETTING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Setting = _reflection.GeneratedProtocolMessageType('Setting', (_message.Message,), {

  'Entry' : _reflection.GeneratedProtocolMessageType('Entry', (_message.Message,), {
    'DESCRIPTOR' : _SETTING_ENTRY,
    '__module__' : 'setting_pb2'
    # @@protoc_insertion_point(class_scope:Setting.Entry)
    })
  ,
  'DESCRIPTOR' : _SETTING,
  '__module__' : 'setting_pb2'
  # @@protoc_insertion_point(class_scope:Setting)
  })
_sym_db.RegisterMessage(Setting)
_sym_db.RegisterMessage(Setting.Entry)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
