from urllib.parse import urljoin, urlencode
import httpx
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base64
import uuid
import json


class BaseSDK:
    _access_key = None
    _base_url = None
    _api_prefix = ""

    @classmethod
    def init(cls, access_key_file: str, base_url: str, api_prefix: str = ""):
        """
        Initialize the SDK with an access key file, base URL, and API prefix.
        :param access_key_file: Path to the JSON file containing access key details.
        :param base_url: Base URL of the API.
        :param api_prefix: Prefix for the API version (e.g., "/api/v1").
        """
        cls._base_url = base_url.rstrip("/")
        cls._api_prefix = api_prefix.rstrip("/")

        # Load the access key details from the file
        try:
            with open(access_key_file, "r") as file:
                cls._access_key = json.load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load access key: {e}")

    @staticmethod
    def _normalize_path(api_prefix: str, path: str, params: dict = None) -> str:
        """
        Normalize and combine the API prefix, path, and query parameters.
        :param api_prefix: The API version prefix (e.g., "/api/v1").
        :param path: The API endpoint path (e.g., "/market/metrics").
        :param params: Query parameters as a dictionary (default is None).
        :return: Combined and normalized path with query string.
        """
        # Combine API prefix and path
        normalized_path = urljoin(api_prefix.rstrip("/") + "/", path.lstrip("/"))
        query_string = f"?{urlencode(params or {})}" if params else ""
        return f"{normalized_path}{query_string}"

    @classmethod
    def _generate_headers(cls, method: str, full_path_with_query: str, body: str = ""):
        """
        Generate the required headers for API requests.
        :param method: HTTP method (e.g., "GET").
        :param full_path_with_query: Full API endpoint path including query parameters.
        :param body: Request body as a string (default is empty).
        :return: A dictionary of headers.
        """
        if not cls._access_key:
            raise RuntimeError("Access key not initialized. Call `init()` first.")

        key = cls._access_key["key"]
        public_key = cls._access_key["publicKey"]
        name = cls._access_key["name"]

        # Generate unique request ID
        request_id = uuid.uuid1().hex

        # Construct the message to be signed
        message = f"{request_id}:{method}:{full_path_with_query}:{body}:"

        # Sign the message with the provided key
        def sign_message(key, message):
            c_key = ECC.import_key(
                f"-----BEGIN EC PRIVATE KEY-----\n{key}\n-----END EC PRIVATE KEY-----"
            )
            h = SHA256.new(message.encode("utf-8"))
            signer = DSS.new(c_key, "fips-186-3", encoding="der")
            signature = signer.sign(h)
            return base64.b64encode(signature)

        signature = sign_message(key, message)

        # Construct headers
        headers = {
            "rid": request_id,
            "name": name,
            "sign": signature.decode("utf-8"),
            "pubkey": public_key,
            "message": message,
        }
        return headers

    @classmethod
    def request(cls, method: str, path: str, params=None, data=None):
        """
        Synchronous request to the API.
        """
        if not cls._base_url:
            raise RuntimeError("SDK not initialized. Call `init()` first.")

        # Combine and normalize API prefix, path, and query parameters
        full_path_with_query = cls._normalize_path(cls._api_prefix, path, params)

        # Prepare the body and headers
        body = json.dumps(data) if data else ""
        headers = cls._generate_headers(method, full_path_with_query, body)

        # Construct the full URL for the request
        full_url = f"{cls._base_url}{full_path_with_query}"

        try:
            with httpx.Client() as client:
                response = client.request(method, full_url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP {e.response.status_code}: {e.response.text}") from e

    @classmethod
    async def async_request(cls, method: str, path: str, params=None, data=None):
        """
        Asynchronous request to the API.
        """
        if not cls._base_url:
            raise RuntimeError("SDK not initialized. Call `init()` first.")

        # Combine and normalize API prefix, path, and query parameters
        full_path_with_query = cls._normalize_path(cls._api_prefix, path, params)

        # Prepare the body and headers
        body = json.dumps(data) if data else ""
        headers = cls._generate_headers(method, full_path_with_query, body)

        # Construct the full URL for the request
        full_url = f"{cls._base_url}{full_path_with_query}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, full_url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP {e.response.status_code}: {e.response.text}") from e


class APIv1(BaseSDK):
    @classmethod
    def init(cls, access_key_file: str, base_url: str = "https://api.bitscrunch.com"):
        """
        Initialize SDK for API v1.
        """
        super().init(access_key_file, base_url, api_prefix="/api/v1")


class APIv2(BaseSDK):
    @classmethod
    def init(cls, access_key_file: str, base_url: str = "https://api.bitscrunch.com"):
        """
        Initialize SDK for API v2.
        """
        super().init(access_key_file, base_url, api_prefix="/api/v2")
