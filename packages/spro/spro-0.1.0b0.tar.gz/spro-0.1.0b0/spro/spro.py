import httpx
import logging
import os
from typing import List, Optional, Dict, Any
import json
from spro._exceptions import (
    SProError,
    APIError,
    InvalidEntityError,
    InvalidAPIKeyError,
    AuthenticationError,
    ConfigurationError,
    ValidationError,
)

from spro._models import SProRequest

logger = logging.getLogger(__name__)


# Main Spro SDK
class Spro:
    def __init__(
        self, api_key: Optional[str] = None, api_url: Optional[str] = None
    ) -> None:
        self.api_key = api_key or os.getenv("SPRO_API_KEY")
        self.api_url = api_url or os.getenv("SPRO_API_URL", "https://beta.hridaai.com")

        if not self.api_key:
            raise ConfigurationError(
                "API key not provided. Set SPRO_API_KEY environment variable or pass it to api_key parameter."
            )

        self.client = httpx.Client(timeout=30.0)  # 30 seconds timeout
        logger.debug("SPro initialized with API URL: %s", self.api_url)

    def __del__(self):
        self.client.close()

    def _headers(self) -> Dict[str, str]:
        """Helper method to get headers for the API requests."""
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _handle_http_errors(self, response: httpx.Response):
        """Handle HTTP errors based on status codes."""
        if response.status_code == 400:
            raise InvalidEntityError(f"Invalid entity: {response.text}")
        elif response.status_code == 401:
            raise InvalidAPIKeyError(
                f"Invalid API key or unauthorized access: {response.text}"
            )
        elif response.status_code == 403:
            raise AuthenticationError(f"Authentication failed: {response.text}")
        elif response.status_code == 500:
            raise APIError(f"Server error: {response.text}")
        elif response.status_code == 453:
            raise InvalidAPIKeyError(
                f"Invalid API key: {response.text} provided. Please check your API key."
            )
        else:
            # For any other unexpected status codes
            response.raise_for_status()

    def _post_request(
        self, data: Dict[str, Any], retries: int = 3, backoff_factor: float = 0.5
    ) -> Dict[str, Any]:
        """
        Send POST request to the API with retry logic.
        Retries up to `retries` times in case of failures, with exponential backoff.
        """
        url = f"{self.api_url}/v1/redact"
        logger.debug("POST request to %s", url)

        attempt = 0
        while attempt < retries:
            response = self.client.post(url, headers=self._headers(), json=data)
            self._handle_http_errors(response)  # Handle HTTP errors here
            return response.json()  # Return if successful

        # If we exhausted retries, raise an APIError
        raise APIError(f"Failed after {retries} retries")

    def secure(
        self,
        prompt: str = "",
        mask_type: str = "char",
        mask_character: str = "*",
        entities: List[str] = [],
    ) -> Dict[str, Any]:
        """Main method to redact sensitive information."""
        # Input validation checks
        if not prompt or not isinstance(prompt, str):
            raise ValidationError("Invalid prompt: Must be a non-empty string.")
        if not isinstance(mask_character, str) or len(mask_character) != 1:
            raise ValidationError("Invalid mask character: Must be a single character.")
        if not isinstance(entities, list) or not all(
            isinstance(e, str) for e in entities
        ):
            raise ValidationError("Invalid entities: Must be a list of strings.")

        try:
            # Construct request object
            request = SProRequest(
                prompt=prompt,
                mask_type=mask_type,
                mask_character=mask_character,
                entities=entities,
            )
            logger.debug("Created SProRequest: %s", request)

            # Send POST request to redact the prompt with retry logic
            response = self._post_request(json.loads(request.model_dump_json()))
            logger.debug("Received response: %s", response)

            return response

        except SProError as e:
            # Directly raise SProError without re-wrapping it
            logger.error(f"SProError: {e}")
            raise
        except Exception as e:
            # Log any other unexpected errors and wrap them in SProError
            logger.error(f"Unexpected error: {e}")
            raise SProError(f"An unexpected error occurred: {str(e)}")
        


