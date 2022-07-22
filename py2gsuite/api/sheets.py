from __future__ import annotations

from typing import Any, Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from py2gsuite.utils import get_logger

from .base import APIBase

__all__ = ["SheetsAPI"]

logger = get_logger()


class SheetsAPI(APIBase):
    """[summary]
    The wrapper of Google Sheets API.

    Attributes:
        creds (Credentials): Credentials instance.
        sheet_id (str): ID of spreadsheet.
        service (Resource): Resource instance to connect to spreadsheet.
    """

    def __init__(
        self,
        creds: Credentials,
        sheet_id: str,
        service: Optional[Resource] = None,
    ) -> None:
        """
        Args:
            creds (Credentials): Credentials instance.
            sheet_id (str): ID of spreadsheet.
            service (Optional[Resource]): Resource instance to connect to spreadsheet.
                Defaults to None.
        """
        super().__init__(creds=creds, file_id=sheet_id)
        if service is None:
            self.service: Resource = build("sheets", "v4", credentials=creds)
        else:
            assert hasattr(service, "spreadsheets")
            self.service: Resource = service

    @classmethod
    def with_new(cls, creds: Credentials, title: str) -> Optional[SheetsAPI]:
        """Create instance with a new sheet.

        Args:
            creds (Credentials): The Credentials instance.
            title (str): The title of a sheet.

        Returns:
            Optional[SheetsAPI]: If failed to request, returns None.
        """
        try:
            service: Resource = build("sheets", "v4", credentials=creds)
            body = {"properties": {"title": title}}
            spreadsheet = service.spreadsheets().create(body=body, fields="spreadsheetId").execute()
            sheet_id: str = spreadsheet.get("spreadsheetId")
            logger.info(f"Spreadsheet ID: {sheet_id}")
        except HttpError as err:
            logger.error(err)
            return None
        return cls(creds, sheet_id, service)

    def add_values(
        self,
        values: List[List[str]],
        range_name: str,
        value_input_option: Optional[str] = None,
        sheet_id: Optional[str] = None,
    ) -> bool:
        """Add values on the cells. If cells are already filled, the old ones are remained.

        Args:
            values (List[List[str]]): Values of cells, in shape (rows, cols)
            range_name (str): Range of cells.
                For example, 'A1:C2' means values will be inserted on the cells from A1 to B2.
            value_input_option (Optional[str]): Input option. Defaults to None.
            sheet_id (Optional[str]): ID of sheet. Defaults to None.

        Returns:
            bool: Whether succeeded to add values.
        """
        if value_input_option is None:
            value_input_option = "USER_ENTERED"

        if sheet_id is None:
            sheet_id = self.id

        try:
            body: Dict[str, List[Any]] = {"values": values}
            result: Dict[str, Any] = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=sheet_id,
                    range=range_name,
                    valueInputOption=value_input_option,
                    body=body,
                )
                .execute()
            )
            logger.info(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        except HttpError as err:
            logger.error(err)
            return False

        return True

    def update_values(
        self,
        values: List[List[str]],
        range_name: str,
        value_input_option: Optional[str] = None,
        sheet_id: Optional[str] = None,
    ) -> bool:
        """Add values on the cells. If cells are already filled, these will be overwritten.

        Args:
            values (List[List[str]]): Values of cells, in shape (rows, cols)
            range_name (str): Range of cells.
                For example, 'A1:C2' means values will be inserted on the cells from A1 to B2.
            value_input_option (Optional[str]): Input option. Defaults to None.
            sheet_id (Optional[str]): ID of sheet. Defaults to None.

        Returns:
            bool: Whether succeeded to update values.
        """
        if value_input_option is None:
            value_input_option = "USER_ENTERED"

        if sheet_id is None:
            sheet_id = self.id

        try:
            body: Dict[str, List[Any]] = {"values": values}
            result: Dict[str, Any] = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=sheet_id,
                    range=range_name,
                    valueInputOption=value_input_option,
                    body=body,
                )
                .execute()
            )
            logger.info(f"{result.get('updatedCells')} cells updated.")
        except HttpError as err:
            logger.error(err)
            return False

        return True

    def is_empty(self, range_name: str) -> bool:
        """Check whether specified cells are empty.
        Args:
            range_name (str): Range of cells.

        Returns:
            bool: Whether all cells are empty.
        """
        result = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range_name).execute()
        values = result.get("values")

        return values is None
