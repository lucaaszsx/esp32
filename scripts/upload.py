import sys

from common import Colors, print_format
from InquirerPy.base.control import Choice
from InquirerPy.prompts.confirm import ConfirmPrompt as confirm
from InquirerPy.prompts.list import ListPrompt as select
from pio import pio_call, pio_load_conf
from serial.tools import list_ports


def main():
    directory = sys.argv[1]
    conf = pio_load_conf(directory)

    command = ["run", "-t", "upload"]

    envs = [name.removeprefix("env:") for name, _ in conf if name.startswith("env:")]

    if len(envs) == 0:
        print_format(Colors.YELLOW, "No specific environment detected in config, skipping env selection")
    else:
        env = select(message="Which environment?", choices=envs).execute()
        command += ["-e", env]

    use_monitor = confirm(message="Start monitor?", default=False).execute()
    same_port = False

    if use_monitor:
        command += ["-t", "monitor"]
        same_port = confirm(message="Use same port for both monitor and upload?", default=True).execute()

    ports = [
        port
        for port in list_ports.comports()
        if port.vid is not None and port.pid is not None
    ]
    port_choices = [Choice(value=p.device, name=f"{p.device} - {p.description}") for p in ports]

    if len(ports) == 0:
        print_format(Colors.YELLOW, "No valid active ports found, PlatformIO will try to infer at upload")
    else:
        upload_port = select(
            message="Which port for upload?",
            choices=port_choices,
            default=None
        ).execute()

        if use_monitor and same_port:
            command += ["-p", upload_port]
        elif use_monitor and not same_port:
            monitor_port = select(message="Which port for monitor?", choices=port_choices, default=None).execute()
            command += [
                "--upload-port", upload_port,
                "--monitor-port", monitor_port
            ]
        elif not use_monitor:
            command += ["--upload-port", upload_port]

    print_format(Colors.BLUE, f"The following command will be executed: {" ".join(command)}")

    proceed = confirm(message="Proceed upload?", default=True).execute()
    if not proceed:
        print_format(Colors.YELLOW, "Aborted")
        sys.exit(0)

    exit_code = pio_call(directory, command)

    print()
    print_format(Colors.GREEN, "Done.")

    return exit_code

if __name__ == "__main__":
    main()
