import requests
from typing import Union
import aiohttp

from .ratelimit import RateLimiter
from .exceptions import TimeoutError, NetworkError, RateLimitError, APIError
import asyncio


class HttpClient:
    def __init__(self, calls: int, period: int, base_url: str = "https://api.dexscreener.io/latest", timeout: int = 30):
        self._limiter = RateLimiter(calls, period)
        self.base_url = base_url
        self.timeout = timeout
        
    def _create_absolute_url(self, relative: str) -> str:
        return f"{self.base_url}/{relative}"

    def _handle_response(self, response, url: str):
        """Handle HTTP response and raise appropriate exceptions."""
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            raise RateLimitError(retry_after=int(retry_after) if retry_after else None)
        
        if response.status_code >= 400:
            try:
                error_data = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError):
                error_data = response.text
            
            raise APIError(
                status_code=response.status_code,
                message=f"Request to {url} failed",
                response_data=error_data
            )
        
        try:
            return response.json()
        except ValueError as e:
            raise APIError(
                status_code=response.status_code,
                message=f"Invalid JSON response from {url}",
                response_data=response.text
            )
            
    async def _handle_response_async(self, response: aiohttp.ClientResponse, url: str):
        """Handle HTTP response and raise appropriate exceptions for async requests."""
        if response.status == 429:
            retry_after = response.headers.get('Retry-After')
            raise RateLimitError(retry_after=int(retry_after) if retry_after else None)
        
        if response.status >= 400:
            try:
                error_data = await response.json()
            except (ValueError, aiohttp.ContentTypeError):
                error_data = await response.text()
            
            raise APIError(
                status_code=response.status,
                message=f"Request to {url} failed",
                response_data=error_data
            )
        
        try:
            return await response.json()
        except ValueError:
            text = await response.text()
            raise APIError(
                status_code=response.status,
                message=f"Invalid JSON response from {url}",
                response_data=text
            )
            
    def request(self, method, url, **kwargs) -> Union[list, dict]:
        url = self._create_absolute_url(url)

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        with self._limiter:
            try:
                r = requests.request(method, url, **kwargs)
                return self._handle_response(r, url)
            
            except requests.exceptions.Timeout as e:
                raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")
            
            except requests.exceptions.ConnectionError as e:
                raise NetworkError(e)


    async def request_async(self, method, url, **kwargs):
        url = self._create_absolute_url(url)

        if 'timeout' not in kwargs:
            kwargs['timeout'] = aiohttp.ClientTimeout(total=self.timeout)

        async with self._limiter:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(method, url, **kwargs) as response:
                        return await self._handle_response_async(response, url)
            
            except aiohttp.ClientError as e:
                raise NetworkError(e)
            
            except asyncio.TimeoutError as e:
                raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")