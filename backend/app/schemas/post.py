from enum import StrEnum


class PostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"
    ARCHIVED = "archived"
