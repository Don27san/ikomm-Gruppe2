from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerAnnounce(_message.Message):
    __slots__ = ("serverId", "feature")
    class Feature(_message.Message):
        __slots__ = ("featureName", "port")
        FEATURENAME_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        featureName: str
        port: int
        def __init__(self, featureName: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    serverId: str
    feature: _containers.RepeatedCompositeFieldContainer[ServerAnnounce.Feature]
    def __init__(self, serverId: _Optional[str] = ..., feature: _Optional[_Iterable[_Union[ServerAnnounce.Feature, _Mapping]]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("userId", "serverId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    serverId: str
    def __init__(self, userId: _Optional[str] = ..., serverId: _Optional[str] = ...) -> None: ...

class ConnectClient(_message.Message):
    __slots__ = ("user", "portId")
    USER_FIELD_NUMBER: _ClassVar[int]
    PORTID_FIELD_NUMBER: _ClassVar[int]
    user: User
    portId: int
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., portId: _Optional[int] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("messageId", "timestamp", "author", "user", "text", "live_location")
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LIVE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    messageId: str
    timestamp: _timestamp_pb2.Timestamp
    author: User
    user: User
    text: str
    live_location: LiveLocation
    def __init__(self, messageId: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., author: _Optional[_Union[User, _Mapping]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., text: _Optional[str] = ..., live_location: _Optional[_Union[LiveLocation, _Mapping]] = ...) -> None: ...

class TypingEvent(_message.Message):
    __slots__ = ("user", "timestamp")
    USER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    user: User
    timestamp: float
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., timestamp: _Optional[float] = ...) -> None: ...

class TypingEvents(_message.Message):
    __slots__ = ("typing_events",)
    TYPING_EVENTS_FIELD_NUMBER: _ClassVar[int]
    typing_events: _containers.RepeatedCompositeFieldContainer[TypingEvent]
    def __init__(self, typing_events: _Optional[_Iterable[_Union[TypingEvent, _Mapping]]] = ...) -> None: ...

class LiveLocation(_message.Message):
    __slots__ = ("user", "timestamp", "expiry_at")
    class Location(_message.Message):
        __slots__ = ("latitude", "longitude")
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        latitude: float
        longitude: float
        def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
    USER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_AT_FIELD_NUMBER: _ClassVar[int]
    user: User
    timestamp: float
    expiry_at: float
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., timestamp: _Optional[float] = ..., expiry_at: _Optional[float] = ...) -> None: ...
