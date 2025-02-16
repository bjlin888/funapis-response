"""Core payload classes for the response library."""

from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Any, List, Optional, Dict
from uuid import UUID

from funapis_response.enums import SortDirection, UserLevel


@dataclass(frozen=True)
class OrderingPayload:
    """Immutable class for sorting information."""
    property: str
    direction: SortDirection = SortDirection.ASC

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "property": self.property,
            "direction": self.direction.value
        }


@dataclass(frozen=True)
class PagingPayload:
    """Immutable class for pagination information."""
    page: int
    page_size: int
    total_elements: int
    total_pages: int
    orders: List[OrderingPayload] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "page": self.page,
            "pageSize": self.page_size,
            "totalElements": self.total_elements,
            "totalPages": self.total_pages,
            "orders": [order.to_dict() for order in self.orders]
        }


@dataclass(frozen=True)
class ResponsePayload:
    """
    Immutable class for HTTP API response payload.
    
    Attributes:
        message_id: Unique identifier for the response
        message_datetime: Timestamp of the response (Taiwan timezone)
        error_code: Error code in format FUNxxyyzzz
        error_desc: Description of the error
        data: Response data payload
        paging: Pagination information
        _stack_trace: Stack trace for debugging (private)
    """
    message_id: UUID
    message_datetime: datetime
    error_code: str
    error_desc: str
    data: Optional[Any] = None
    paging: Optional[PagingPayload] = None
    _stack_trace: Optional[str] = None

    def to_dict(self, user_level: UserLevel = UserLevel.GENERAL_USER) -> Dict[str, Any]:
        """
        Convert to dictionary representation.
        
        Args:
            user_level: User's access level for controlling stack trace visibility
        
        Returns:
            Dict containing the response payload
        """
        result = {
            "messageId": str(self.message_id),
            "messageDatetime": self.message_datetime.isoformat(),
            "errorCode": self.error_code,
            "errorDesc": self.error_desc
        }

        if self.data is not None:
            result["data"] = self.data

        if self.paging is not None:
            result["paging"] = self.paging.to_dict()

        # Simplified security: only show stack trace to developers
        if self._stack_trace and user_level == UserLevel.DEVELOPER:
            result["stackTrace"] = self._stack_trace

        return result

    def to_json(self, user_level: UserLevel = UserLevel.GENERAL_USER) -> str:
        """
        Convert to JSON string.
        
        Args:
            user_level: User's access level for controlling stack trace visibility
        
        Returns:
            JSON string representation of the payload
        """
        return json.dumps(self.to_dict(user_level), ensure_ascii=False)