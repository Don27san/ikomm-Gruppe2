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
        __slots__ = ("featureName", "port", "udpPort")
        FEATURENAME_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        UDPPORT_FIELD_NUMBER: _ClassVar[int]
        featureName: str
        port: int
        udpPort: int
        def __init__(self, featureName: _Optional[str] = ..., port: _Optional[int] = ..., udpPort: _Optional[int] = ...) -> None: ...
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    serverId: str
    feature: _containers.RepeatedCompositeFieldContainer[ServerAnnounce.Feature]
    def __init__(self, serverId: _Optional[str] = ..., feature: _Optional[_Iterable[_Union[ServerAnnounce.Feature, _Mapping]]] = ...) -> None: ...

class ConnectClient(_message.Message):
    __slots__ = ("user", "udpPort")
    USER_FIELD_NUMBER: _ClassVar[int]
    UDPPORT_FIELD_NUMBER: _ClassVar[int]
    user: User
    udpPort: int
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., udpPort: _Optional[int] = ...) -> None: ...

class ConnectResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_ERROR: _ClassVar[ConnectResponse.Result]
        CONNECTED: _ClassVar[ConnectResponse.Result]
        IS_ALREADY_CONNECTED_ERROR: _ClassVar[ConnectResponse.Result]
    UNKNOWN_ERROR: ConnectResponse.Result
    CONNECTED: ConnectResponse.Result
    IS_ALREADY_CONNECTED_ERROR: ConnectResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ConnectResponse.Result
    def __init__(self, result: _Optional[_Union[ConnectResponse.Result, str]] = ...) -> None: ...

