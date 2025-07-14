from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessage(_message.Message):
    __slots__ = ["author", "document", "group", "live_location", "messageSnowflake", "textContent", "translation", "user", "userOfGroup"]
    class UserOfGroup(_message.Message):
        __slots__ = ["group", "user"]
        GROUP_FIELD_NUMBER: ClassVar[int]
        USER_FIELD_NUMBER: ClassVar[int]
        group: Group
        user: User
        def __init__(self, user: Optional[Union[User, Mapping]] = ..., group: Optional[Union[Group, Mapping]] = ...) -> None: ...
    AUTHOR_FIELD_NUMBER: ClassVar[int]
    DOCUMENT_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    LIVE_LOCATION_FIELD_NUMBER: ClassVar[int]
    MESSAGESNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    TEXTCONTENT_FIELD_NUMBER: ClassVar[int]
    TRANSLATION_FIELD_NUMBER: ClassVar[int]
    USEROFGROUP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    author: User
    document: Document
    group: Group
    live_location: LiveLocation
    messageSnowflake: int
    textContent: str
    translation: Translation
    user: User
    userOfGroup: ChatMessage.UserOfGroup
    def __init__(self, messageSnowflake: Optional[int] = ..., author: Optional[Union[User, Mapping]] = ..., user: Optional[Union[User, Mapping]] = ..., group: Optional[Union[Group, Mapping]] = ..., userOfGroup: Optional[Union[ChatMessage.UserOfGroup, Mapping]] = ..., textContent: Optional[str] = ..., document: Optional[Union[Document, Mapping]] = ..., live_location: Optional[Union[LiveLocation, Mapping]] = ..., translation: Optional[Union[Translation, Mapping]] = ...) -> None: ...

