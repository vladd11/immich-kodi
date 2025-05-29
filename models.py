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
class AlbumAsset:
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

    def __post_init__(self):
        if isinstance(self.exifInfo, dict):
            self.exifInfo = ExifInfo(**self.exifInfo)
