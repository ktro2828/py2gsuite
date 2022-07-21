import pkg_resources

from .api import SheetsAPI, SlidesAPI
from .utils import CredentialType, InsertType, ScopeType

__all__ = (
    "SheetsAPI",
    "SlidesAPI",
    "TEXT",
    "TABLE",
    "GRAPH",
    "IMAGE",
    "PE",
    "PR",
    "SE",
    "SR",
    "API_KEY",
    "OAUTH",
    "SERVICE_ACCOUNT",
    "CredentialType",
    "InsertType",
    "ScopeType",
)

__version__ = pkg_resources.get_distribution("py2gsuite").version


# InsertType alias
TEXT = InsertType.TEXT
TABLE = InsertType.TABLE
GRAPH = InsertType.GRAPH
IMAGE = InsertType.IMAGE

# ScopeType alias
PE = ScopeType.PRESENTATION_EDITABLE
PR = ScopeType.PRESENTATION_READONLY
SE = ScopeType.SHEETS_EDITABLE
SR = ScopeType.SHEETS_READONLY

# CredentialType alias
API_KEY = CredentialType.API_KEY
OAUTH = CredentialType.OAUTH
SERVICE_ACCOUNT = CredentialType.SERVICE_ACCOUNT
