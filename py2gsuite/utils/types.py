from enum import Enum


class InsertType(Enum):
    """Type of inserted in google suite."""

    TEXT = "text"
    TABLE = "table"
    GRAPH = "graph"
    IMAGE = "image"


class ScopeType(Enum):
    """Type of scopes for google suite.

    PRESENTATION_EDITABLE: Allows read/write access to the user's presentations and their properties.
    PRESENTATION_READONLY: Allows read-only access to the user's presentations and their properties.
    SHEETS_EDITABLE: Allows read/write access to the user's sheets and their properties.
    SHEETS_READONLY: Allows read-only access to the user's sheets and their properties.
    DRIVE_FILES: Per-file access to files created or opened by the app.
    DRIVE_READONLY: Allows read-only access to the user's file metadata and file content.
    DRIVE: Full, permissive scope to access all of a user's files.
        Request this scope only when it is strictly necessary.
    """

    PRESENTATION_EDITABLE = ["https://www.googleapis.com/auth/presentations"]
    PRESENTATION_READONLY = ["https://www.googleapis.com/auth/presentations.readonly"]
    SHEETS_EDITABLE = ["https://www.googleapis.com/auth/spreadsheets"]
    SHEETS_READONLY = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    DRIVE_FILES = ["https://www.googleapis.com/auth/drive.file"]
    DRIVE_READONLY = ["https://www.googleapis.com/auth/drive.readonly"]
    DRIVE = ["https://www.googleapis.com/auth/drive"]


class CredentialType(Enum):
    """Type of credential."""

    API_KEYS = "api_keys"
    OAUTH = "oauth"
    SERVICE_ACCOUNT = "service_account"


class SlideLayout(Enum):
    """Type of slide layout"""

    BLANK = "BLANK"
    CAPTION_ONLY = "CAPTION_ONLY"
    TITLE = "TITLE"
    TITLE_AND_BODY = "TITLE_AND_BODY"
    TITLE_AND_TWO_COLUMNS = "TITLE_AND_TWO_COLUMNS"
    TITLE_ONLY = "TITLE_ONLY"
    SECTION_HEADER = "SECTION_HEADER"
    SECTION_TITLE_AND_DESCRIPTION = "SECTION_TITLE_AND_DESCRIPTION"
    ONE_COLUMN_TEXT = "ONE_COLUMN_TEXT"
    MAIN_POINT = "MAIN_POINT"
    BIG_NUMBER = "BIG_NUMBER"
