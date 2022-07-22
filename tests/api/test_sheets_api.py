import os.path as osp

import pytest
from httplib2 import Credentials

from py2gsuite.api import SheetsAPI
from py2gsuite.utils import get_credential


class TestSheetsAPI:
    credential_file: str = osp.join(osp.dirname(__file__), "oauth.json")
    if not osp.exists(credential_file):
        pytest.skip("There is no credential file .json")

    creds: Credentials = get_credential(credential_file, port=4567)
    sheet_id: str = "1F-eEyCnrsMNQtXWNCCGG7rV-c4yCfJGTL5ZTLVHogTw"
    api: SheetsAPI = SheetsAPI(creds, sheet_id)

    def test_add_values(self):
        values = [["1", "2"], ["[3, 4]", "(5, 6)"], ["G", "H"]]
        range_name = "A1:C3"
        assert self.api.add_values(values, range_name)

    def test_update_values(self):
        values = [["F", "B"], ["C", "D"]]
        range_name = "C1:E2"
        assert self.api.update_values(values, range_name)


if __name__ == "__main__":
    api_test = TestSheetsAPI()
    api_test.test_add_values()
    api_test.test_update_values()
