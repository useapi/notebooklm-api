from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from useapi_notebook import runner
from useapi_notebook.client import SETUP_ACCOUNT_URL, UseapiError


class NotebooklmUseapiProvider(ToolProvider):
    """Checks the useapi.net token with a cheap read call (GET /accounts, which does not call Google)."""

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            ctx = runner.make_context(credentials)
            accounts = ctx.get("accounts")
        except UseapiError as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
        if not isinstance(accounts, dict) or not accounts:
            raise ToolProviderCredentialValidationError(
                "The token works, but no Google account is connected to NotebookLM (Gemini Notebook) yet. "
                f"Connect one first: {SETUP_ACCOUNT_URL}"
            )
        if ctx.default_email and ctx.default_email not in accounts:
            raise ToolProviderCredentialValidationError(
                f"{ctx.default_email} is not a connected Google account. Connected: {', '.join(accounts)}. "
                f"Leave the email empty, or connect it at {SETUP_ACCOUNT_URL}"
            )
