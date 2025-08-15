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
    startDate: str
    endDate: str
    assets: list
    assetCount: int
    isActivityEnabled: bool
    order: str
    lastModifiedAssetTimestamp: str

    def __post_init__(self):
        if isinstance(self.owner, dict):
            self.owner = User(**self.owner)
        if isinstance(self.albumUsers, list):
            self.albumUsers = [AlbumUser(**user) for user in self.albumUsers]


@dataclass
class ExifInfo:
    make: str
    model: str
    exifImageWidth: int
    exifImageHeight: int
    fileSizeInByte: int
    orientation: str
    dateTimeOriginal: str
    modifyDate: str
    timeZone: str
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
    description: str = ""
    projectionType: Optional[str] = None
    rating: Optional[int] = None


@dataclass
class ItemAsset:
    id: str
    deviceAssetId: str
    ownerId: str

    deviceId: str
    libraryId: Optional[str]
    type: str
    originalPath: str
    originalFileName: str
    originalMimeType: str
    thumbhash: str
    fileCreatedAt: str
    fileModifiedAt: str
    localDateTime: str
    updatedAt: str
    isFavorite: bool
    isArchived: bool
    isTrashed: bool
    visibility: str
    duration: str
    exifInfo: ExifInfo
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

    def __post_init__(self):
        if isinstance(self.exifInfo, dict):
            self.exifInfo = ExifInfo(**self.exifInfo)


@dataclass
class TimelineBucket:
    timeBucket: str
    count: int


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
