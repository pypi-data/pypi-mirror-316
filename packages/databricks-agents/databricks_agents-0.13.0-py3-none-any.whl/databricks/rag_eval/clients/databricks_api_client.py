"""
Base class for concrete clients to various Databricks APIs
"""

import abc
from typing import Dict, Optional

import jinja2
import requests
from requests import adapters, auth
from urllib3.util import retry

_WORKSPACE_ACCESS_TOKEN_MAX_RETRIES = 3


def get_default_workspace_access_token_retry_config():
    """Get the default retry config for calls to get the workspace access token."""
    retry.Retry(
        total=_WORKSPACE_ACCESS_TOKEN_MAX_RETRIES,
        # There's no API reference for the endpoint, so we use a default set of status codes
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(
            ["GET", "POST"]
        ),  # by default, it doesn't retry on POST
    )


class DatabricksAPIClient(abc.ABC):
    """
    This is a base client to talk to Databricks API. The child classes of this base client can use the `get_auth()`
    and `get_request_session()` methods provided by `DatabricksAPIClient` to send request to the
    corresponding Databricks API.

    Example Usage:

    class MyClient(DatabricksAPIClient):
      def __init__(self, api_url: str, api_token: str):
        super().__init__(api_url=api_url, api_token=api_token, version="2.1")

      def send_request(self):
        with self.get_request_session() as s:
            resp = s.post(self.get_method_url("list"), json="request_body: {...}", auth=self.get_auth())
        self.process_response(resp)
    """

    def __init__(
        self,
        version: str,
        api_url: str,
        api_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """
        :param api_url: The url that can be used to talk to the workspace,
                        e.g. "https://oregon.staging.cloud.databricks.com".
        :param api_token: Token for authentication
        :param client_id: Client ID for authentication
        :param client_secret: Client secret for authentication
        :param version: The version of the Databricks API, e.g. "2.1", "2.0".
        """
        self._api_url = api_url
        self._client_id = client_id
        self._client_secret = client_secret
        assert api_token or (client_id and client_secret), (
            "Insufficient authentication provided. Please either set `DATABRICKS_TOKEN` to a valid"
            " PAT token or set `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET` to a valid"
            " secret."
        )

        # Databricks documentation recommends not using token-based authentication:
        # https://docs.databricks.com/en/dev-tools/auth/pat.html#databricks-personal-access-token-authentication
        workspace_access_token = self.get_workspace_access_token()
        self._api_token = (
            workspace_access_token if workspace_access_token is not None else api_token
        )

        self._version = version
        self._base_api_url = f"api/{version}"

    def get_workspace_access_token(self) -> Optional[str]:
        """
        Returns the workspace-level access token
        :return: Workspace access token if client ID and client secret are specified
        """
        if not self._client_id or not self._client_secret:
            return None

        token_endpoint_url = f"{self._api_url}/oidc/v1/token"
        request_data = {
            "grant_type": "client_credentials",
            "scope": "all-apis",
        }

        with DatabricksAPIClient.get_request_session(
            get_default_workspace_access_token_retry_config()
        ) as session:
            resp = session.post(
                token_endpoint_url,
                data=request_data,
                auth=auth.HTTPBasicAuth(self._client_id, self._client_secret),
            )

        if resp.status_code == requests.codes.ok:
            return resp.json().get("access_token", None)
        else:
            try:
                resp.raise_for_status()
            except requests.HTTPError as e:
                raise Exception(
                    f"Failed to get workspace access token from client ID and secret: {e}"
                ) from e

    def get_parameterized_method_path(
        self,
        method_template: str,
        method_path_params: Dict[str, str],
        endpoint: str,
        is_preview: bool = False,
    ):
        """
        Returns the path to invoke a specific method

        :param method_template: Jinja template of the method path
        :param method_path_params: Parameters for rendering the method path jinja template
        :param endpoint: Endpoint to construct base url, e.g. "workspace", "jobs".
        :param is_preview: Whether to use the preview path identifier
        """
        method_path = (
            jinja2.Template(method_template).render(method_path_params).lstrip("/")
        )
        return f"{'preview/' if is_preview else ''}{endpoint}/{method_path}"

    def get_method_url(self, method_path: str):
        """
        Returns the URL to invoke a specific method. This is a concatenation of the workspace url + the
        corresponding method path.

        :param method_path: The method path
        """
        return f"{self._api_url}/{self._base_api_url}/{method_path.lstrip('/')}"

    def get_auth(self):
        """
        Get authentication for requests.
        """
        return self.BearerAuth(self._api_token)

    @classmethod
    def get_request_session(
        cls, max_retries: retry.Retry | int | None = adapters.DEFAULT_RETRIES
    ) -> requests.Session:
        """
        Creates a request session with a retry mechanism.

        :return: Session object.
        """
        adapter = adapters.HTTPAdapter(max_retries=max_retries)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def get_default_request_session(
        self,
        retry_config: Optional[retry.Retry] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Session:
        """
        Creates a request session with a retry mechanism, headers, and default authentication
        :return: Session object.
        """
        session = self.get_request_session(retry_config)
        session.headers.update(headers)
        session.auth = self.get_auth()
        return session

    class BearerAuth(auth.AuthBase):
        """Bearer Authentication class which holds tokens for talking with Databricks API."""

        def __init__(self, token: str):
            self._token = token

        def __call__(self, r):
            r.headers["authorization"] = f"Bearer {self._token}"
            return r
