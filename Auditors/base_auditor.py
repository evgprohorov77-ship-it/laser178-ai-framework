from abc import ABC, abstractmethod
from typing import List, Optional
from AI.Models.finding import Finding


class BaseAuditor(ABC):
    """
    Базовый класс для всех аудиторов LAOS.
    Каждый аудитор возвращает List[Finding].
    """

    name: str = "base"
    version: str = "1.0.0"

    @abstractmethod
    def audit(self, url: str, html: str, headers: Optional[dict] = None) -> List[Finding]:
        """
        Принимает URL и HTML страницы.
        Возвращает список Finding.
        """
        pass

    def _headers(self, headers: Optional[dict] = None) -> dict:
        default = {"Cookie": "beget=begetok"}
        if headers:
            default.update(headers)
        return default
