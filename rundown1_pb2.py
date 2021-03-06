# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rundown1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import track_start_point_pb2 as track__start__point__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rundown1.proto',
  package='ghostpacer.run',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0erundown1.proto\x12\x0eghostpacer.run\x1a\x17track_start_point.proto\"\xe8\x01\n\rDownloadedRun\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08startLat\x18\x02 \x01(\x02\x12\x10\n\x08startLon\x18\x03 \x01(\x02\x12\x11\n\tmileSplit\x18\x04 \x01(\x02\x12\x38\n\x0ftrackStartPoint\x18\x05 \x01(\x0e\x32\x1f.ghostpacer.run.TrackStartPoint\x12\x14\n\x08pointLat\x18\x06 \x03(\x02\x42\x02\x10\x01\x12\x14\n\x08pointLon\x18\x07 \x03(\x02\x42\x02\x10\x01\x12\x15\n\tpointElev\x18\x08 \x03(\x02\x42\x02\x10\x01\x12\x15\n\tsavedTime\x18\t \x03(\x02\x42\x02\x10\x01\x62\x06proto3'
  ,
  dependencies=[track__start__point__pb2.DESCRIPTOR,])




_DOWNLOADEDRUN = _descriptor.Descriptor(
  name='DownloadedRun',
  full_name='ghostpacer.run.DownloadedRun',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ghostpacer.run.DownloadedRun.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='startLat', full_name='ghostpacer.run.DownloadedRun.startLat', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='startLon', full_name='ghostpacer.run.DownloadedRun.startLon', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mileSplit', full_name='ghostpacer.run.DownloadedRun.mileSplit', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trackStartPoint', full_name='ghostpacer.run.DownloadedRun.trackStartPoint', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pointLat', full_name='ghostpacer.run.DownloadedRun.pointLat', index=5,
      number=6, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pointLon', full_name='ghostpacer.run.DownloadedRun.pointLon', index=6,
      number=7, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pointElev', full_name='ghostpacer.run.DownloadedRun.pointElev', index=7,
      number=8, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='savedTime', full_name='ghostpacer.run.DownloadedRun.savedTime', index=8,
      number=9, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=60,
  serialized_end=292,
)

_DOWNLOADEDRUN.fields_by_name['trackStartPoint'].enum_type = track__start__point__pb2._TRACKSTARTPOINT
DESCRIPTOR.message_types_by_name['DownloadedRun'] = _DOWNLOADEDRUN
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DownloadedRun = _reflection.GeneratedProtocolMessageType('DownloadedRun', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADEDRUN,
  '__module__' : 'rundown1_pb2'
  # @@protoc_insertion_point(class_scope:ghostpacer.run.DownloadedRun)
  })
_sym_db.RegisterMessage(DownloadedRun)


_DOWNLOADEDRUN.fields_by_name['pointLat']._options = None
_DOWNLOADEDRUN.fields_by_name['pointLon']._options = None
_DOWNLOADEDRUN.fields_by_name['pointElev']._options = None
_DOWNLOADEDRUN.fields_by_name['savedTime']._options = None
# @@protoc_insertion_point(module_scope)
