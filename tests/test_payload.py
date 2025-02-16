"""Test cases for the response payload classes."""

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4

from funapis_response import (
    ResponsePayloadBuilder,
    PagingPayloadBuilder,
    OrderingPayloadBuilder,
)
from funapis_response.enums import SortDirection, UserLevel


class TestResponsePayload(unittest.TestCase):
    """Test cases for ResponsePayload and its builder."""

    def setUp(self):
        """Set up test fixtures."""
        self.taipei_tz = ZoneInfo("Asia/Taipei")
        self.test_datetime = datetime.now(self.taipei_tz)
        self.test_uuid = uuid4()

    def test_basic_response(self):
        """Test creating a basic response without optional fields."""
        response = ResponsePayloadBuilder()\
            .with_message_id(self.test_uuid)\
            .with_message_datetime(self.test_datetime)\
            .with_error_code("FUN006600001")\
            .with_error_desc("Success")\
            .build()

        self.assertEqual(response.message_id, self.test_uuid)
        self.assertEqual(response.error_code, "FUN006600001")
        self.assertEqual(response.error_desc, "Success")
        self.assertIsNone(response.data)
        self.assertIsNone(response.paging)

    def test_response_with_data(self):
        """Test response with data payload."""
        test_data = {"key": "value"}
        response = ResponsePayloadBuilder()\
            .with_message_id(self.test_uuid)\
            .with_message_datetime(self.test_datetime)\
            .with_error_code("FUN006600001")\
            .with_error_desc("Success")\
            .with_data(test_data)\
            .build()

        self.assertEqual(response.data, test_data)

    def test_response_with_paging(self):
        """Test response with paging information."""
        order = OrderingPayloadBuilder()\
            .with_property("createTime")\
            .with_direction(SortDirection.DESC)\
            .build()

        paging = PagingPayloadBuilder()\
            .with_page(0)\
            .with_page_size(10)\
            .with_total_elements(100)\
            .with_total_pages(10)\
            .add_order(order)\
            .build()

        response = ResponsePayloadBuilder()\
            .with_message_id(self.test_uuid)\
            .with_message_datetime(self.test_datetime)\
            .with_error_code("FUN006600001")\
            .with_error_desc("Success")\
            .with_paging(paging)\
            .build()

        self.assertIsNotNone(response.paging)
        self.assertEqual(response.paging.page, 0)
        self.assertEqual(response.paging.page_size, 10)
        self.assertEqual(len(response.paging.orders), 1)
        self.assertEqual(response.paging.orders[0].property, "createTime")
        self.assertEqual(response.paging.orders[0].direction, SortDirection.DESC)

    def test_stack_trace_visibility(self):
        """Test stack trace visibility for different user levels."""
        debug_info = "Debug stack trace"
        response = ResponsePayloadBuilder()\
            .with_message_id(self.test_uuid)\
            .with_message_datetime(self.test_datetime)\
            .with_error_code("FUN009900001")\
            .with_error_desc("System Error")\
            .with_stack_trace(debug_info)\
            .build()

        # Test general user can't see stack trace
        general_dict = response.to_dict(UserLevel.GENERAL_USER)
        self.assertNotIn("stackTrace", general_dict)

        # Test developer can see stack trace
        dev_dict = response.to_dict(UserLevel.DEVELOPER)
        self.assertIn("stackTrace", dev_dict)
        self.assertEqual(dev_dict["stackTrace"], debug_info)

    def test_invalid_error_code(self):
        """Test validation of invalid error codes."""
        with self.assertRaises(ValueError):
            ResponsePayloadBuilder()\
                .with_message_id(self.test_uuid)\
                .with_message_datetime(self.test_datetime)\
                .with_error_code("INVALID")\
                .with_error_desc("Test")\
                .build()

    def test_naive_datetime(self):
        """Test validation of naive datetime."""
        naive_dt = datetime.now()
        with self.assertRaises(ValueError):
            ResponsePayloadBuilder()\
                .with_message_id(self.test_uuid)\
                .with_message_datetime(naive_dt)\
                .with_error_code("FUN006600001")\
                .with_error_desc("Test")\
                .build()


class TestPagingPayload(unittest.TestCase):
    """Test cases for PagingPayload and its builder."""

    def test_invalid_page_number(self):
        """Test validation of negative page numbers."""
        with self.assertRaises(ValueError):
            PagingPayloadBuilder()\
                .with_page(-1)\
                .with_page_size(10)\
                .with_total_elements(100)\
                .with_total_pages(10)\
                .build()

    def test_invalid_page_size(self):
        """Test validation of invalid page sizes."""
        with self.assertRaises(ValueError):
            PagingPayloadBuilder()\
                .with_page(0)\
                .with_page_size(0)\
                .with_total_elements(100)\
                .with_total_pages(10)\
                .build()

    def test_ordering(self):
        """Test ordering functionality."""
        order1 = OrderingPayloadBuilder()\
            .with_property("name")\
            .with_direction(SortDirection.ASC)\
            .build()

        order2 = OrderingPayloadBuilder()\
            .with_property("age")\
            .with_direction(SortDirection.DESC)\
            .build()

        paging = PagingPayloadBuilder()\
            .with_page(0)\
            .with_page_size(10)\
            .with_total_elements(100)\
            .with_total_pages(10)\
            .with_orders([order1, order2])\
            .build()

        paging_dict = paging.to_dict()
        self.assertEqual(len(paging_dict["orders"]), 2)
        self.assertEqual(paging_dict["orders"][0]["property"], "name")
        self.assertEqual(paging_dict["orders"][0]["direction"], "ASC")
        self.assertEqual(paging_dict["orders"][1]["property"], "age")
        self.assertEqual(paging_dict["orders"][1]["direction"], "DESC")


if __name__ == '__main__':
    unittest.main()