class ConnectServer(_message.Message):
    __slots__ = ("serverId", "features")
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    serverId: str
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, serverId: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

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

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UnsupportedMessage(_message.Message):
    __slots__ = ("message_name",)
    MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    message_name: str
    def __init__(self, message_name: _Optional[str] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("groupId", "serverId")
    GROUPID_FIELD_NUMBER: _ClassVar[int]
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    groupId: str
    serverId: str
    def __init__(self, groupId: _Optional[str] = ..., serverId: _Optional[str] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("documentId", "filename", "mimeType", "data")
    DOCUMENTID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    documentId: str
    filename: str
    mimeType: str
    data: bytes
    def __init__(self, documentId: _Optional[str] = ..., filename: _Optional[str] = ..., mimeType: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class Translation(_message.Message):
    __slots__ = ("original_message", "target_language")
    class Language(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DE: _ClassVar[Translation.Language]
        EN: _ClassVar[Translation.Language]
        ZH: _ClassVar[Translation.Language]
    DE: Translation.Language
    EN: Translation.Language
    ZH: Translation.Language
    ORIGINAL_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TARGET_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    original_message: str
    target_language: Translation.Language
    def __init__(self, original_message: _Optional[str] = ..., target_language: _Optional[_Union[Translation.Language, str]] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("messageSnowflake", "author", "user", "group", "userOfGroup", "textContent", "document", "live_location", "translation")
    class UserOfGroup(_message.Message):
        __slots__ = ("user", "group")
        USER_FIELD_NUMBER: _ClassVar[int]
        GROUP_FIELD_NUMBER: _ClassVar[int]
        user: User
        group: Group
        def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., group: _Optional[_Union[Group, _Mapping]] = ...) -> None: ...
    MESSAGESNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    USEROFGROUP_FIELD_NUMBER: _ClassVar[int]
    TEXTCONTENT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    LIVE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    messageSnowflake: int
    author: User
    user: User
    group: Group
    userOfGroup: ChatMessage.UserOfGroup
    textContent: str
    document: Document
    live_location: LiveLocation
    translation: Translation
    def __init__(self, messageSnowflake: _Optional[int] = ..., author: _Optional[_Union[User, _Mapping]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., group: _Optional[_Union[Group, _Mapping]] = ..., userOfGroup: _Optional[_Union[ChatMessage.UserOfGroup, _Mapping]] = ..., textContent: _Optional[str] = ..., document: _Optional[_Union[Document, _Mapping]] = ..., live_location: _Optional[_Union[LiveLocation, _Mapping]] = ..., translation: _Optional[_Union[Translation, _Mapping]] = ...) -> None: ...

class ChatMessageResponse(_message.Message):
    __slots__ = ("messageSnowflake", "statuses")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_STATUS: _ClassVar[ChatMessageResponse.Status]
        DELIVERED: _ClassVar[ChatMessageResponse.Status]
        OTHER_ERROR: _ClassVar[ChatMessageResponse.Status]
        USER_AWAY: _ClassVar[ChatMessageResponse.Status]
        USER_NOT_FOUND: _ClassVar[ChatMessageResponse.Status]
        OTHER_SERVER_TIMEOUT: _ClassVar[ChatMessageResponse.Status]
        OTHER_SERVER_NOT_FOUND: _ClassVar[ChatMessageResponse.Status]
        USER_BLOCKED: _ClassVar[ChatMessageResponse.Status]
    UNKNOWN_STATUS: ChatMessageResponse.Status
    DELIVERED: ChatMessageResponse.Status
    OTHER_ERROR: ChatMessageResponse.Status
    USER_AWAY: ChatMessageResponse.Status
    USER_NOT_FOUND: ChatMessageResponse.Status
    OTHER_SERVER_TIMEOUT: ChatMessageResponse.Status
    OTHER_SERVER_NOT_FOUND: ChatMessageResponse.Status
    USER_BLOCKED: ChatMessageResponse.Status
    class DeliveryStatus(_message.Message):
        __slots__ = ("user", "status")
        USER_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        user: User
        status: ChatMessageResponse.Status
        def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., status: _Optional[_Union[ChatMessageResponse.Status, str]] = ...) -> None: ...
    MESSAGESNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    messageSnowflake: int
    statuses: _containers.RepeatedCompositeFieldContainer[ChatMessageResponse.DeliveryStatus]
    def __init__(self, messageSnowflake: _Optional[int] = ..., statuses: _Optional[_Iterable[_Union[ChatMessageResponse.DeliveryStatus, _Mapping]]] = ...) -> None: ...

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
        __slots__ = ("live_location", "messageSnowflake")
        LIVE_LOCATION_FIELD_NUMBER: _ClassVar[int]
        MESSAGESNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
        live_location: LiveLocation
        messageSnowflake: int
        def __init__(self, live_location: _Optional[_Union[LiveLocation, _Mapping]] = ..., messageSnowflake: _Optional[int] = ...) -> None: ...
    EXTENDED_LIVE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    extended_live_locations: _containers.RepeatedCompositeFieldContainer[LiveLocations.ExtendedLiveLocation]
    def __init__(self, extended_live_locations: _Optional[_Iterable[_Union[LiveLocations.ExtendedLiveLocation, _Mapping]]] = ...) -> None: ...

class DownloadDocument(_message.Message):
    __slots__ = ("documentSnowflake",)
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    documentSnowflake: int
    def __init__(self, documentSnowflake: _Optional[int] = ...) -> None: ...

class DownloadingDocument(_message.Message):
    __slots__ = ("documentSnowflake", "result", "data")
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    documentSnowflake: int
    result: DocumentStatus.Result
    data: bytes
    def __init__(self, documentSnowflake: _Optional[int] = ..., result: _Optional[_Union[DocumentStatus.Result, str]] = ..., data: _Optional[bytes] = ...) -> None: ...

class DocumentStatus(_message.Message):
    __slots__ = ("documentSnowflake", "result", "expiry")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_ERROR: _ClassVar[DocumentStatus.Result]
        AVAILABLE: _ClassVar[DocumentStatus.Result]
        NOT_FOUND: _ClassVar[DocumentStatus.Result]
        EXPIRED: _ClassVar[DocumentStatus.Result]
        DELETED: _ClassVar[DocumentStatus.Result]
        PENDING_UPLOAD: _ClassVar[DocumentStatus.Result]
    UNKNOWN_ERROR: DocumentStatus.Result
    AVAILABLE: DocumentStatus.Result
    NOT_FOUND: DocumentStatus.Result
    EXPIRED: DocumentStatus.Result
    DELETED: DocumentStatus.Result
    PENDING_UPLOAD: DocumentStatus.Result
    DOCUMENTSNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    documentSnowflake: int
    result: DocumentStatus.Result
    expiry: int
    def __init__(self, documentSnowflake: _Optional[int] = ..., result: _Optional[_Union[DocumentStatus.Result, str]] = ..., expiry: _Optional[int] = ...) -> None: ...
