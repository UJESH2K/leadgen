from __future__ import annotations

from abc import ABC, abstractmethod

from leadgen_pipeline.models import Tender


class TenderSource(ABC):
    @abstractmethod
    def fetch(self) -> list[Tender]:
        raise NotImplementedError
