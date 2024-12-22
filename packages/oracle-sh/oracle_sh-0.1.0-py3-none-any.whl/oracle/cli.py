from typing import Callable, Optional

import typer
from typing_extensions import Annotated

from oracle.controller import Controller, ControllerError

app = typer.Typer()
controller = Controller()
