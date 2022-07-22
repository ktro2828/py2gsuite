import os.path as osp

import pytest
from google.oauth2.credentials import Credentials

from py2gsuite.api import SlidesAPI
from py2gsuite.utils.credential import get_credential


class TestSlidesAPI:
    credential_file: str = osp.join(osp.dirname(__file__), "oauth.json")
    if not osp.exists(credential_file):
        pytest.skip("There is no credential file .json")

    creds: Credentials = get_credential(credential_file, port=5678)
    presentation_id: str = "119bzp-JdYgH5D71LpB89U9X-ameDp24F-gnU2_Ht_4A"
    api: SlidesAPI = SlidesAPI(creds, presentation_id)

    def hoge(self):
        print(self.api.service.presentations().pages().get("NewPage"))

    def test_add_text(self):
        text: str = "Hello world!"
        assert self.api.add_text(text)

    def test_add_image(self):
        img_url: str = "http://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        assert self.api.add_image(img_url)


if __name__ == "__main__":
    api_test = TestSlidesAPI()
    api_test.test_add_text()
    api_test.test_add_image()
