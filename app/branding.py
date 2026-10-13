from typing import Any

_PROVIDER_NAME = "Zen Business Solutions"


def configure_branding(provider_name: str) -> None:
    global _PROVIDER_NAME
    if provider_name.strip():
        _PROVIDER_NAME = provider_name.strip()


def branded_response(data: dict[str, Any]):
    return {
        **data,
        "branding": {
            "provider": _PROVIDER_NAME,
            "powered_by": f"Powered by: {_PROVIDER_NAME}",
        },
    }
