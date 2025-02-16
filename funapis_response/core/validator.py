"""Validation utilities for response payload components."""

import re
from datetime import datetime
from typing import Dict


class PayloadValidator:
    """Validator for response payload components."""

    @staticmethod
    def validate_error_code(error_code: str) -> bool:
        """
        Validate error code format (FUNxxyyzzz).
        
        Args:
            error_code: Error code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^FUN\d{9}$'
        return bool(re.match(pattern, error_code))

    @staticmethod
    def validate_datetime_format(dt: datetime) -> bool:
        """
        Validate datetime has timezone information.
        
        Args:
            dt: Datetime to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return dt.tzinfo is not None

    @staticmethod
    def validate_paging_params(params: Dict) -> bool:
        """
        Validate paging parameters.
        
        Args:
            params: Dictionary containing page, pageSize, totalElements, totalPages
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_keys = {'page', 'pageSize', 'totalElements', 'totalPages'}
        
        # Check all required keys exist
        if not all(key in params for key in required_keys):
            return False
            
        # Validate values
        try:
            if params['page'] < 0:
                return False
            if params['pageSize'] <= 0:
                return False
            if params['totalElements'] < 0:
                return False
            if params['totalPages'] < 0:
                return False
                
            # Logical validation
            if params['totalPages'] > 0 and params['page'] >= params['totalPages']:
                return False
                
            return True
        except (TypeError, ValueError):
            return False