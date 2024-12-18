"""The local Reflex agent."""

import importlib
import inspect
from pathlib import Path
import types
from types import FunctionType

import reflex as rx
import sys

from reflex_ai import paths
from reflex_ai.utils import path_utils

from reflex_ai.selection import ClickSelectionState
from reflex_ai.runtime import RunTimeState


class EditableState(rx.State):
    """Rewrite rx.State imports in copied modules to this new class to avoid conflicts."""

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the state.

        Returns:
            The name of the state.
        """
        module = cls.__module__.replace(".", "___")
        return rx.utils.format.to_snake_case(f"Editable___{module}___{cls.__name__}")


def enable(app: rx.App):
    """Enable the agent on an app.

    Args:
        app: The app to enable the agent on.

    Note:
        For now, this must be called before add_page is called as
        we override the add_page method.

    Raises:
        Exception: If watchfiles is installed
    """
    from reflex.utils.exec import is_prod_mode
    from reflex_cli.v2 import cli as hosting_cli

    # Ensure that user logs in before using the app.
    hosting_cli.login()

    # Skip if in production mode.
    if is_prod_mode():
        return

    from .selection import clickable
    from .playground import playground

    # The base path is the directory where the app is defined.
    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename

    # We care about the main directory, where the files live, and the parent directory, where .web lives
    base_paths = [Path(caller_path).parent, Path(caller_path).parent.parent]

    # Skip if the base path is a temporary directory.
    if path_utils.SCRATCH_DIR_NAME in str(base_paths[0]):
        return

    if importlib.util.find_spec("watchfiles") is not None:
        raise Exception(
            "It looks like you have watchfiles installed. The AI toolbar will not work correctly; it is recommended you uninstall it first. To do this, run `pip uninstall watchfiles'"
        )

    paths.base_paths = base_paths

    tmp_root_path = path_utils.create_scratch_dir(base_paths[0])
    paths.tmp_root_path = tmp_root_path
    filename = tmp_root_path / base_paths[0].name / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "tmp" + base_paths[0].name,
        filename,
    )
    new_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_module)
    sys.modules["tmp" + base_paths[0].name] = new_module

    def add_page(self, component, *args, **kwargs):
        # Skip if the component is not a function.
        if not isinstance(component, FunctionType):
            return
        # Add the page normally.
        route = kwargs.pop("route", rx.utils.format.format_route(component.__name__))
        rx.App.add_page(self, component, *args, route=route, **kwargs)

        # Determine which module the component came from
        module = inspect.getmodule(component)
        if module is None:
            # Skip if the component does not come from a known module.
            return

        # Get the scratch module path.
        module_path = inspect.getfile(component)
        new_module_path = Path(
            module_path.replace(str(base_paths[0].parent), str(tmp_root_path))
        )
        spec = importlib.util.spec_from_file_location(
            "tmp" + module.__name__,
            new_module_path,
        )
        new_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(new_module)

        # Add the page on the edit route.
        rx.App.add_page(
            self,
            clickable(base_paths=base_paths)(
                lambda: playground(getattr(new_module, component.__name__))
            ),
            route=f"/{route}/edit" if route != "index" else "/edit",
            on_load=[
                RunTimeState.reset_scratch_dir(base_paths[0]),
                ClickSelectionState.click_page(
                    new_module_path, component.__name__
                ).prevent_default.stop_propagation,
            ],
        )

    def add_page2(self, component, *args, **kwargs):
        pass

    if "reflex_ai_tmp" in caller_path:
        app.add_page = types.MethodType(add_page2, app)

    app.add_page = types.MethodType(add_page, app)
