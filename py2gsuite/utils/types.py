from enum import Enum


class InsertType(Enum):
    """Type of inserted in google suite."""

    TEXT = "text"
    TABLE = "table"
    GRAPH = "graph"
    IMAGE = "image"


class ScopeType(Enum):
    """Type of scopes for google suite."""

    PRESENTATION_EDITABLE = ["https://www.googleapis.com/auth/presentations"]
    PRESENTATION_READONLY = ["https://www.googleapis.com/auth/presentations.readonly"]
    SHEETS_EDITABLE = ["https://www.googleapis.com/auth/spreadsheets"]
    SHEETS_READONLY = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class CredentialType(Enum):
    """Type of credential."""

    API_KEY = "api_key"
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
