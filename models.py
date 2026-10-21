from dataclasses import dataclass, field
from typing import List, Optional


def _filter_fields(cls, data: dict) -> dict:
    known = {f for f in cls.__dataclass_fields__}
    return {k: v for k, v in data.items() if k in known}


@dataclass
class User:
    id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    profileImagePath: Optional[str] = None
    avatarColor: Optional[str] = None
    profileChangedAt: Optional[str] = None


@dataclass
class AlbumUser:
    user: Optional[User] = None
    role: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.user, dict):
            self.user = User(**_filter_fields(User, self.user))


@dataclass
class Album:
    id: str
    albumName: str
    description: Optional[str] = None
    albumThumbnailAssetId: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    ownerId: Optional[str] = None
    owner: Optional[User] = None
    albumUsers: Optional[List[AlbumUser]] = None
    shared: bool = False
    hasSharedLink: bool = False
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    assets: Optional[list] = None
    assetCount: int = 0
    isActivityEnabled: bool = True
    order: Optional[str] = None
    lastModifiedAssetTimestamp: Optional[str] = None
    albumOrder: Optional[str] = None
    isPinned: bool = False
    timelineEnabled: bool = True
    unknown_fields: Optional[dict] = None

    def __post_init__(self):
        if isinstance(self.owner, dict):
            self.owner = User(**_filter_fields(User, self.owner))
        if isinstance(self.albumUsers, list):
            self.albumUsers = [
                AlbumUser(**_filter_fields(AlbumUser, u)) if isinstance(u, dict) else u
                for u in self.albumUsers
            ]

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
    deviceAssetId: Optional[str] = None
    ownerId: Optional[str] = None
    deviceId: Optional[str] = None
    type: Optional[str] = None
    originalPath: Optional[str] = None
    originalFileName: Optional[str] = None
    originalMimeType: Optional[str] = None
    thumbhash: Optional[str] = None
    fileCreatedAt: Optional[str] = None
    createdAt: Optional[str] = None
    fileModifiedAt: Optional[str] = None
    localDateTime: Optional[str] = None
    updatedAt: Optional[str] = None
    isFavorite: bool = False
    isArchived: bool = False
    isTrashed: bool = False
    visibility: Optional[str] = None
    duration: Optional[str] = None
    exifInfo: ExifInfo = field(default_factory=ExifInfo)
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
        elif self.exifInfo is None:
            self.exifInfo = ExifInfo()

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
