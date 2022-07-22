# SlidesAPI

About detail, see [py2gsuite/api/slides.py](../py2gsuite/api/slides.py)

```python
from py2gsuite import SlidesAPI
from py2gsuite.utils import get_credential

# Pre-required
credential_file: str = <YOUR_CREDENTIAL_PATH>.json
presentation_id: str = <YOUR_PRESENTATION_ID>

creds = get_credential(credential_file)

api = SlidesAPI(creds, presentation_id)

# Add text.
text: str = "Hello world!"
api.add_text(text)

# Add image uploaded on internet.
img_url: str = "http://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
api.add_image(img_url)

api.close()
```
