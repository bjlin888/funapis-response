"""Enumeration types for the payload library."""

from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class SortDirection(Enum):
    """Sort direction for ordering."""
    ASC = "ASC"
    DESC = "DESC"


class UserLevel(Enum):
    """User access levels for security control."""
    GENERAL_USER = "GENERAL_USER"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"