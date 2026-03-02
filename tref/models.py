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
    section: str = ""
    source_url: str | None = None
    source_title: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["confidence"] = self.score
        data["doc_url"] = self.source_url
        return data


@dataclass(slots=True)
class AskResponse:
    library: str
    version: str
    query: str
    results: List[SearchResult]
    version_requested: str | None = None
    version_resolution: Dict[str, Any] | None = None
    version_mismatch: bool = False
    answer: str | None = None
    autodetected_library: bool = False
    freshness: Dict[str, Any] | None = None
    provenance: Dict[str, Any] | None = None
    guidance: Dict[str, Any] | None = None
    warnings: List[str] | None = None
    full_document: Dict[str, Any] | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "library": self.library,
            "version": self.version,
            "version_requested": self.version_requested,
            "version_resolution": self.version_resolution,
            "version_mismatch": self.version_mismatch,
            "query": self.query,
            "results": [result.to_dict() for result in self.results],
            "answer": self.answer,
            "autodetected_library": self.autodetected_library,
            "freshness": self.freshness,
            "provenance": self.provenance,
            "guidance": self.guidance,
            "warnings": self.warnings or [],
            "full_document": self.full_document,
        }
