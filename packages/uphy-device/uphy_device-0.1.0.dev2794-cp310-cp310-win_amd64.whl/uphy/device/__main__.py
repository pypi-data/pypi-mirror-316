from contextlib import nullcontext
import faulthandler
import importlib.metadata
from typing import Optional, Annotated

import typer.rich_utils
from uphy.device import gui
from uphy.device import api
import logging
import typer
from pathlib import Path
from rich.logging import RichHandler
from rich.table import Table
from rich import print
import importlib.metadata
import importlib.util
import importlib.resources
import psutil
import upgen.model.uphy as uphy_model

from . import (
    get_device_handler,
    get_sample_model,
    DeviceError,
    run_client,
    run_client_and_server,
    run_server,
    Protocol,
    LOGGER,
)

from .server import mdns

faulthandler.enable()

app = typer.Typer(
    pretty_exceptions_enable=False,
    no_args_is_help=True,
    name="device",
    help="Run a U-Phy server from python.",
)


def _model_parser(path: Path) -> uphy_model.Root:
    try:
        return uphy_model.Root.parse_file(str(path))
    except Exception as exception:
        raise typer.BadParameter(str(exception)) from exception


def _interface_parser(interface: str) -> str:
    interfaces = psutil.net_if_addrs()
    if interface not in interfaces:
        raise typer.BadParameter(
            f"Interface '{interface}' not found in {list(interfaces)}"
        )
    return interface


INTERFACE_HELP = "The network interface to run the server on. NOTE: This should not be your main network card, but a secondary card used for protocol data."
INTERFACE_OPTION = typer.Option(
    help=INTERFACE_HELP,
    parser=_interface_parser,
    prompt="Enter network interface to use",
)
TRANSPORT_HELP = "The target transport to connect to the running server. 'tcp://' for network localhost access, '/dev/uphyX' or 'COMX') for serial connection to device."
MODEL_HELP = "Path to a U-Phy device model json file."
MODEL_OPTION = typer.Option(help=MODEL_HELP, parser=_model_parser)
HANDLER_HELP = "Path to custom device handler python script. A template file can be generated using 'uphy-device export-handler'."
MDNS_HELP = "Expose device and model for discovery over mdns/zeroconf, useful to use with a supported controller."


def _set_logging(level, force=False):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
        force=force,
    )


_set_logging(level=logging.INFO)


@app.command(no_args_is_help=True)
def client(
    protocol: Protocol,
    transport: Annotated[
        str,
        typer.Option(help=TRANSPORT_HELP),
    ],
    model: Annotated[Optional[uphy_model.Root], MODEL_OPTION] = None,
    verbose: bool = False,
    handler: Annotated[Optional[str], typer.Option(help=HANDLER_HELP)] = None,
    gui_arg: Annotated[gui.Gui, typer.Option("--gui")] = gui.Gui.dear,
):
    """Run a model from source XML file"""

    try:
        if verbose:
            _set_logging(level=logging.DEBUG, force=True)

        if model is None:
            model = get_sample_model()

        up = get_device_handler(protocol, model, handler)
        with up.gui(gui_arg):
            run_client(up, transport)

    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)
    except gui.GuiExit:
        pass


@app.command()
def mono(
    protocol: Protocol,
    interface: Annotated[
        str,
        INTERFACE_OPTION,
    ],
    model: Annotated[Optional[uphy_model.Root], MODEL_OPTION] = None,
    verbose: bool = False,
    handler: Annotated[Optional[str], typer.Option(help=HANDLER_HELP)] = None,
    gui_arg: Annotated[gui.Gui, typer.Option("--gui")] = gui.Gui.dear,
    run_mdns: Annotated[bool, typer.Option("--mdns", help=MDNS_HELP)] = False,
):
    """Run a client and server on same system."""
    try:
        if verbose:
            _set_logging(level=logging.DEBUG, force=True)

        if model is None:
            model = get_sample_model()

        if run_mdns:
            mdns_ctx = mdns.run(
                model=model,
                device=model.devices[0],
                interface=interface,
                protocol=protocol,
            )
        else:
            mdns_ctx = nullcontext()

        with mdns_ctx:
            up = get_device_handler(protocol, model, handler)
            with up.gui(gui_arg):
                run_client_and_server(up, interface)

    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)
    except gui.GuiExit:
        pass


@app.command()
def build():
    """Start building your device model"""

    print("To start building your device you need to create a model of your device describing its inputs and outputs.")
    print("This is done using RT-Labs device builder at https://devicebuilder.rt-labs.com/")
    print()
    print("After you have configured your model, download the model file into a known location")
    print()
    print()
    if typer.confirm(
        "Start a web browser navigating to this location?"
    ):
        typer.launch("https://devicebuilder.rt-labs.com/")


@app.command()
def export_handler(file: Annotated[typer.FileBinaryWrite, typer.Argument(mode="xb")]):
    """Export a template handler to file"""
    with importlib.resources.open_binary(__package__, "handler.py") as template:
        file.write(template.read())


@app.command()
def server(
    interface: Annotated[
        str,
        INTERFACE_OPTION,
    ],
):
    """Start a u-phy server on your local system. This will listen to connections from client instances to run the u-phy system."""
    try:
        run_server(interface)
    except (DeviceError, api.ApiError) as exception:
        LOGGER.error(str(exception))
        LOGGER.debug("", exc_info=True)


@app.command()
def discover():
    """Tries to discovery locally attached u-phy servers"""
    import serial.tools.list_ports

    table = Table("ID", "Serial Number", "Subsystem", title="Serial ports")
    for port in serial.tools.list_ports.comports():
        print(port.usb_info())
        if port.vid != 0x04D8 or port.pid != 0x1301:
            continue
        index = port.location.split(".")[-1]
        if index == "0":
            system = "server"
        elif index == "2":
            system = "console"
        else:
            system = "unkown"
        table.add_row(port.name, port.serial_number, system)

    print(table)


@app.command()
def readme():
    print("The main documentation site for U-Phy is located at https://docs.rt-labs.com/u-phy.")
    if typer.confirm(
        "Start a web browser navigating to site?"
    ):
        typer.launch("https://docs.rt-labs.com/u-phy")


if __name__ == "__main__":
    app()
