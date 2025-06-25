from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("userId", "serverId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    userId: str
    serverId: str
    def __init__(self, userId: _Optional[str] = ..., serverId: _Optional[str] = ...) -> None: ...

class DiscoverServer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

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

class ConnectClient(_message.Message):
    __slots__ = ("user", "typingPort", "location_port")
    USER_FIELD_NUMBER: _ClassVar[int]
    TYPINGPORT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_PORT_FIELD_NUMBER: _ClassVar[int]
    user: User
    typingPort: int
    location_port: int
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., typingPort: _Optional[int] = ..., location_port: _Optional[int] = ...) -> None: ...

class ConnectionResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_ERROR: _ClassVar[ConnectionResponse.Result]
        CONNECTED: _ClassVar[ConnectionResponse.Result]
        IS_ALREADY_CONNECTED_ERROR: _ClassVar[ConnectionResponse.Result]
    UNKNOWN_ERROR: ConnectionResponse.Result
    CONNECTED: ConnectionResponse.Result
    IS_ALREADY_CONNECTED_ERROR: ConnectionResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ConnectionResponse.Result
    def __init__(self, result: _Optional[_Union[ConnectionResponse.Result, str]] = ...) -> None: ...

class HangUp(_message.Message):
    __slots__ = ("reason",)
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_REASON: _ClassVar[HangUp.Reason]
        EXIT: _ClassVar[HangUp.Reason]
        TIMEOUT: _ClassVar[HangUp.Reason]
        PAYLOAD_LIMIT_EXCEEDED: _ClassVar[HangUp.Reason]
        MESSAGE_MALFORMED: _ClassVar[HangUp.Reason]
    UNKNOWN_REASON: HangUp.Reason
    EXIT: HangUp.Reason
    TIMEOUT: HangUp.Reason
    PAYLOAD_LIMIT_EXCEEDED: HangUp.Reason
    MESSAGE_MALFORMED: HangUp.Reason
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: HangUp.Reason
    def __init__(self, reason: _Optional[_Union[HangUp.Reason, str]] = ...) -> None: ...

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
    __slots__ = ("user", "timestamp", "expiry_at", "location")
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
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    user: User
    timestamp: float
    expiry_at: float
    location: LiveLocation.Location
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., timestamp: _Optional[float] = ..., expiry_at: _Optional[float] = ..., location: _Optional[_Union[LiveLocation.Location, _Mapping]] = ...) -> None: ...

class LiveLocations(_message.Message):
    __slots__ = ("extended_live_locations",)
    class ExtendedLiveLocation(_message.Message):
        __slots__ = ("live_location", "chatmessageID")
        LIVE_LOCATION_FIELD_NUMBER: _ClassVar[int]
        CHATMESSAGEID_FIELD_NUMBER: _ClassVar[int]
        live_location: LiveLocation
        chatmessageID: str
        def __init__(self, live_location: _Optional[_Union[LiveLocation, _Mapping]] = ..., chatmessageID: _Optional[str] = ...) -> None: ...
    EXTENDED_LIVE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    extended_live_locations: _containers.RepeatedCompositeFieldContainer[LiveLocations.ExtendedLiveLocation]
    def __init__(self, extended_live_locations: _Optional[_Iterable[_Union[LiveLocations.ExtendedLiveLocation, _Mapping]]] = ...) -> None: ...
