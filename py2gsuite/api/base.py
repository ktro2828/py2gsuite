from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource


class APIBase(ABC):
    @abstractmethod
    def __init__(self, creds: Credentials, file_id: str) -> None:
        super().__init__()
        self.creds: Credentials = creds
        self.id: str = file_id
        self.service: Resource

    @classmethod
    @abstractclassmethod
    def with_new(cls, creds: Credentials, title: str) -> Optional[APIBase]:
        pass

    def close(self) -> None:
        self.service.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
