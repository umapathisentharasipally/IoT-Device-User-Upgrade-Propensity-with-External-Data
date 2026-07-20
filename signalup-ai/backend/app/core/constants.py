from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class ResponseMessage:
    SUCCESS = "Operation completed successfully."
    HEALTH_OK = "Service is healthy."
    DATABASE_OK = "Database connection is healthy."
    DATABASE_ERROR = "Database connection failed."
    INTERNAL_ERROR = "Internal server error."