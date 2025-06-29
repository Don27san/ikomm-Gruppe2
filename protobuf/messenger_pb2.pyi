from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessage(_message.Message):
    __slots__ = ["author", "live_location", "messageId", "text", "timestamp", "user"]
    AUTHOR_FIELD_NUMBER: ClassVar[int]
    LIVE_LOCATION_FIELD_NUMBER: ClassVar[int]
    MESSAGEID_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    author: User
    live_location: LiveLocation
    messageId: str
    text: str
    timestamp: _timestamp_pb2.Timestamp
    user: User
    def __init__(self, messageId: Optional[str] = ..., timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., author: Optional[Union[User, Mapping]] = ..., user: Optional[Union[User, Mapping]] = ..., text: Optional[str] = ..., live_location: Optional[Union[LiveLocation, Mapping]] = ...) -> None: ...

class ConnectClient(_message.Message):
    __slots__ = ["location_port", "typingPort", "user"]
    LOCATION_PORT_FIELD_NUMBER: ClassVar[int]
    TYPINGPORT_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    location_port: int
    typingPort: int
    user: User
    def __init__(self, user: Optional[Union[User, Mapping]] = ..., typingPort: Optional[int] = ..., location_port: Optional[int] = ...) -> None: ...

class ConnectionResponse(_message.Message):
    __slots__ = ["result"]
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONNECTED: ConnectionResponse.Result
    IS_ALREADY_CONNECTED_ERROR: ConnectionResponse.Result
    RESULT_FIELD_NUMBER: ClassVar[int]
    UNKNOWN_ERROR: ConnectionResponse.Result
    result: ConnectionResponse.Result
    def __init__(self, result: Optional[Union[ConnectionResponse.Result, str]] = ...) -> None: ...

class DiscoverServer(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HangUp(_message.Message):
    __slots__ = ["reason"]
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    EXIT: HangUp.Reason
    MESSAGE_MALFORMED: HangUp.Reason
    PAYLOAD_LIMIT_EXCEEDED: HangUp.Reason
    REASON_FIELD_NUMBER: ClassVar[int]
    TIMEOUT: HangUp.Reason
    UNKNOWN_REASON: HangUp.Reason
    reason: HangUp.Reason
    def __init__(self, reason: Optional[Union[HangUp.Reason, str]] = ...) -> None: ...

class LiveLocation(_message.Message):
    __slots__ = ["expiry_at", "location", "timestamp", "user"]
    class Location(_message.Message):
        __slots__ = ["latitude", "longitude"]
        LATITUDE_FIELD_NUMBER: ClassVar[int]
        LONGITUDE_FIELD_NUMBER: ClassVar[int]
        latitude: float
        longitude: float
        def __init__(self, latitude: Optional[float] = ..., longitude: Optional[float] = ...) -> None: ...
    EXPIRY_AT_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    expiry_at: float
    location: LiveLocation.Location
    timestamp: float
    user: User
    def __init__(self, user: Optional[Union[User, Mapping]] = ..., timestamp: Optional[float] = ..., expiry_at: Optional[float] = ..., location: Optional[Union[LiveLocation.Location, Mapping]] = ...) -> None: ...

class LiveLocations(_message.Message):
    __slots__ = ["extended_live_locations"]
    class ExtendedLiveLocation(_message.Message):
        __slots__ = ["chatmessageID", "live_location"]
        CHATMESSAGEID_FIELD_NUMBER: ClassVar[int]
        LIVE_LOCATION_FIELD_NUMBER: ClassVar[int]
        chatmessageID: str
        live_location: LiveLocation
        def __init__(self, live_location: Optional[Union[LiveLocation, Mapping]] = ..., chatmessageID: Optional[str] = ...) -> None: ...
    EXTENDED_LIVE_LOCATIONS_FIELD_NUMBER: ClassVar[int]
    extended_live_locations: _containers.RepeatedCompositeFieldContainer[LiveLocations.ExtendedLiveLocation]
    def __init__(self, extended_live_locations: Optional[Iterable[Union[LiveLocations.ExtendedLiveLocation, Mapping]]] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ServerAnnounce(_message.Message):
    __slots__ = ["feature", "serverId"]
    class Feature(_message.Message):
        __slots__ = ["featureName", "port"]
        FEATURENAME_FIELD_NUMBER: ClassVar[int]
        PORT_FIELD_NUMBER: ClassVar[int]
        featureName: str
        port: int
        def __init__(self, featureName: Optional[str] = ..., port: Optional[int] = ...) -> None: ...
    FEATURE_FIELD_NUMBER: ClassVar[int]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    feature: _containers.RepeatedCompositeFieldContainer[ServerAnnounce.Feature]
    serverId: str
    def __init__(self, serverId: Optional[str] = ..., feature: Optional[Iterable[Union[ServerAnnounce.Feature, Mapping]]] = ...) -> None: ...

class TypingEvent(_message.Message):
    __slots__ = ["timestamp", "user"]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    timestamp: float
    user: User
    def __init__(self, user: Optional[Union[User, Mapping]] = ..., timestamp: Optional[float] = ...) -> None: ...

class TypingEvents(_message.Message):
    __slots__ = ["typing_events"]
    TYPING_EVENTS_FIELD_NUMBER: ClassVar[int]
    typing_events: _containers.RepeatedCompositeFieldContainer[TypingEvent]
    def __init__(self, typing_events: Optional[Iterable[Union[TypingEvent, Mapping]]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["serverId", "userId"]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    USERID_FIELD_NUMBER: ClassVar[int]
    serverId: str
    userId: str
    def __init__(self, userId: Optional[str] = ..., serverId: Optional[str] = ...) -> None: ...
