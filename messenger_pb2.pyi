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

class TypingEvent(_message.Message):
    __slots__ = ("userId", "timestamp")
    USERID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    userId: str
    timestamp: float
    def __init__(self, userId: _Optional[str] = ..., timestamp: _Optional[float] = ...) -> None: ...

class TypingEvents(_message.Message):
    __slots__ = ("typing_events",)
    TYPING_EVENTS_FIELD_NUMBER: _ClassVar[int]
    typing_events: _containers.RepeatedCompositeFieldContainer[TypingEvent]
    def __init__(self, typing_events: _Optional[_Iterable[_Union[TypingEvent, _Mapping]]] = ...) -> None: ...
