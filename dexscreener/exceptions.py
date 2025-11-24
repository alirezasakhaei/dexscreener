class DexscreenerError(Exception):
    pass


class APIError(DexscreenerError):
    def __init__(self, status_code: int, message: str, response_data=None):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data
        super().__init__(f"API Error {status_code}: {message}")


class RateLimitError(APIError):
    def __init__(self, retry_after: int = None):
        self.retry_after = retry_after
        message = "Rate limit exceeded"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(429, message)


class NetworkError(DexscreenerError):
    def __init__(self, original_error: Exception):
        self.original_error = original_error
        super().__init__(f"Network error: {str(original_error)}")


class ValidationError(DexscreenerError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TimeoutError(DexscreenerError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)