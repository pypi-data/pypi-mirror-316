import click

from controller_main.controller_main_device_list import controller_main_device_list
from controller_main.controller_main_project_list import controller_main_project_list
from controller_main.controller_main_sms_record_list import controller_main_sms_record_list
from controller_main.controller_main_sms_report_list import controller_main_sms_report_list
from format_printer.printer_controller_main import printer_main_list


@click.group()
def cli_group():
    """CLI commands for SMS Backend Project"""

@click.command(name="controller-main-device")
@click.argument("action")
def controller_main_device(action):
    """Action of Main Controller Device. Supported operations[List]"""
    action = action.lower()
    if action == "list":
        data = controller_main_device_list()
        out = printer_main_list(data)
        click.echo(out)
    else:
        click.echo("controller_main_device")


@click.command(name="controller-main-project")
@click.argument("action")
def controller_main_project(action):
    """Action of Main Controller project. Supported operations[list]"""
    action = action.lower()
    if action == "list":
        data = controller_main_project_list()
        out = printer_main_list(data)
        click.echo(out)
    else:
        click.echo("controller_main_device")

@click.command(name="controller-main-sms")
@click.argument("module")
@click.option(
    "-a",
    "--action",
    help="Operations performed on the module",
)
def controller_main_sms(module, action):
    """Action of Main Controller SMS. Supported operations[list]"""
    module = module.lower()
    action = action.lower()
    if module == "report":
        if action == "list":
            data = controller_main_sms_report_list()
            out = printer_main_list(data)
            click.echo(out)
    elif module == "record":
        if action == "list":
            data = controller_main_sms_record_list()
            out = printer_main_list(data)
            click.echo(out)
    else:
        click.echo("controller_main_device")


cli_group.add_command(controller_main_device)
cli_group.add_command(controller_main_project)
cli_group.add_command(controller_main_sms)

if __name__ == '__main__':
    cli_group()