# py2gsuite

py2gsuite is wrapper of Google Sheets/Slides API.

## Pre-requires

- Python >= 3.8
- Poetry

  - Install poetry

    ```bash
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    ```

  - To learn more about poetry, refer to [Poetry documentation](https://python-poetry.org/docs/)

- Credentials

  - Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials)

  - To manage API key securely, refer to [API security best practices](https://developers.google.com/maps/api-security-best-practices)

## Get started

- Install py2gslide

  ```bash
  $ git clone https://github.com/ktro2828/py2gslide.git
  # Install with poetry
  $ poetry add ./py2gslide
  # or Install with pip
  $ pip install -e ./py2gslide
  ```

## References

- [Google Sheets API](https://developers.google.com/sheets/api/reference/rest)
- [Google Slides API](https://developers.google.com/slides/api/reference/rest)
