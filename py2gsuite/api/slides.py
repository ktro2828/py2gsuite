from __future__ import annotations

from secrets import token_hex
from typing import Any, Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from py2gsuite.utils import SlideLayout, get_logger

from .base import APIBase

__all__ = ["SlidesAPI"]

logger = get_logger()


class SlidesAPI(APIBase):
    """The wrapper of Google Slides API.

    Attributes:
        creds (Credentials): The Credentials instance.
        id (str): The ID of presentation.
        service (Resource): The Resource instance.
    """

    def __init__(
        self,
        creds: Credentials,
        presentation_id: str,
        service: Optional[Resource] = None,
    ) -> None:
        """
        Args:
            creds (Credentials): Credentials instance.
            presentation_id (str): ID of presentation.
            service (Optional[Resource]): Resource instance to connect to spreadsheet.
                Defaults to None.
        """
        super().__init__(creds=creds, file_id=presentation_id)
        if service is None:
            self.service: Resource = build("slides", "v1", credentials=self.creds)
        else:
            assert hasattr(service, "presentations")
            self.service: Resource = service

    @classmethod
    def with_new(cls, creds: Credentials, title: str) -> Optional[SlidesAPI]:
        """[summary]
        Create SlidesAPI instance with new presentation.

        Args:
            creds (Credentials): Credentials instance.
            title (str): The title of presentation.

        Returns:
            Optional[SlidesAPI]: SlidesAPI instance. If fail, returns None.
        """
        try:
            service = build("slides", "v1", credentials=creds)
            body = {"title": title}
            presentation = service.presentations().create(body=body).execute()
            presentation_id: str = presentation.get("presentationId")
            logger.info(f"Created presentation with ID:" f"{presentation_id}")
        except HttpError as err:
            logger.error(err)
            return None

        return cls(creds=creds, presentation_id=presentation_id, service=service)

    def __post_update(self, requests: List[Any]) -> Optional[Dict[str, Any]]:
        """[summary]
        Post update requests.

        Args:
            requests (List[Any]): Requests to be posted.

        Returns:
            response (Optional[Dict[str, Any]]): Response result as dict. If fail, returns None.
        """
        try:
            body: Dict[str, List[Any]] = {"requests": requests}
            response: Dict[str, Any] = (
                self.service.presentations()
                .batchUpdate(
                    presentationId=self.id,
                    body=body,
                )
                .execute()
            )
        except HttpError as err:
            logger.error(err)
            return None

        return response

    def exists_page(self, page_id: str) -> bool:
        """Check if the page that has specified page_id exists.

        Args:
            page_id (str): ID of page.

        Returns:
            bool: Wether page exists.
        """
        try:
            response_id: Optional[str] = (
                self.service.presentations()
                .pages()
                .get(
                    presentationId=self.id,
                    pageObjectId=page_id,
                )
            )
        except HttpError as err:
            logger.error(err)
            return False

        return True if response_id == page_id else False

    def create_slide(
        self,
        page_id: str,
        layout: SlideLayout = SlideLayout.BLANK,
    ) -> bool:
        """[summary]
        Create new slide to the presentation.

        Args:
            page_id (str): ID of new page.
            layout (SlideLayout): Defaults to SlideLayout.BLANK

        Returns:
            bool: Whether succeeded to create new slide.
        """
        # if self.exists_page(page_id):
        #     return True
        requests = [
            {
                "createSlide": {
                    "objectId": page_id,
                    "insertionIndex": "1",
                    "slideLayoutReference": {
                        "predefinedLayout": layout.value,
                    },
                }
            }
        ]
        response = self.__post_update(requests)
        if response is not None:
            create_slide_response = response.get("replies")[0].get("createSlide")
            logger.info(f"Created slide with ID:" f"{(create_slide_response.get('objectId'))}")
            return True
        return False

    def add_text(self, text: str, page_id: Optional[str] = None, **kwargs) -> bool:
        """[summary]
        Add new text to specified slide.
        If page_id is not specified, add text to the first slide.

        Args:
            text (str): text info to be inserted.
            element_id (str): ID of text box.
            page_id (str): page ID to be inserted.

        **kwargs:
            element_id (str): the element ID of text. Defaults to 'NewTextBox'.
            magnitude (int): magnitude of textbox. Defaults to 350.

        Returns:
            bool: Whether succeeded to add text.
        """
        if page_id is None:
            page_id = "p"

        element_id: str = kwargs.get("element_id", token_hex(16))
        pt: Dict[str, Any] = {"magnitude": kwargs.get("magnitude", 100), "unit": "PT"}

        requests: List[Dict[str, Any]] = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": pt, "width": pt},
                        "transform": {"scaleX": 1, "scaleY": 1, "translateX": 350, "translateY": 100, "unit": "PT"},
                    },
                }
            },
            # Insert text into the box, using the supplied element ID.
            {"insertText": {"objectId": element_id, "insertionIndex": 0, "text": text}},
        ]
        response = self.__post_update(requests)
        if response is not None:
            create_shape_response = response.get("replies")[0].get("createShape")
            logger.info(f"Created textbox with ID: {create_shape_response.get('objectId')}")
            return True
        return False

    def add_image(self, img_url: str, page_id: Optional[str] = None, **kwargs) -> bool:
        """[summary]
        Add new image to specified slide.
        If page_id is not specified, add image to the first slide.

        Args:
            img_url (str): URL of image.
            page_id (Optional[str]): ID of page. Defaults to None.

        **kwargs:
            image_id (str): ID of image. If None, create with random token. Defaults to None.
            magnitude (int): Size of image. Defaults to 4000.

        Returns:
            bool: Whether succeeded to add image.
        """
        if page_id is None:
            page_id = "p"

        image_id: str = kwargs.get("image_id", token_hex(16))
        emu: Dict[str, Any] = {"magnitude": kwargs.get("magnitude", 4000), "unit": "EMU"}
        requests: List[Dict[str, Any]] = [
            {
                "createImage": {
                    "objectId": image_id,
                    "url": img_url,
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": emu, "width": emu},
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": 100000,
                            "translateY": 100000,
                            "unit": "EMU",
                        },
                    },
                }
            }
        ]
        response: Optional[Dict[str, Any]] = self.__post_update(requests)
        if response is not None:
            create_image_response = response.get("replies")[0].get("createImage")
            logger.info(f"Created image with ID: {create_image_response.get('objectId')}")
            return True
        return False

    def create_empty_table(self, table_id: str, rows: int, cols: int, page_id: Optional[str] = None) -> bool:
        """Create empty table.

        Args:
            table_id (str): The ID of table.
            rows (int): The number of rows.
            cols (int): The number of columns.
            page_id (Optional[str]): The ID of page. If None, the table will be created on the first page.
                Defaults to None.

        Returns:
            bool: Whether succeeded to create the table.
        """
        if page_id is None:
            page_id = "p"

        requests: List[Dict[str, Any]] = [
            {
                "createTable": {
                    "objectId": table_id,
                    "elementProperties": {
                        "pageObjectId": page_id,
                    },
                    "rows": rows,
                    "cols": cols,
                }
            }
        ]
        response: Optional[Dict[str, Any]] = self.__post_update(requests)
        if response is not None:
            create_table_response = response.get("replies")[0].get("createTable")
            logger.info(f"Created table with ID: {create_table_response.get('objectId')}")
            return True
        return False

    def add_table(
        self,
        values: List[List[str]],
        table_id: Optional[str] = None,
        page_id: Optional[str] = None,
    ) -> bool:
        """Add values to the table.

        Args:
            values (List[List[str]]): Values of elements, in shape (rows, cols).
            table_id (Optional[str]): ID of table. If None, create new table. Defaults to None.
            page_id (Optional[str]): ID of page. If None, create on the first page. Defaults to None.

        Returns:
            bool: Whether succeeded to add elements in the table.
        """
        assert isinstance(values, list)
        assert all([isinstance(e, list) for e in values])

        rows: int = len(values)
        cols: int = len(values[0])
        assert all([len(e) == cols for e in values])

        # Create new empty table
        if table_id is None:
            table_id: str = token_hex(16)
            assert self.create_empty_table(
                table_id=table_id,
                rows=rows,
                cols=cols,
                page_id=page_id,
            )

        # Insert to table
        requests: List[Dict[str, Any]] = []
        # cnt: int = 0
        for i, v_rows in enumerate(values):
            for j, v in enumerate(v_rows):
                requests.append(
                    {
                        "insertText": {
                            "objectId": table_id,
                            "cellLocation": {
                                "rowindex": i,
                                "columnIndex": j,
                            },
                            "text": str(v),
                            "insertionIndex": 0,  # cnt
                        }
                    }
                )
                # cnt += 1
        response: Optional[Dict[str, Any]] = self.__post_update(requests)
        if response is not None:
            return True
        return False
