import argparse

from google.oauth2.credentials import Credentials

from py2gsuite import CredentialType, ScopeType, SheetsAPI
from py2gsuite.utils import get_credential


def main():
    """Simple example of SheetsAPI."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--credential",
        type=str,
        help="Credential file path as json",
        required=True,
    )
    parser.add_argument(
        "-id",
        "--sheet_id",
        type=str,
        help="Presentation ID",
        required=True,
    )
    parser.add_argument(
        "--scope",
        choices=["read", "edit"],
        help="Scope type, [read: ReadOnly, edit: Editable]",
        required=True,
    )

    args = parser.parse_args()
    credential_file: str = args.credential
    sheet_id: str = args.sheet_id
    scope_name: str = args.scope
    if scope_name == "read":
        scope: ScopeType = ScopeType.SHEETS_READONLY
    elif scope_name == "edit":
        scope: ScopeType = ScopeType.SHEETS_EDITABLE
    else:
        raise ValueError(f"Unexpected scope: {scope_name}")

    creds: Credentials = get_credential(
        credential_file,
        CredentialType.OAUTH,
        scope,
    )

    with SheetsAPI(creds, sheet_id) as api:
        # Add values to cells
        values = [["1", "2"], ["[3, 4]", "(5, 6)"], ["G", "H"]]
        range_name = "A1:C3"
        api.add_values(values, range_name)

        # Update values in cells
        values = [["F", "B"], ["C", "D"]]
        range_name = "A1:C2"
        api.update_values(values, range_name)


if __name__ == "__main__":
    main()
