"""Builder implementations for response payload classes."""

from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from funapis_response.core.validator import PayloadValidator
from funapis_response.core.payload import ResponsePayload, PagingPayload, OrderingPayload
from funapis_response.enums import SortDirection


class OrderingPayloadBuilder:
    """Builder for OrderingPayload."""
    
    def __init__(self) -> None:
        self._property: Optional[str] = None
        self._direction: SortDirection = SortDirection.ASC

    def with_property(self, property_name: str) -> 'OrderingPayloadBuilder':
        """
        Set the property name for sorting.
        
        Args:
            property_name: Field name to sort by
            
        Returns:
            Self for method chaining
        """
        self._property = property_name
        return self

    def with_direction(self, direction: SortDirection) -> 'OrderingPayloadBuilder':
        """
        Set the sort direction.
        
        Args:
            direction: Sort direction (ASC/DESC)
            
        Returns:
            Self for method chaining
        """
        self._direction = direction
        return self

    def build(self) -> OrderingPayload:
        """
        Build the OrderingPayload instance.
        
        Raises:
            ValueError: If property is not set
            
        Returns:
            OrderingPayload instance
        """
        if not self._property:
            raise ValueError("Property must be set")
            
        return OrderingPayload(
            property=self._property,
            direction=self._direction
        )


class PagingPayloadBuilder:
    """Builder for PagingPayload."""
    
    def __init__(self) -> None:
        self._page: Optional[int] = None
        self._page_size: Optional[int] = None
        self._total_elements: Optional[int] = None
        self._total_pages: Optional[int] = None
        self._orders: List[OrderingPayload] = []

    def with_page(self, page: int) -> 'PagingPayloadBuilder':
        """
        Set the current page number.
        
        Args:
            page: Zero-based page number
            
        Raises:
            ValueError: If page number is negative
            
        Returns:
            Self for method chaining
        """
        if page < 0:
            raise ValueError("Page number cannot be negative")
        self._page = page
        return self

    def with_page_size(self, page_size: int) -> 'PagingPayloadBuilder':
        """
        Set the page size.
        
        Args:
            page_size: Number of items per page
            
        Raises:
            ValueError: If page size is not positive
            
        Returns:
            Self for method chaining
        """
        if page_size <= 0:
            raise ValueError("Page size must be positive")
        self._page_size = page_size
        return self

    def with_total_elements(self, total_elements: int) -> 'PagingPayloadBuilder':
        """
        Set the total number of elements.
        
        Args:
            total_elements: Total number of items
            
        Raises:
            ValueError: If total elements is negative
            
        Returns:
            Self for method chaining
        """
        if total_elements < 0:
            raise ValueError("Total elements cannot be negative")
        self._total_elements = total_elements
        return self

    def with_total_pages(self, total_pages: int) -> 'PagingPayloadBuilder':
        """
        Set the total number of pages.
        
        Args:
            total_pages: Total number of pages
            
        Raises:
            ValueError: If total pages is negative
            
        Returns:
            Self for method chaining
        """
        if total_pages < 0:
            raise ValueError("Total pages cannot be negative")
        self._total_pages = total_pages
        return self

    def with_orders(self, orders: List[OrderingPayload]) -> 'PagingPayloadBuilder':
        """
        Set the ordering information.
        
        Args:
            orders: List of OrderingPayload instances
            
        Returns:
            Self for method chaining
        """
        self._orders = orders
        return self

    def add_order(self, order: OrderingPayload) -> 'PagingPayloadBuilder':
        """
        Add a single ordering.
        
        Args:
            order: OrderingPayload instance
            
        Returns:
            Self for method chaining
        """
        self._orders.append(order)
        return self

    def build(self) -> PagingPayload:
        """
        Build the PagingPayload instance.
        
        Raises:
            ValueError: If any required field is not set or validation fails
            
        Returns:
            PagingPayload instance
        """
        if any(x is None for x in [self._page, self._page_size, self._total_elements, self._total_pages]):
            raise ValueError("All paging fields must be set")

        # Validate paging parameters
        paging_params = {
            'page': self._page,
            'pageSize': self._page_size,
            'totalElements': self._total_elements,
            'totalPages': self._total_pages
        }
        
        if not PayloadValidator.validate_paging_params(paging_params):
            raise ValueError(
                f"Invalid paging parameters: page={self._page}, "
                f"pageSize={self._page_size}, "
                f"totalElements={self._total_elements}, "
                f"totalPages={self._total_pages}"
            )

        return PagingPayload(
            page=self._page,
            page_size=self._page_size,
            total_elements=self._total_elements,
            total_pages=self._total_pages,
            orders=self._orders
        )


