import argparse

from google.oauth2.credentials import Credentials

from py2gsuite import SlidesAPI
from py2gsuite.utils import get_credential


def main():
    """Simple example of SlidesAPI."""

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
        "--presentation_id",
        type=str,
        help="Presentation ID",
        required=True,
    )

    args = parser.parse_args()
    credential_file: str = args.credential
    presentation_id: str = args.presentation_id

    creds: Credentials = get_credential(credential_file)

    with SlidesAPI(creds, presentation_id) as api:
        text: str = "Hello world!"
        api.add_text(text)

        img_url: str = "http://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        api.add_image(img_url)


if __name__ == "__main__":
    main()
