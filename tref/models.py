from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(slots=True)
class SearchResult:
    score: float
    text: str
    citation: str
    library: str
    version: str
    item: str
    signature: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AskResponse:
    library: str
    version: str
    query: str
    results: List[SearchResult]
    answer: str | None = None
    autodetected_library: bool = False
    freshness: Dict[str, Any] | None = None
    warnings: List[str] | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "library": self.library,
            "version": self.version,
            "query": self.query,
            "results": [result.to_dict() for result in self.results],
            "answer": self.answer,
            "autodetected_library": self.autodetected_library,
            "freshness": self.freshness,
            "warnings": self.warnings or [],
        }