class ResponsePayloadBuilder:
    """Builder for ResponsePayload with simplified security."""
    
    def __init__(self) -> None:
        self._message_id: UUID = uuid4()
        self._message_datetime: datetime = datetime.now(ZoneInfo("Asia/Taipei"))
        self._error_code: Optional[str] = None
        self._error_desc: Optional[str] = None
        self._data: Any = None
        self._paging: Optional[PagingPayload] = None
        self._stack_trace: Optional[str] = None

    def with_message_id(self, message_id: UUID) -> 'ResponsePayloadBuilder':
        """
        Set custom message ID.
        
        Args:
            message_id: UUID for the response
            
        Returns:
            Self for method chaining
        """
        self._message_id = message_id
        return self

    def with_message_datetime(self, message_datetime: datetime) -> 'ResponsePayloadBuilder':
        """
        Set custom message datetime.
        
        Args:
            message_datetime: Timezone-aware datetime object
            
        Raises:
            ValueError: If datetime is not timezone-aware
            
        Returns:
            Self for method chaining
        """
        if not PayloadValidator.validate_datetime_format(message_datetime):
            raise ValueError("Datetime must be timezone-aware")
        self._message_datetime = message_datetime
        return self

    def with_error_code(self, error_code: str) -> 'ResponsePayloadBuilder':
        """
        Set error code.
        
        Args:
            error_code: Error code in FUNxxyyzzz format
            
        Raises:
            ValueError: If error code format is invalid
            
        Returns:
            Self for method chaining
        """
        if not PayloadValidator.validate_error_code(error_code):
            raise ValueError(f"Invalid error code format: {error_code}. Must be in FUNxxyyzzz format.")
        self._error_code = error_code
        return self

    def with_error_desc(self, error_desc: str) -> 'ResponsePayloadBuilder':
        """
        Set error description.
        
        Args:
            error_desc: Human-readable error description
            
        Returns:
            Self for method chaining
        """
        self._error_desc = error_desc
        return self

    def with_data(self, data: Any) -> 'ResponsePayloadBuilder':
        """
        Set response data.
        
        Args:
            data: Any JSON-serializable data
            
        Returns:
            Self for method chaining
        """
        self._data = data
        return self

    def with_paging(self, paging: PagingPayload) -> 'ResponsePayloadBuilder':
        """
        Set paging information.
        
        Args:
            paging: PagingPayload instance
            
        Returns:
            Self for method chaining
        """
        self._paging = paging
        return self

    def with_stack_trace(self, stack_trace: str) -> 'ResponsePayloadBuilder':
        """
        Set stack trace (only visible to developers).
        
        Args:
            stack_trace: Debug stack trace information
            
        Returns:
            Self for method chaining
        """
        self._stack_trace = stack_trace
        return self

    def build(self) -> ResponsePayload:
        """
        Build the ResponsePayload instance.
        
        Raises:
            ValueError: If required fields are not set
            
        Returns:
            ResponsePayload instance
        """
        if not self._error_code or not self._error_desc:
            raise ValueError("Error code and description are required")

        return ResponsePayload(
            message_id=self._message_id,
            message_datetime=self._message_datetime,
            error_code=self._error_code,
            error_desc=self._error_desc,
            data=self._data,
            paging=self._paging,
            _stack_trace=self._stack_trace
        )