class ChatMessageResponse(_message.Message):
    __slots__ = ["messageSnowflake", "statuses"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class DeliveryStatus(_message.Message):
        __slots__ = ["status", "user"]
        STATUS_FIELD_NUMBER: ClassVar[int]
        USER_FIELD_NUMBER: ClassVar[int]
        status: ChatMessageResponse.Status
        user: User
        def __init__(self, user: Optional[Union[User, Mapping]] = ..., status: Optional[Union[ChatMessageResponse.Status, str]] = ...) -> None: ...
    DELIVERED: ChatMessageResponse.Status
    MESSAGESNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    OTHER_ERROR: ChatMessageResponse.Status
    OTHER_SERVER_NOT_FOUND: ChatMessageResponse.Status
    OTHER_SERVER_TIMEOUT: ChatMessageResponse.Status
    STATUSES_FIELD_NUMBER: ClassVar[int]
    UNKNOWN_STATUS: ChatMessageResponse.Status
    USER_AWAY: ChatMessageResponse.Status
    USER_BLOCKED: ChatMessageResponse.Status
    USER_NOT_FOUND: ChatMessageResponse.Status
    messageSnowflake: int
    statuses: _containers.RepeatedCompositeFieldContainer[ChatMessageResponse.DeliveryStatus]
    def __init__(self, messageSnowflake: Optional[int] = ..., statuses: Optional[Iterable[Union[ChatMessageResponse.DeliveryStatus, Mapping]]] = ...) -> None: ...

class ConnectClient(_message.Message):
    __slots__ = ["udpPort", "user"]
    UDPPORT_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    udpPort: int
    user: User
    def __init__(self, user: Optional[Union[User, Mapping]] = ..., udpPort: Optional[int] = ...) -> None: ...

class ConnectResponse(_message.Message):
    __slots__ = ["result"]
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONNECTED: ConnectResponse.Result
    IS_ALREADY_CONNECTED_ERROR: ConnectResponse.Result
    RESULT_FIELD_NUMBER: ClassVar[int]
    UNKNOWN_ERROR: ConnectResponse.Result
    result: ConnectResponse.Result
    def __init__(self, result: Optional[Union[ConnectResponse.Result, str]] = ...) -> None: ...

class ConnectServer(_message.Message):
    __slots__ = ["features", "serverId"]
    FEATURES_FIELD_NUMBER: ClassVar[int]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    serverId: str
    def __init__(self, serverId: Optional[str] = ..., features: Optional[Iterable[str]] = ...) -> None: ...

class DiscoverServer(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Document(_message.Message):
    __slots__ = ["data", "documentId", "filename", "mimeType"]
    DATA_FIELD_NUMBER: ClassVar[int]
    DOCUMENTID_FIELD_NUMBER: ClassVar[int]
    FILENAME_FIELD_NUMBER: ClassVar[int]
    MIMETYPE_FIELD_NUMBER: ClassVar[int]
    data: bytes
    documentId: str
    filename: str
    mimeType: str
    def __init__(self, documentId: Optional[str] = ..., filename: Optional[str] = ..., mimeType: Optional[str] = ..., data: Optional[bytes] = ...) -> None: ...

class DocumentStatus(_message.Message):
    __slots__ = ["documentSnowflake", "expiry", "result"]
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    AVAILABLE: DocumentStatus.Result
    DELETED: DocumentStatus.Result
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    EXPIRED: DocumentStatus.Result
    EXPIRY_FIELD_NUMBER: ClassVar[int]
    NOT_FOUND: DocumentStatus.Result
    PENDING_UPLOAD: DocumentStatus.Result
    RESULT_FIELD_NUMBER: ClassVar[int]
    UNKNOWN_ERROR: DocumentStatus.Result
    documentSnowflake: int
    expiry: int
    result: DocumentStatus.Result
    def __init__(self, documentSnowflake: Optional[int] = ..., result: Optional[Union[DocumentStatus.Result, str]] = ..., expiry: Optional[int] = ...) -> None: ...

class DownloadDocument(_message.Message):
    __slots__ = ["documentSnowflake"]
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    documentSnowflake: int
    def __init__(self, documentSnowflake: Optional[int] = ...) -> None: ...

class DownloadingDocument(_message.Message):
    __slots__ = ["data", "documentSnowflake", "result"]
    DATA_FIELD_NUMBER: ClassVar[int]
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: ClassVar[int]
    RESULT_FIELD_NUMBER: ClassVar[int]
    data: bytes
    documentSnowflake: int
    result: DocumentStatus.Result
    def __init__(self, documentSnowflake: Optional[int] = ..., result: Optional[Union[DocumentStatus.Result, str]] = ..., data: Optional[bytes] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ["groupId", "serverId"]
    GROUPID_FIELD_NUMBER: ClassVar[int]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    groupId: str
    serverId: str
    def __init__(self, groupId: Optional[str] = ..., serverId: Optional[str] = ...) -> None: ...

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
    __slots__ = ["author", "expiry_at", "group", "location", "timestamp", "user", "userOfGroup"]
    class Location(_message.Message):
        __slots__ = ["latitude", "longitude"]
        LATITUDE_FIELD_NUMBER: ClassVar[int]
        LONGITUDE_FIELD_NUMBER: ClassVar[int]
        latitude: float
        longitude: float
        def __init__(self, latitude: Optional[float] = ..., longitude: Optional[float] = ...) -> None: ...
    AUTHOR_FIELD_NUMBER: ClassVar[int]
    EXPIRY_AT_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    LOCATION_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    USEROFGROUP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    author: User
    expiry_at: float
    group: Group
    location: LiveLocation.Location
    timestamp: float
    user: User
    userOfGroup: UserOfGroup
    def __init__(self, author: Optional[Union[User, Mapping]] = ..., user: Optional[Union[User, Mapping]] = ..., group: Optional[Union[Group, Mapping]] = ..., userOfGroup: Optional[Union[UserOfGroup, Mapping]] = ..., timestamp: Optional[float] = ..., expiry_at: Optional[float] = ..., location: Optional[Union[LiveLocation.Location, Mapping]] = ...) -> None: ...

class LiveLocations(_message.Message):
    __slots__ = ["extended_live_locations"]
    class ExtendedLiveLocation(_message.Message):
        __slots__ = ["live_location", "messageSnowflake"]
        LIVE_LOCATION_FIELD_NUMBER: ClassVar[int]
        MESSAGESNOWFLAKE_FIELD_NUMBER: ClassVar[int]
        live_location: LiveLocation
        messageSnowflake: int
        def __init__(self, live_location: Optional[Union[LiveLocation, Mapping]] = ..., messageSnowflake: Optional[int] = ...) -> None: ...
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
        __slots__ = ["featureName", "port", "udpPort"]
        FEATURENAME_FIELD_NUMBER: ClassVar[int]
        PORT_FIELD_NUMBER: ClassVar[int]
        UDPPORT_FIELD_NUMBER: ClassVar[int]
        featureName: str
        port: int
        udpPort: int
        def __init__(self, featureName: Optional[str] = ..., port: Optional[int] = ..., udpPort: Optional[int] = ...) -> None: ...
    FEATURE_FIELD_NUMBER: ClassVar[int]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    feature: _containers.RepeatedCompositeFieldContainer[ServerAnnounce.Feature]
    serverId: str
    def __init__(self, serverId: Optional[str] = ..., feature: Optional[Iterable[Union[ServerAnnounce.Feature, Mapping]]] = ...) -> None: ...

class Translation(_message.Message):
    __slots__ = ["original_message", "target_language"]
    class Language(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DE: Translation.Language
    EN: Translation.Language
    ORIGINAL_MESSAGE_FIELD_NUMBER: ClassVar[int]
    TARGET_LANGUAGE_FIELD_NUMBER: ClassVar[int]
    ZH: Translation.Language
    original_message: str
    target_language: Translation.Language
    def __init__(self, original_message: Optional[str] = ..., target_language: Optional[Union[Translation.Language, str]] = ...) -> None: ...

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

class UnsupportedMessage(_message.Message):
    __slots__ = ["message_name"]
    MESSAGE_NAME_FIELD_NUMBER: ClassVar[int]
    message_name: str
    def __init__(self, message_name: Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["serverId", "userId"]
    SERVERID_FIELD_NUMBER: ClassVar[int]
    USERID_FIELD_NUMBER: ClassVar[int]
    serverId: str
    userId: str
    def __init__(self, userId: Optional[str] = ..., serverId: Optional[str] = ...) -> None: ...

class UserOfGroup(_message.Message):
    __slots__ = ["group", "user"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    USER_FIELD_NUMBER: ClassVar[int]
    group: Group
    user: User
    def __init__(self, user: Optional[Union[User, Mapping]] = ..., group: Optional[Union[Group, Mapping]] = ...) -> None: ...
