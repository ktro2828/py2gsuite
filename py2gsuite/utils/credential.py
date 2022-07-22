import os.path as osp
import sys

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .logger import get_logger
from .types import CredentialType, ScopeType

logger = get_logger()


def get_credential(
    credential_file: str,
    credential_type: CredentialType = CredentialType.OAUTH,
    scope: ScopeType = ScopeType.DRIVE,
    **kwargs,
) -> Credentials:
    """[summary]
    Returns Credentials instance.

    Args:
        credential_file (str): The json file of credential.
        credential_type (CredentialType): The type of Credential.
            For Sheets/SlidesAPI only allows OAuth2.0 or API Keys. Defaults to CredentialType.OAUTH.
        scope (ScopeType): The type of scope. Defaults to ScopeType.DRIVE.

    **kwargs:
        host (str): Defaults to "localhost".
        port (int): Defaults to 8080.
        cache_token (bool): Defaults to False.

    Returns:
        creds (Credentials): Credential instance.

    Raises:
        FileNotFoundError: When cannot find specified credential file.
    """
    if not osp.exists(credential_file):
        raise FileNotFoundError(f"Cannot find {credential_file}")

    host: str = kwargs.get("host", "localhost")
    port: int = kwargs.get("port", 8080)
    cache_token: bool = kwargs.get("cache_token", False)

    creds: Credentials
    try:
        if credential_type == CredentialType.API_KEYS:
            # TODO
            raise NotImplementedError("Only support CredentialType.OAUTH")
        elif credential_type == CredentialType.OAUTH:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                credential_file,
                scope.value,
            )
            creds: Credentials = flow.run_local_server(host=host, port=port)
        elif credential_type == CredentialType.SERVICE_ACCOUNT:
            raise ValueError("Only support OAuth2.0 or API keys")
        else:
            raise TypeError(f"`credential_type` must be an element of py2gsuite.Type, but got {credential_type}")
    except OSError as err:
        logger.error(err)
        sys.exit(1)

    if cache_token:
        logger.warn("Important personal info is included in the token.json. Please keep it safe.")
        with open(osp.join(osp.dirname(__file__), "token.json"), "w") as token:
            token.write(creds.to_json())

    return creds


def get_credential_from_token(scope: ScopeType):
    """[summary]
    Get Credentials instance from cached token.json.

    Args:
        scope (ScopeType): The ScopeType instance.

    Returns:
        creds (Credentials): The Credentials instance loaded from token.json.

    Raises:
        FileNotFoundError: When there is no token.json.
    """
    if not osp.exists(osp.basename(__file__), "token.json"):
        raise FileNotFoundError("Cannot find token.json")

    try:
        creds: Credentials = Credentials.from_authorized_user_file(
            "token.json",
            scopes=scope,
        )
    except OSError as err:
        logger.error(err)
        sys.exit(1)

    return creds