# Asynchronous SPro SDK
class AsyncSpro:
    def __init__(
        self, api_key: Optional[str] = None, api_url: Optional[str] = None
    ) -> None:
        self.api_key = api_key or os.getenv("SPRO_API_KEY")
        self.api_url = api_url or os.getenv("SPRO_API_URL", "https://beta.hridaai.com")

        if not self.api_key:
            raise ConfigurationError(
                "API key not provided. Set SPRO_API_KEY environment variable or pass it to api_key parameter."
            )

        self.client = httpx.AsyncClient(timeout=30.0)  # 30 seconds timeout
        logger.debug("AsyncSPro initialized with API URL: %s", self.api_url)

    async def __aexit__(self, *args):
        await self.client.aclose()

    def _headers(self) -> Dict[str, str]:
        """Helper method to get headers for the API requests."""
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _handle_http_errors(self, response: httpx.Response):
        """Handle HTTP errors based on status codes."""
        if response.status_code == 400:
            raise InvalidEntityError(f"Invalid entity: {response.text}")
        elif response.status_code == 401:
            raise InvalidAPIKeyError(
                f"Invalid API key or unauthorized access: {response.text}"
            )
        elif response.status_code == 403:
            raise AuthenticationError(f"Authentication failed: {response.text}")
        elif response.status_code == 500:
            raise APIError(f"Server error: {response.text}")
        elif response.status_code == 453:
            raise InvalidAPIKeyError(
                f"Invalid API key: {response.text} provided. Please check your API key."
            )
        else:
            # For any other unexpected status codes
            response.raise_for_status()

    async def _post_request(
        self, data: Dict[str, Any], retries: int = 3, backoff_factor: float = 0.5
    ) -> Dict[str, Any]:
        """
        Send POST request to the API with retry logic.
        Retries up to `retries` times in case of failures, with exponential backoff.
        """
        url = f"{self.api_url}/v1/redact"
        logger.debug("POST request to %s", url)

        attempt = 0
        while attempt < retries:
            try:
                response = await self.client.post(
                    url, headers=self._headers(), json=data
                )
                self._handle_http_errors(response)  # Handle HTTP errors here
                return response.json()  # Return if successful
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                # Log retryable errors and retry
                logger.warning(
                    f"Request error: {e}. Retrying ({attempt+1}/{retries})..."
                )
                attempt += 1
                # await asyncio.sleep(backoff_factor * 2 ** attempt)

        # If we exhausted retries, raise an APIError
        raise APIError(f"Failed after {retries} retries")

    async def secure(
        self,
        prompt: str = "",
        mask_type: str = "char",
        mask_character: str = "*",
        entities: List[str] = [],
    ) -> Dict[str, Any]:
        """Main method to redact sensitive information asynchronously."""
        # Input validation checks
        if not prompt or not isinstance(prompt, str):
            raise ValidationError("Invalid prompt: Must be a non-empty string.")
        if not isinstance(mask_character, str) or len(mask_character) != 1:
            raise ValidationError("Invalid mask character: Must be a single character.")
        if not isinstance(entities, list) or not all(
            isinstance(e, str) for e in entities
        ):
            raise ValidationError("Invalid entities: Must be a list of strings.")

        try:
            # Construct request object
            request = SProRequest(
                prompt=prompt,
                mask_type=mask_type,
                mask_character=mask_character,
                entities=entities,
            )
            logger.debug("Created SProRequest: %s", request)

            # Send POST request to redact the prompt with retry logic
            response = await self._post_request(json.loads(request.model_dump_json()))
            logger.debug("Received response: %s", response)

            return response

        except SProError as e:
            # Directly raise SProError without re-wrapping it
            logger.error(f"SProError: {e}")
            raise
        except Exception as e:
            # Log any other unexpected errors and wrap them in SProError
            logger.error(f"Unexpected error: {e}")
            raise SProError(f"An unexpected error occurred: {str(e)}")


