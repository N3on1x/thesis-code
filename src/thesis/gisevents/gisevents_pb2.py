# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gisevents/gisevents.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19gisevents/gisevents.proto\x12\tgisevents\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc9\x02\n\rCreationEvent\x12\x0e\n\x02id\x18\x01 \x01(\x03R\x02id\x12\x38\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ttimestamp\x12\x18\n\x07version\x18\x03 \x01(\x05R\x07version\x12(\n\x05point\x18\x04 \x01(\x0b\x32\x10.gisevents.PointH\x00R\x05point\x12\x37\n\nlinestring\x18\x05 \x01(\x0b\x32\x15.gisevents.LineStringH\x00R\nlinestring\x12.\n\x07polygon\x18\x06 \x01(\x0b\x32\x12.gisevents.PolygonH\x00R\x07polygon\x12\x35\n\nproperties\x18\x07 \x01(\x0b\x32\x15.gisevents.PropertiesR\npropertiesB\n\n\x08geometry\"4\n\nProperties\x12\x10\n\x03key\x18\x01 \x03(\tR\x03key\x12\x14\n\x05value\x18\x02 \x03(\tR\x05value\"\xb3\x02\n\x11ModificationEvent\x12\x0e\n\x02id\x18\x01 \x01(\x03R\x02id\x12\x38\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ttimestamp\x12\x18\n\x07version\x18\x03 \x01(\x05R\x07version\x12\x33\n\x0bpoint_patch\x18\x04 \x01(\x0b\x32\x10.gisevents.PointH\x00R\npointPatch\x12G\n\x10linestring_patch\x18\x05 \x01(\x0b\x32\x1a.gisevents.LineStringPatchH\x00R\x0flinestringPatch\x12\x33\n\nprop_patch\x18\x06 \x01(\x0b\x32\x14.gisevents.PropPatchR\tpropPatchB\x07\n\x05patch\"s\n\rDeletionEvent\x12\x0e\n\x02id\x18\x01 \x01(\x03R\x02id\x12\x38\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ttimestamp\x12\x18\n\x07version\x18\x03 \x01(\x05R\x07version\"+\n\x05Point\x12\x10\n\x03lon\x18\x02 \x01(\x11R\x03lon\x12\x10\n\x03lat\x18\x01 \x01(\x11R\x03lat\"0\n\nLineString\x12\x10\n\x03lat\x18\x01 \x03(\x11R\x03lat\x12\x10\n\x03lon\x18\x02 \x03(\x11R\x03lon\"-\n\x07Polygon\x12\x10\n\x03lat\x18\x01 \x03(\x11R\x03lat\x12\x10\n\x03lon\x18\x02 \x03(\x11R\x03lon\"\xbe\x01\n\x0fLineStringPatch\x12\x14\n\x05index\x18\x01 \x03(\x05R\x05index\x12<\n\x07\x63ommand\x18\x02 \x03(\x0e\x32\".gisevents.LineStringPatch.CommandR\x07\x63ommand\x12(\n\x06vector\x18\x03 \x03(\x0b\x32\x10.gisevents.PointR\x06vector\"-\n\x07\x43ommand\x12\n\n\x06INSERT\x10\x00\x12\n\n\x06\x44\x45LETE\x10\x01\x12\n\n\x06\x43HANGE\x10\x02\"\xaa\x01\n\tPropPatch\x12\x36\n\x0bprop_delete\x18\x01 \x01(\x0b\x32\x15.gisevents.PropDeleteR\npropDelete\x12-\n\x08prop_add\x18\x02 \x01(\x0b\x32\x12.gisevents.PropAddR\x07propAdd\x12\x36\n\x0bprop_update\x18\x03 \x01(\x0b\x32\x15.gisevents.PropUpdateR\npropUpdate\"%\n\nPropDelete\x12\x17\n\x07key_idx\x18\x01 \x03(\rR\x06keyIdx\"1\n\x07PropAdd\x12\x10\n\x03key\x18\x01 \x03(\tR\x03key\x12\x14\n\x05value\x18\x02 \x03(\tR\x05value\";\n\nPropUpdate\x12\x17\n\x07key_idx\x18\x01 \x03(\rR\x06keyIdx\x12\x14\n\x05value\x18\x02 \x03(\tR\x05valueBc\n\rcom.giseventsB\x0eGiseventsProtoP\x01\xa2\x02\x03GXX\xaa\x02\tGisevents\xca\x02\tGisevents\xe2\x02\x15Gisevents\\GPBMetadata\xea\x02\tGiseventsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gisevents.gisevents_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\rcom.giseventsB\016GiseventsProtoP\001\242\002\003GXX\252\002\tGisevents\312\002\tGisevents\342\002\025Gisevents\\GPBMetadata\352\002\tGisevents'
  _globals['_CREATIONEVENT']._serialized_start=74
  _globals['_CREATIONEVENT']._serialized_end=403
  _globals['_PROPERTIES']._serialized_start=405
  _globals['_PROPERTIES']._serialized_end=457
  _globals['_MODIFICATIONEVENT']._serialized_start=460
  _globals['_MODIFICATIONEVENT']._serialized_end=767
  _globals['_DELETIONEVENT']._serialized_start=769
  _globals['_DELETIONEVENT']._serialized_end=884
  _globals['_POINT']._serialized_start=886
  _globals['_POINT']._serialized_end=929
  _globals['_LINESTRING']._serialized_start=931
  _globals['_LINESTRING']._serialized_end=979
  _globals['_POLYGON']._serialized_start=981
  _globals['_POLYGON']._serialized_end=1026
  _globals['_LINESTRINGPATCH']._serialized_start=1029
  _globals['_LINESTRINGPATCH']._serialized_end=1219
  _globals['_LINESTRINGPATCH_COMMAND']._serialized_start=1174
  _globals['_LINESTRINGPATCH_COMMAND']._serialized_end=1219
  _globals['_PROPPATCH']._serialized_start=1222
  _globals['_PROPPATCH']._serialized_end=1392
  _globals['_PROPDELETE']._serialized_start=1394
  _globals['_PROPDELETE']._serialized_end=1431
  _globals['_PROPADD']._serialized_start=1433
  _globals['_PROPADD']._serialized_end=1482
  _globals['_PROPUPDATE']._serialized_start=1484
  _globals['_PROPUPDATE']._serialized_end=1543
# @@protoc_insertion_point(module_scope)
