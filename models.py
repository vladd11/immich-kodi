from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: str
    email: str
    name: str
    profileImagePath: str
    avatarColor: str
    profileChangedAt: str


@dataclass
class AlbumUser:
    user: User
    role: str


@dataclass
class Album:
    albumName: str
    description: str
    albumThumbnailAssetId: str
    createdAt: str
    updatedAt: str
    id: str
    ownerId: str
    owner: User
    albumUsers: List[AlbumUser]
    shared: bool
    hasSharedLink: bool
    assets: list
    assetCount: int
    isActivityEnabled: bool
    order: str
    # Additional optional fields for API resilience
    startDate: str = None
    endDate: str = None
    lastModifiedAssetTimestamp: str = None
    albumOrder: Optional[str] = None
    isPinned: bool = False
    timelineEnabled: bool = True
    unknown_fields: Optional[dict] = None

    def __post_init__(self):
        if isinstance(self.owner, dict):
            self.owner = User(**self.owner)
        if isinstance(self.albumUsers, list):
            self.albumUsers = [AlbumUser(**user) for user in self.albumUsers]

    @classmethod
    def from_api_response(cls, data: dict) -> "Album":
        """Create Album from API response, ignoring unknown fields."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        unknown = {k: v for k, v in data.items() if k not in known_fields}
        if unknown:
            filtered_data["unknown_fields"] = unknown
        return cls(**filtered_data)


@dataclass
class ExifInfo:
    make: Optional[str] = None
    model: Optional[str] = None
    exifImageWidth: Optional[int] = None
    exifImageHeight: Optional[int] = None
    fileSizeInByte: Optional[int] = None
    orientation: Optional[str] = None
    dateTimeOriginal: Optional[str] = None
    modifyDate: Optional[str] = None
    timeZone: Optional[str] = None
    lensModel: Optional[str] = None
    fNumber: Optional[float] = None
    focalLength: Optional[float] = None
    iso: Optional[int] = None
    exposureTime: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    projectionType: Optional[str] = None
    rating: Optional[int] = None
    # Additional optional fields for API resilience
    artist: Optional[str] = None
    software: Optional[str] = None
    copyright: Optional[str] = None
    unknown_fields: Optional[dict] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "ExifInfo":
        """Create ExifInfo from API response, ignoring unknown fields."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        unknown = {k: v for k, v in data.items() if k not in known_fields}
        if unknown:
            filtered_data["unknown_fields"] = unknown
        return cls(**filtered_data)


@dataclass
class ItemAsset:
    id: str
    deviceAssetId: str
    ownerId: str
    deviceId: str
    type: str
    originalPath: str
    originalFileName: str
    originalMimeType: str
    thumbhash: str
    fileCreatedAt: str
    createdAt: str
    fileModifiedAt: str
    localDateTime: str
    updatedAt: str
    isFavorite: bool
    isArchived: bool
    isTrashed: bool
    visibility: str
    duration: str
    exifInfo: ExifInfo
    libraryId: Optional[str] = None
    livePhotoVideoId: Optional[str] = None
    people: Optional[List[str]] = None
    checksum: Optional[str] = None
    isOffline: bool = False
    hasMetadata: bool = True
    duplicateId: Optional[str] = None
    resized: bool = False
    owner: Optional[User] = None
    tags: Optional[List[str]] = None
    unassignedFaces: Optional[List[str]] = None
    stack: Optional[str] = None
    # Additional fields from newer Immich API versions
    width: Optional[int] = None
    height: Optional[int] = None
    thumbhashV2: Optional[str] = None
    encodedVideoPath: Optional[str] = None
    isExternal: bool = False
    isReadOnly: bool = False
    sidecarPath: Optional[str] = None
    isVisible: bool = True
    # Accept and ignore any additional fields from API
    unknown_fields: Optional[dict] = None

    def __post_init__(self):
        if isinstance(self.exifInfo, dict):
            self.exifInfo = ExifInfo.from_api_response(self.exifInfo)

    @classmethod
    def from_api_response(cls, data: dict) -> "ItemAsset":
        """Create ItemAsset from API response, ignoring unknown fields."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        unknown = {k: v for k, v in data.items() if k not in known_fields}
        if unknown:
            filtered_data["unknown_fields"] = unknown
        return cls(**filtered_data)


@dataclass
class TimelineBucket:
    timeBucket: str
    count: int
    # Additional optional fields for API resilience
    unknown_fields: Optional[dict] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "TimelineBucket":
        """Create TimelineBucket from API response, ignoring unknown fields."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        unknown = {k: v for k, v in data.items() if k not in known_fields}
        if unknown:
            filtered_data["unknown_fields"] = unknown
        return cls(**filtered_data)


@dataclass
class TimeBucket:
    city: Optional[List[str]]
    country: Optional[List[str]]
    duration: Optional[List[float]]
    id: List[str]
    visibility: List[str]
    isFavorite: List[str]
    isImage: List[str]
    isTrashed: List[str]
    livePhotoVideoId: List[str]
    localOffsetHours: List[int]
    fileCreatedAt: List[str]
    ownerId: List[str]
    projectionType: Optional[str]
    ratio: Optional[float]
    status: List[str]
    thumbhash: List[str]
    visibility: List[str]
