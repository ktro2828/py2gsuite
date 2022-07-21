# SheetsAPI

About detail, see [py2gsuite/api/sheets.py](../py2gsuite/api/sheets.py)

```python
from py2gsuite import CredentialType, ScopeType, SheetsAPI
from py2gsuite.utils import get_credential

# Pre-required
credential_file: str = <YOUR_CREDENTIAL_PATH>.json
sheets_id: str = <YOUR_SPREADSHEETS_ID>

creds = get_credential(
    credential_file,
    CredentialType.OAUTH,
    ScopeType.SHEETS_EDITABLE,
)

api = SheetsAPI(creds, sheets_id)

# Add text: If cells are already filled, add to new rows and columns.
values = [["1", "2"], ["[3, 4]", "(5, 6)"], ["G", "H"]]
range_name = "A1:C3"
api.add_values(values, range_name)

# Update text: If cells are already filled, overwrite them.
values = [["F", "B"], ["C", "D"]]
range_name = "A1:C2"
api.update_values(values, range_name)

api.close()
```
