from __future__ import annotations

import importlib
import importlib.util
import inspect
import logging
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

logger = logging.getLogger("zenmcp.tool_loader")


def _call_registration(fn: Callable[..., Any], context: dict[str, Any]) -> None:
    """Invoke a registration function by matching its parameter names to context."""
    signature = inspect.signature(fn)
    kwargs: dict[str, Any] = {}
    aliases = {
        "server": "mcp",
        "mcp_server": "mcp",
        "client": "odoo",
        "odoo_client": "odoo",
        "config": "settings",
    }

    for name, parameter in signature.parameters.items():
        key = aliases.get(name, name)
        if key in context:
            kwargs[name] = context[key]
        elif parameter.default is inspect.Parameter.empty:
            raise TypeError(
                f"Cannot register {fn.__module__}.{fn.__name__}: "
                f"unsupported required parameter '{name}'."
            )

    fn(**kwargs)


def _registration_functions(module: ModuleType) -> list[Callable[..., Any]]:
    explicit = getattr(module, "register_tools", None)
    if callable(explicit):
        return [explicit]

    functions: list[Callable[..., Any]] = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if obj.__module__ != module.__name__:
            continue
        if name.startswith("register_") and name.endswith("_tools"):
            functions.append(obj)
    return functions


def _load_module_from_file(path: Path, namespace: str) -> ModuleType:
    module_name = f"zenmcp_external.{namespace}.{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _iter_package_modules(package_name: str):
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        return

    if not hasattr(package, "__path__"):
        return

    for info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        yield importlib.import_module(info.name)


def register_dynamic_tools(
    *,
    mcp,
    odoo,
    settings,
    failed,
) -> list[str]:
    """
    Dynamically load tools from:
      1. app.tools (the Peltier tool set)
      2. app.addons
      3. app.custom_addons
      4. ADDONS_PATH directories from the environment

    An addon module may expose either:
      - register_tools(...), or
      - one or more register_*_tools(...) functions.

    Supported injectable parameter names: mcp/server/mcp_server, odoo/client/
    odoo_client, settings/config, failed.
    """
    context = {
        "mcp": mcp,
        "odoo": odoo,
        "settings": settings,
        "failed": failed,
    }
    registered: list[str] = []
    seen_functions: set[tuple[str, str]] = set()

    modules: list[ModuleType] = []
    for package_name in ("app.tools", "app.addons", "app.custom_addons"):
        modules.extend(list(_iter_package_modules(package_name) or []))

    for raw_path in settings.addons_path:
        root = Path(raw_path).expanduser().resolve()
        if not root.exists():
            logger.warning("ADDONS_PATH does not exist: %s", root)
            continue
        for file_path in sorted(root.rglob("*.py")):
            if file_path.name.startswith("_"):
                continue
            namespace = str(abs(hash(str(file_path.parent))))
            modules.append(_load_module_from_file(file_path, namespace))

    for module in modules:
        for fn in _registration_functions(module):
            key = (fn.__module__, fn.__name__)
            if key in seen_functions:
                continue
            seen_functions.add(key)
            _call_registration(fn, context)
            qualified = f"{fn.__module__}.{fn.__name__}"
            registered.append(qualified)
            logger.info("Loaded MCP tool registration: %s", qualified)

    return registered
