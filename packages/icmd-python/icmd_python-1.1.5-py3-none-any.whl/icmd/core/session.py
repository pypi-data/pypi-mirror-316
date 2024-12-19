"""Session class to handle ICMD API requests."""

import json
import logging
import re
import socket
import socketserver
import webbrowser
from datetime import datetime, timedelta
from getpass import getpass
from http import HTTPStatus
from pathlib import Path

import requests.auth
from IPython.display import HTML, display

from .token_handler import TokenHandler

TOKEN_EXPIRE_BUFFER: timedelta = timedelta(milliseconds=5000)
CREDENTIAL_FILE = str(Path.home() / ".icmd_cred.json")

SIGN_IN_METHODS = {"SAML", "PASSWORD"}
AUTH_PORTS = [8001, 8002, 8003, 8004, 8005]

def _find_available_port(port_list: list) -> int:
    """Find the first available port from the predefined list."""
    for port in port_list:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No available ports found in the predefined list: {port_list}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Handle requests in a separate thread."""

    allow_reuse_address = True

class Session(requests.Session):
    """Wrapper around requests.Session that auto refresh token."""

    def __init__(self, jupyterlite: bool = False):
        super().__init__()
        self.api_version = "v1"

        self.sign_in_method: str = ""
        self.icmd_domain: str = ""
        self.username: str = ""
        self.password: str = ""
        self.mfa_code: str = ""
        self.auth_code: str = ""
        self.jupyterlite = jupyterlite

        self.refresh_token: str = ""
        self.id_token: str = ""
        self.id_token_expiration: datetime = datetime.utcnow()
        self.headers.update({"Content-Type": "application/json"})

        self._load_credential_file()
        if not jupyterlite:
            self._refresh_id_token()

    @property
    def api_root(self) -> str:
        """Return the root of the ICMD API, e.g., https://icmd.questek.com/api/v1."""
        if not self._is_valid_icmd_domain:
            self.icmd_domain = input("Your ICMD® domain (e.g., icmd.questek.com): ")
            if not self.icmd_domain.startswith("http"):
                self.icmd_domain = "https://" + self.icmd_domain
            self.sign_in_method = input(
                'If you use SSO, please enter "saml"; otherwise, leave empty: '
            )
            self.sign_in_method = self.sign_in_method.strip().upper()
            if self.sign_in_method == "":
                self.sign_in_method = "SAML"
            if self.sign_in_method not in SIGN_IN_METHODS:
                raise ValueError("Invalid sign-in method.")

        self._write_credential_file()
        return f"{self.icmd_domain}/api/{self.api_version}"

    def _load_credential_file(self) -> None:
        """Load icmd_domain and refresh_token from the CREDENTIAL_FILE."""
        if not Path(CREDENTIAL_FILE).is_file():
            return
        try:
            with open(CREDENTIAL_FILE) as file:
                data = json.load(file)
            self.icmd_domain = data.get("ICMD_DOMAIN", "")
            self.sign_in_method = data.get("ICMD_SIGN_IN_METHOD", "")
            self.refresh_token = data.get("ICMD_REFRESH_TOKEN", "")
        except OSError:
            logging.warning(f"Cannot open credential file: {CREDENTIAL_FILE}")
        except json.JSONDecodeError:
            logging.warning(f"Cannot decode credential file in JSON: {CREDENTIAL_FILE}")

    def _write_credential_file(self) -> None:
        """Write current values to the CREDENTIAL_FILE."""
        data = {
            "ICMD_DOMAIN": self.icmd_domain,
            "ICMD_SIGN_IN_METHOD": self.sign_in_method,
            "ICMD_REFRESH_TOKEN": self.refresh_token,
        }
        with open(CREDENTIAL_FILE, "w") as file:
            json.dump(data, file)

    @property
    def _is_valid_icmd_domain(self) -> bool:
        """Check if the given domain matches the pattern of ICMD domains."""
        if not self.icmd_domain.startswith("http"):
            self.icmd_domain = "https://" + self.icmd_domain
        if self.icmd_domain.endswith("server.questek.com"):
            return True
        if self.icmd_domain.startswith("https"):
            pattern = r"^https://(\w*.)?icmd\.questek\.com"
            return bool(re.match(pattern, self.icmd_domain))
        return self.icmd_domain.startswith("http")  # ignore local development

    @property
    def _is_id_token_expired(self):
        return self.id_token_expiration - TOKEN_EXPIRE_BUFFER <= datetime.utcnow()

    def _refresh_id_token(self) -> None:
        """Optionally refresh our id token."""
        url = f"{self.api_root}/account/auth/refresh/"
        response = self.request("post", url, json={"refreshToken": self.refresh_token})
        if response.status_code != HTTPStatus.OK:
            if self.sign_in_method.strip().upper() == "SAML":
                self._user_saml_sign_in()
            else:
                self._user_sign_in()
        else:
            self._handle_cookies(response)
            self._assign_tokens(response.json())

    def checked_request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Make a request to the ICMD API and handle token expiration."""
        clean_path = path.strip("/")
        if self._is_id_token_expired:
            self._refresh_id_token()

        url = f"{self.api_root}/{clean_path}/"
        response = self.request(method, url, **kwargs)

        if response.status_code == HTTPStatus.UNAUTHORIZED and response.reason == "Unauthorized":
            self._refresh_id_token()
            response = self.request(method, url, **kwargs)

        return response

    def _assign_tokens(self, auth: dict) -> None:
        """Assign tokens from auth response."""
        self.headers.update({"X-User-Context": auth.get("userFingerprint")})
        self.id_token = auth.get("idToken")
        if auth.get("refreshToken"):
            self.refresh_token = auth.get("refreshToken")
        self.id_token_expiration = datetime.fromisoformat(auth.get("expiresAt"))
        self.auth = BearerAuth(auth.get("idToken"))

    def _handle_cookies(self, response: requests.Response) -> None:
        """Handle cookies from response."""
        for cookie in response.cookies:
            if cookie.name == "Secure-Fgp":
                self.cookies.set("Secure-Fgp", cookie.value)

    def _mfa_sign_in(self, challenge, username, challenge_name) -> None:
        """Sign in with MFA code."""
        session = challenge["Session"]
        if not self.mfa_code:
            self.mfa_code = input("Your MFA Code: ")
        if username is None:
            username = input("Your ICMD® email: ")
        url = f"{self.api_root}/account/auth/mfa/"
        response = self.request(
            "post",
            url,
            json={
                "mfa_code": self.mfa_code,
                "session": session,
                "username": username,
                "challenge_name": challenge_name,
            },
        )
        if response.status_code != HTTPStatus.OK:
            raise ValueError(str(response.json()))
        self._handle_cookies(response)
        self._assign_tokens(response.json())

    def _handle_sign_in_response(self, username, response: requests.Response) -> None:
        """Handle response from login API endpoint."""
        if response.status_code != HTTPStatus.OK:
            raise ValueError("Cannot sign into ICMD®: " + str(response.json()))
        self._handle_cookies(response)
        auth = response.json()
        if auth and auth.get("challenge"):
            challenge = auth["challenge"]
            challenge_name = challenge.get("ChallengeName")
            if challenge_name in {"SOFTWARE_TOKEN_MFA", "SMS_MFA"}:
                self._mfa_sign_in(challenge, username, challenge_name)
            else:
                raise ValueError("Unknown challenge - " + challenge_name)
        else:
            self._assign_tokens(auth)

    def _user_sign_in(self):
        """Let user sign in with password to fetch a refresh token."""
        if not self.username:
            self.username = input("Your ICMD® email: ")
            self.password = getpass("Your ICMD® password: ")
            self.mfa_code = input("Your MFA Code (if enabled): ")

        try:
            url = f"{self.api_root}/account/auth/login/"
            response = self.request(
                "post", url, json={"username": self.username, "password": self.password}
            )
            self._handle_sign_in_response(self.username, response)
        except Exception as e:
            raise ValueError("Cannot sign into ICMD®: " + str(e)) from e

        self._write_credential_file()

    def _user_saml_sign_in(self):
        """Let user sign in with SAML to fetch a refresh token."""
        try:
            if self.jupyterlite:
                self._browser_env_saml_sign_in()
            else:
                print("\n\033[94mSigning into ICMD® with SAML SSO...\033[0m\n")

                LOCAL_PORT = _find_available_port(AUTH_PORTS)
                consent_login_url = f"{self.api_root}/account/auth/consent?redirect_uri=http://localhost:{LOCAL_PORT}/callback"

                print("\n\033[94mConsent granted. Proceeding with SSO authentication...\033[0m\n")

                print("Automatically opening the SSO authorization page in your default browser. "
                    "If it doesn't open or you prefer to use a different browser, "
                    "go to this URL:")

                print(f"\n{consent_login_url}\n")
                webbrowser.open(consent_login_url)

                # Start a local server to capture the auth_code
                with socketserver.TCPServer(("localhost", LOCAL_PORT), TokenHandler) as httpd:
                    httpd.handle_request()  # Wait for a single request, blocking
                    auth_code = httpd.auth_code
                    if not auth_code:
                        raise ValueError("Authentication code was not received.")

                login_url = f"{self.api_root}/account/auth/login/"
                response = self.request("post", login_url, json=
                    {
                        "code": auth_code,
                        "redirect_uri": f"http://localhost:{LOCAL_PORT}/callback"
                    })
                self._handle_sign_in_response(None, response)
                print("\n\033[92mSigned in successfully.\033[0m\n")
        except Exception as e:
            print("\nCannot sign into ICMD®: " + str(e) + "\n")
        finally:
            pass

    def _browser_env_saml_sign_in(self):
        """Show a button for signing in with SAML in JupyterLite."""
        try:
            # Create a sign-in button
            consent_login_url = f"{self.api_root}/account/auth/consent"
            buttomHTML = f"""
            <a type="button" href="{consent_login_url}" target="_blank">Sign in with SAML SSO</a>
            """
            display(HTML(buttomHTML))
        except Exception as e:
            print(f"\nCannot sign in: {e}\n")

    def complete_saml_sign_in(self):
        """Complete the SAML sign in process."""
        if not self.auth_code:
            print("\033[91mPlease enter an authorization code.\033[0m")
            return
        try:
            login_url = f"{self.api_root}/account/auth/login/"
            response = self.request("post", login_url, json={
                "code": self.auth_code,
                "redirect_uri": f"{self.api_root}/account/auth/exchange"
            })
            self._handle_sign_in_response(None, response)
            print("\n\033[92mSigned in successfully.\033[0m\n")
        except Exception as e:
            print(f"\n\033[91mError during sign in: {e!s}\033[0m\n")

    def jupyterlite_sign_in(self):
        """Sign in on JupyterLite."""
        if not self.icmd_domain or not self.sign_in_method:
            raise ValueError(
                "Please provide all following necessary information to sign in:\n"
                "session.icmd_domain = await input('icmd_domain'), e.g., icmd.questek.com\n"
                "session.sign_in_method = await input('sign_in_method'), e.g., PASSWORD or SAML\n"
            )

        if self.sign_in_method == "PASSWORD" and not all(
            [
                self.username,
                self.password,
                self.mfa_code,
            ]
        ):
            raise ValueError(
                "Please provide all following necessary information to sign in:\n"
                "session.username = await input('username'), i.e., your email\n"
                "session.password = await getpass('password'), i.e., your password\n"
                "session.mfa_code = await input('mfa_code'), i.e., the 6 digit code for MFA\n"
            )

        if self.sign_in_method == "SAML" and not all(
            [self.username]
        ):
            raise ValueError(
                "Please provide all following necessary information to sign in:\n"
                "session.username = await input('username'), i.e., your email\n"
            )
        self._refresh_id_token()

    @staticmethod
    def extract_code(url):
        """Extract authorization code from the url."""
        start = url.find("code=")
        if start == -1:
            return None
        start += len("code=")
        end = url.find(" ", start)
        if end == -1:
            end = len(url)
        return url[start:end]


class BearerAuth(requests.auth.AuthBase):
    """A lightweight Auth class to support Bearer token auth header."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an Authorization header to the given Request object."""
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
