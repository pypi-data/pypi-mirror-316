import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import rich_click as click
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich import box
    from thunder import auth
    import os
    from os.path import join
    import json
    from scp import SCPClient, SCPException
    import paramiko
    import subprocess
    import time
    import platform
    from contextlib import contextmanager
    from threading import Timer

    from thunder import utils
    from thunder.get_latest import get_latest

    try:
        from importlib.metadata import version
    except Exception as e:
        from importlib_metadata import version

    import requests
    from packaging import version as version_parser


PACKAGE_NAME = "tnr"
ENABLE_RUN_COMMANDS = True if platform.system() == "Linux" else False
INSIDE_INSTANCE = False
INSTANCE_ID = None
OPEN_PORTS = {
    'comfy-ui': 8188,
    'ollama': 8080,
}


# Remove the DefaultCommandGroup class
DISPLAYED_WARNING = False
logging_in = False

@contextmanager
def DelayedProgress(*progress_args, delay=0.4, **progress_kwargs):
    progress = Progress(*progress_args, **progress_kwargs)
    timer = Timer(delay, progress.start)
    timer.start()
    try:
        yield progress
        timer.cancel()
        if progress.live.is_started: progress.stop()
    finally:
        timer.cancel()
        if progress.live.is_started: progress.stop()

def get_token():
    global logging_in, DISPLAYED_WARNING

    if "TNR_API_TOKEN" in os.environ:
        return os.environ["TNR_API_TOKEN"]

    token_file = auth.get_credentials_file_path()
    if not os.path.exists(token_file):
        logging_in = True
        auth.login()

    with open(auth.get_credentials_file_path(), "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            token = lines[0].strip()
            return token

    auth.logout()
    logging_in = True
    token = auth.login()
    return token


def init():
    global INSIDE_INSTANCE, INSTANCE_ID, ENABLE_RUN_COMMANDS

    if not ENABLE_RUN_COMMANDS:
        utils.setup_config(get_token())
        config = utils.read_config()
    else:
        config = {}

    deployment_mode = config.get("deploymentMode", "public")

    if deployment_mode == "public":
        if ENABLE_RUN_COMMANDS:
            utils.setup_instance(get_token())

        # Determine if we are currently in a TC instance
        INSTANCE_ID = utils.get_instance_id(get_token())
        if INSTANCE_ID == -1:
            exit(1)

        INSIDE_INSTANCE = INSTANCE_ID is not None
        if INSIDE_INSTANCE:
            utils.enable_default_tnr_activate()

    elif deployment_mode == "on-prem":
        pass

    elif deployment_mode == "test":
        ENABLE_RUN_COMMANDS = True
        INSTANCE_ID = 0

    else:
        raise click.ClickException(
            "deploymentMode field in `~/.thunder/config.json` is set to an invalid value"
        )


init()

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.COMMAND_GROUPS = {
    "cli": [
        (
            {
                "name": "Instance management",
                "commands": ["create", "delete", "start", "stop"],
            }
            if not INSIDE_INSTANCE
            else {}
        ),
        (
            {
                "name": "Shell management",
                "commands": ["activate", "deactivate"],
            } if ENABLE_RUN_COMMANDS else {}
        ),
        {
            "name": "Utility",
            "commands": (
                ["device", "status", "scp"]
                if INSIDE_INSTANCE
                else ["connect", "status", "scp", "resize"]
            ),
        },
        (
            {
                "name": "Account management",
                "commands": ["login", "logout"],
            }
            if not INSIDE_INSTANCE
            else {}
        ),
    ]
}

COLOR = "green" if INSIDE_INSTANCE else "cyan"
click.rich_click.STYLE_OPTION = COLOR
click.rich_click.STYLE_COMMAND = COLOR

main_message = (
    f":link: [bold {COLOR}]You're connected to a Thunder Compute instance. Any process you run will automatically use a GPU on-demand.[/]"
    if INSIDE_INSTANCE
    else f":laptop_computer: [bold {COLOR}]You're in a local environment, use these commands to manage your Thunder Compute instances.[/]"
)


@click.group(
    cls=click.RichGroup,
    help=main_message,
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.version_option(version=version(PACKAGE_NAME))
def cli():
    meets_version, versions = does_meet_min_required_version()
    if not meets_version:
        raise click.ClickException(
            f'Failed to meet minimum required tnr version to proceed (current=={versions[0]}, required=={versions[1]}), please run "pip install --upgrade tnr" to update'
        )
    utils.validate_config()

# @click.group(
#     cls=click.RichGroup,
#     help=main_message,
#     context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
# )
# @click.version_option(version=version(PACKAGE_NAME))
# @click.pass_context
# def cli(ctx):
#     ctx.start_time = time.time()
    
#     meets_version, versions = does_meet_min_required_version()
#     if not meets_version:
#         raise click.ClickException(
#             f'Failed to meet minimum required tnr version to proceed (current=={versions[0]}, required=={versions[1]}), please run "pip install --upgrade tnr" to update'
#         )
#     utils.validate_config()
    
#     # Add CLI initialization timing
#     cli_init_time = time.time()
    
#     # Store the initialization end time for command timing
#     ctx.init_end_time = cli_init_time
    
#     # Create a callback that includes the context
#     ctx.call_on_close(lambda: print_execution_time(ctx))

# def print_execution_time(ctx):
#     end_time = time.time()
#     # Calculate total execution time from click config
#     total_execution_time = end_time - ctx.start_time
#     # Calculate command execution time     
#     print(f"⏱️ Total execution time: {total_execution_time:.2f}s")

if ENABLE_RUN_COMMANDS:

    @cli.command(
        help="Runs process on a remote Thunder Compute GPU. The GPU type is specified in the ~/.thunder/dev file. For more details, please go to thundercompute.com",
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
        hidden=True,
    )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    @click.option("--nowarnings", is_flag=True, help="Hide warning messages")
    def run(args, nowarnings):
        if not args:
            raise click.ClickException("No arguments provided. Exiting...")

        token = get_token()
        uid = utils.get_uid(token)

        # Run the requested process
        if not INSIDE_INSTANCE and not nowarnings:
            message = "[yellow]Attaching to a remote GPU from a non-managed instance - this will hurt performance. If this is not intentional, please connect to a managed CPU instance using tnr create and tnr connect <INSTANCE ID>[/yellow]"
            panel = Panel(
                message,
                title=":warning:  Warning :warning: ",
                title_align="left",
                highlight=True,
                width=100,
                box=box.ROUNDED,
            )
            rich.print(panel)

        config = utils.read_config()
        if "binary" in config:
            binary = config["binary"]
            if not os.path.isfile(binary):
                raise click.ClickException(
                    "Invalid path to libthunder.so in config.binary"
                )
        else:
            binary = get_latest("client", "~/.thunder/libthunder.so")
            if binary == None:
                raise click.ClickException("Failed to download binary")

        device = config.get("gpuType", "t4")

        os.environ["SESSION_USERNAME"] = uid
        os.environ["TOKEN"] = token
        os.environ["__TNR_RUN"] = "true"
        if device.lower() != "cpu":
            os.environ["LD_PRELOAD"] = f"{binary}"

        # This should never return
        try:
            os.execvp(args[0], args)
        except FileNotFoundError:
            raise click.ClickException(f"Invalid command: \"{' '.join(args)}\"")
        except Exception as e:
            raise click.ClickException(f"Unknown exception: {e}")

    @cli.command(
        help="If device_type is empty, displays the current GPU and a list of available GPUs. If device_name has a value, switches to the specified device. Input billing information at console.thundercompute.com to use devices besides NVIDIA T4s",
        hidden=not INSIDE_INSTANCE,
    )
    @click.argument("device_type", required=False)
    @click.option("-n", "--ngpus", type=int, help="Number of GPUs to use")
    @click.option("--raw", is_flag=True, help="Output raw device information")
    def device(device_type, ngpus, raw):
        config = utils.read_config()
        supported_devices = set(
            [
                "cpu",
                "t4",
                "v100",
                "a100",
                "l4",
                "p4",
                "p100",
                "h100",
            ]
        )

        if device_type is None:
            # User wants to read current device
            device = config.get("gpuType", "t4")
            gpu_count = config.get("gpuCount", 1)

            if raw is not None and raw:
                if gpu_count <= 1:
                    click.echo(device.upper())
                else:
                    click.echo(f"{gpu_count}x{device.upper()}")
                return

            if device.lower() == "cpu":
                click.echo(
                    click.style(
                        "📖 No GPU selected - use `tnr device <gpu-type>` to select a GPU",
                        fg="white",
                    )
                )
                return

            console = Console()
            if gpu_count == 1:
                console.print(f"[bold green]📖 Current GPU:[/] {device.upper()}")
            else:
                console.print(
                    f"[bold green]📖 Current GPUs:[/][white] {gpu_count} x {device.upper()}[/]"
                )

            utils.display_available_gpus()
            return

        if device_type.lower() not in supported_devices:
            raise click.ClickException(
                f"Unsupported device type: {device_type}. Please select one of CPU, T4, V100, A100, L4, P4, P100, or H100"
            )

        if ngpus is not None and ngpus < 1:
            raise click.ClickException(
                f"Unsupported device count {ngpus} - must be at least 1"
            )

        if device_type.lower() == "cpu":
            config["gpuType"] = "cpu"
            config["gpuCount"] = 0

            click.echo(
                click.style(
                    f"✅ Device set to CPU, you are now disconnected from any GPUs",
                    fg="green",
                )
            )
        else:
            config["gpuType"] = device_type.lower()

            gpu_count = ngpus if ngpus is not None else 1
            config["gpuCount"] = gpu_count
            click.echo(
                click.style(
                    f"✅ Device set to {gpu_count} x {device_type.upper()}", fg="green"
                )
            )
        utils.write_config(config)

    @cli.command(
        help="Activate a tnr shell environment. Once activated, everything will automatically run on a remote GPU",
        hidden=not ENABLE_RUN_COMMANDS,
    )
    def activate():
        pass

    @cli.command(
        help="Deactivate a tnr environment",
        hidden=not ENABLE_RUN_COMMANDS,
    )
    def deactivate():
        pass

else:

    @cli.command(hidden=True)
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def run(args):
        raise click.ClickException(
            "tnr run is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
        )

    @cli.command(hidden=True)
    @click.argument("device_type", required=False)
    @click.option("-n", "--ngpus", type=int, help="Number of GPUs to use")
    @click.option("--raw", is_flag=True, help="Output raw device information")
    def device(device_type, ngpus, raw):
        raise click.ClickException(
            "tnr device is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
        )


@cli.command(hidden=True)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def launch(args):
    return run(args)
if INSIDE_INSTANCE:
    @cli.command(
        help="Lists details of your current Thunder Compute instance and any actively running GPU processes"
    )
    def status():
        with DelayedProgress(
            SpinnerColumn(spinner_name="dots", style="white"),
            TextColumn("[white]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("Loading", total=None)  # No description text

            token = get_token() 

        # Retrieve IP address and active sessions in one call
            current_ip, active_sessions = utils.get_active_sessions(token)

            # Extract storage information
            storage_total = (
                subprocess.check_output("df -h / | awk 'NR==2 {print $2}'", shell=True)
                .decode()
                .strip()
            )
            storage_used = (
                subprocess.check_output("df -h / | awk 'NR==2 {print $3}'", shell=True)
                .decode()
                .strip()
            )

            disk_space_text = Text(
                f"Disk Space: {storage_used} / {storage_total} (Used / Total)", 
                style="white"
            )

            # Format INSTANCE_ID and current_ip as Text objects with a specific color (e.g., white)
            instance_id_text = Text(f"ID: {INSTANCE_ID}", style="white")
            current_ip_text = Text(f"Public IP: {current_ip}", style="white")

        # Console output for instance details
        console = Console()
        console.print(Text("Instance Details", style="bold green"))
        console.print(instance_id_text)
        console.print(current_ip_text)
        console.print(disk_space_text)
        console.print()

        # GPU Processes Table
        gpus_table = Table(
            title="Active GPU Processes",
            title_style="bold green",
            title_justify="left",
            box=box.ROUNDED,
        )

        gpus_table.add_column("GPU Type", justify="center")
        gpus_table.add_column("Duration", justify="center")

        # Populate table with active sessions data
        for session_info in active_sessions:
            gpus_table.add_row(
                f'{session_info["count"]} x {session_info["gpu"]}',
                f"{session_info['duration']}s",
            )

        # If no active sessions, display placeholder
        if not active_sessions:
            gpus_table.add_row("--", "--")

        # Print table
        console.print(gpus_table)

else:

    @cli.command(
        help="Lists details of Thunder Compute instances associated with your account"
    )
    def status():
        with DelayedProgress(
            SpinnerColumn(spinner_name="dots", style="white"),
            TextColumn("[white]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task("Loading", total=None)  # No description text

            token = get_token()
            success, error, instances = utils.get_instances(token)
            if not success:
                raise click.ClickException(f"Status command failed with error: {error}")

            instances_table = Table(
                title="Thunder Compute Instances",
                title_style="bold cyan",
                title_justify="left",
                box=box.ROUNDED,
            )

        instances_table.add_column("ID", justify="center")
        instances_table.add_column("Status", justify="center")
        instances_table.add_column("Address", justify="center")
        instances_table.add_column("Disk Size", justify="center")
        instances_table.add_column("CPU Cores", justify="center")
        instances_table.add_column("RAM", justify="center")
        instances_table.add_column("Creation Date", justify="center")

        for instance_id, metadata in instances.items():
            # Set status color based on status
            if metadata["status"] == "RUNNING":
                status_color = "green"
            elif metadata["status"] == "STOPPED":
                status_color = "red"
            else:
                status_color = "yellow"

            # Handle missing IP addresses
            ip_entry = metadata["ip"] if metadata["ip"] else "--"

            # Convert all entries to strings to avoid NotRenderableError
            instances_table.add_row(
                str(instance_id),
                Text(metadata["status"], style=status_color),
                str(ip_entry),
                f"{metadata['storage']}GB",
                str(metadata['cpuCores']),
                f"{int(metadata['cpuCores'])*4}GB",
                str(metadata["createdAt"]),
            )

        console = Console()

        # If there are no instances, display placeholders
        if len(instances) == 0:
            instances_table.add_row("--", "--", "--", "--", "--")

        console.print(instances_table)

        if len(instances) == 0:
            console.print("Tip: use `tnr create` to create a Thunder Compute instance")

@cli.command(
    help="Create a new Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
@click.option('--cores', type=click.Choice(['4', '8', '16']), default='4', help='Number of CPU cores to create the instance with')
@click.option('--template', type=click.Choice(['base', 'comfy-ui', 'ollama']), default='base', help='Template to create client instance with')
def create(cores, template):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        success, error = utils.create_instance(token, cores, template)
    if success:
        click.echo(
            click.style(
                "Successfully created a Thunder Compute instance! View this instance with 'tnr status'",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to create Thunder Compute instance: {error}"
        )


@cli.command(
    help="Permanently deletes a Thunder Compute instance. This action is not reversible",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def delete(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        success, error = utils.delete_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully deleted Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )

        utils.remove_instance_from_ssh_config(f"tnr-{instance_id}")
    else:
        raise click.ClickException(
            f"Failed to delete Thunder Compute instance {instance_id}: {error}"
        )
    
@cli.command(
    help="Increases the disk size of a Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
@click.argument("new_size", required=True, type=int)
def resize(instance_id, new_size):
    
    if new_size > 1024:
        raise click.ClickException(
            f"❌ The requested size ({new_size}GB) exceeds the 1TB limit."
        )
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None) 
        token = get_token()
        success, error, instances = utils.get_instances(token)
        if not success:
            raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")

        metadata = instances.get(instance_id)
        if not metadata or metadata["ip"] is None:
            raise click.ClickException(
                f"Instance {instance_id} is not available to connect or has no valid IP."
            )

    ip = metadata["ip"]
    keyfile = utils.get_key_file(metadata["uuid"])
    if not os.path.exists(keyfile):
        if not utils.add_key_to_instance(instance_id, token):
            raise click.ClickException(
                f"Unable to find or create SSH key file for instance {instance_id}."
            )

    # Step 1: Establish SSH connection with retries
    start_time = time.time()
    connection_successful = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while time.time() - start_time < 60:
        try:
            ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
            connection_successful = True
            break
        except Exception:
            time.sleep(5)  # Brief wait before retrying

    if not connection_successful:
        raise click.ClickException(
            "Failed to connect to the Thunder Compute instance within a minute. Please retry this command or contact support@thundercompute.com if the issue persists."
        )

    # Step 2: Get current disk size using SSH
    current_size = utils.get_current_disk_size_ssh(ssh)
    if current_size is None:
        click.echo(click.style("❌ Unable to retrieve the current disk size.", fg="red"))
        ssh.close()
        return

    # Step 3: Check if resizing is needed
    if current_size >= new_size:
        click.echo(click.style(
            f"❌ The current disk size ({current_size}GB) is already greater than or equal to the requested size ({new_size}GB). No resize needed.",
            fg="yellow"
        ))
        ssh.close()
        return

    # Step 3.5: Verify that user wants to resize disk
    message = "[yellow]This action cannot be undone, persistent disk size can only be increased.[/yellow]"
    panel = Panel(
        message,
        title=":warning:  Warning :warning: ",
        title_align="left",
        highlight=True,
        width=100,
        box=box.ROUNDED,
    )
    rich.print(panel)
    if not click.confirm("Would you like to continue?"):
        click.echo(
            click.style(
            "The operation has been cancelled. No changes to the instance have been made.",
            fg="cyan",
            )
        )
        return
    
    # Step 4: Resize the disk
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading, this may take a minute", total=None)  # No description text
        success, error = utils.resize_instance(instance_id, new_size, token)
        if success:
            _, stdout, stderr = ssh.exec_command("""
                sudo apt install -y cloud-guest-utils
                sudo growpart /dev/sda 1
                sudo resize2fs /dev/sda1
            """)
            # Wait for standard output, otherwise this won't complete correctly
            stdout.read().decode()
            stderr.read().decode()
        
        ssh.close()

    if success:
        click.echo(
            click.style(
                f"Successfully resized the persistent disk for instance {instance_id} to {new_size}GB.",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to resize the persistent disk on Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Starts a stopped Thunder Compute instance",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def start(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        success, error = utils.start_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully started Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to start Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Stops a running Thunder Compute instance. Stopped instances have persistent storage and can be restarted at any time",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def stop(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        success, error = utils.stop_instance(instance_id, token)
    if success:
        click.echo(
            click.style(
                f"Successfully stopped Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to stop Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(
    help="Connects to the Thunder Compute instance with the specified instance_ID",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=False)
@click.option("-t", "--tunnel", type=int, multiple=True, help="Tunnel specific ports, i.e. to forward locally hosted webpages or APIs")
def connect(tunnel, instance_id=None):
    # Set default instance_id to '0' if not provided
    instance_id = instance_id or "0"
    click.echo(
        click.style(
            f"Connecting to Thunder Compute instance with instance_id: {instance_id}...",
            fg="cyan",
        )
    )
    token = get_token()
    success, error, instances = utils.get_instances(token)
    if not success:
        raise click.ClickException(f"Failed to list Thunder Compute instance: {error}")

    for curr_instance_id, metadata in instances.items():
        if curr_instance_id == instance_id:
            if metadata["ip"] == None:
                raise click.ClickException(
                    f"Instance {instance_id} is not available to connect"
                )

            ip = metadata["ip"]

            if ip is None or ip == "":
                raise click.ClickException(
                    f"Unable to connect to instance {instance_id}, is the instance running?"
                )

            keyfile = utils.get_key_file(metadata["uuid"])
            if not os.path.exists(keyfile):
                if not utils.add_key_to_instance(instance_id, token):
                    raise click.ClickException(
                        f"Unable to find or create ssh key file for instance {instance_id}"
                    )


            start_time = time.time()
            connection_successful = False
            while start_time + 60 > time.time():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                    connection_successful = True
                    break
                except Exception as e:
                    continue

            if not connection_successful:
                raise click.ClickException(
                    "Failed to connect to the Thunder Compute instance within one minute. Please retry this command or contact the developers at support@thundercompute.com if this issue persists"
                )

            basedir = join(os.path.expanduser("~"), ".thunder")
            ssh.exec_command("mkdir -p ~/.thunder && chmod 700 ~/.thunder")
            stdin, stdout, stderr = ssh.exec_command("pip install --upgrade tnr")
            stdout.read().decode()  # Forces the command to get executed

            scp = SCPClient(ssh.get_transport())

            if os.path.exists(join(basedir, "token")):
                scp.put(join(basedir, "token"), remote_path="~/.thunder/token")

            # Update ~/.ssh/config
            # Fallback to "base" which has no default ports on this lookup
            host_alias = f"tnr-{instance_id}"
            exists, prev_ip = utils.get_ssh_config_entry(host_alias)
            if not exists:
                utils.add_instance_to_ssh_config(ip, keyfile, host_alias)
            else:
                if ip != prev_ip:
                    utils.update_ssh_config_ip(host_alias, ip)
                    
            # Construct tunnel command
            tunnel_args = []
            for port in tunnel:
                tunnel_args += ["-L", f"{port}:localhost:{port}"]
            template_port = OPEN_PORTS.get(metadata.get('template', 'base'))
            if template_port:
                tunnel_args += ["-L", f"{template_port}:localhost:{template_port}"]
            
            # Run SSH command
            if platform.system() == "Windows":
                subprocess.run(
                    ["ssh"] + tunnel_args + [
                        "-q",  # Quiet mode, suppresses warnings
                        f"ubuntu@{ip}",
                        "-o",
                        "StrictHostKeyChecking=accept-new",  # Accepts new hosts permanently without asking
                        "-i",
                        rf"{keyfile}",
                        "-t",
                        f"{'export TNR_API_TOKEN=' + os.environ['TNR_API_TOKEN'] + ';' if 'TNR_API_TOKEN' in os.environ else ''} exec /home/ubuntu/.local/bin/tnr run /bin/bash",
                    ],
                    shell=True,
                )
            else:
                subprocess.run(
                    [
                        f"ssh \
                        {' '.join(tunnel_args)}\
                        -q ubuntu@{ip} \
                        -o StrictHostKeyChecking=accept-new \
                        -o UserKnownHostsFile=/dev/null \
                        -i {keyfile} \
                        -t '{'export TNR_API_TOKEN=' + os.environ['TNR_API_TOKEN'] + ';' if 'TNR_API_TOKEN' in os.environ else ''} \
                        exec /home/ubuntu/.local/bin/tnr run /bin/bash'\
                        "
                    ],
                    shell=True,
                )
            click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="green"))
            return

    raise click.ClickException(
        f"Unable to find instance {instance_id}. Check available instances with `tnr status`"
    )


@cli.command()
@click.argument("source_path", required=True)
@click.argument("destination_path", required=True)
def scp(source_path, destination_path):
    """Copy data from local machine to a thunder instance or vice versa.

    Arguments:\n
        SOURCE_PATH: The path to copy from. For remote paths, use instance_id:path\n
        DESTINATION_PATH: The path to copy to. For remote paths, use instance_id:path
    """
    try:
        token = get_token()
        success, error, instances = utils.get_instances(token)
        if not success:
            raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")

        # Parse source and destination paths
        src_instance, src_path = _parse_path(source_path)
        dst_instance, dst_path = _parse_path(destination_path)

        # Validate that exactly one path is remote
        if (src_instance and dst_instance) or (not src_instance and not dst_instance):
            raise click.ClickException(
                "Please specify exactly one remote path (instance_id:path) and one local path"
            )

        # Determine direction and get instance details
        instance_id = src_instance or dst_instance
        local_to_remote = bool(dst_instance)
        
        if instance_id not in instances:
            raise click.ClickException(f"Instance '{instance_id}' not found")

        metadata = instances[instance_id]
        if not metadata["ip"]:
            raise click.ClickException(
                f"Instance {instance_id} is not available. Use 'tnr status' to check if the instance is running"
            )

        # Setup SSH connection
        ssh = _setup_ssh_connection(instance_id, metadata, token)
        
        # Prepare paths
        local_path = source_path if local_to_remote else destination_path
        remote_path = dst_path if local_to_remote else src_path
        remote_path = remote_path or "~/"

        # Verify remote path exists before transfer
        if not local_to_remote:
            if not _verify_remote_path(ssh, remote_path):
                raise click.ClickException(
                    f"Remote path '{remote_path}' does not exist on instance {instance_id}"
                )

        # Setup progress bar
        with Progress(
            BarColumn(
                complete_style="cyan",
                finished_style="cyan",
                pulse_style="white"
            ),
            TextColumn("[cyan]{task.description}", justify="right"),
            transient=True
        ) as progress:
            # Perform transfer
            _perform_transfer(
                ssh, 
                local_path, 
                remote_path, 
                instance_id, 
                local_to_remote, 
                progress
            )

    except paramiko.SSHException as e:
        raise click.ClickException(f"SSH connection error: {str(e)}")
    except SCPException as e:
        error_msg = str(e)
        if "No such file or directory" in error_msg:
            if local_to_remote:
                raise click.ClickException(f"Local file '{local_path}' not found")
            else:
                raise click.ClickException(
                    f"Remote file '{remote_path}' not found on instance {instance_id}"
                )
        raise click.ClickException(f"SCP transfer failed: {error_msg}")
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {str(e)}")

def _parse_path(path):
    """Parse a path into (instance_id, path) tuple."""
    parts = path.split(":", 1)
    return (parts[0], parts[1]) if len(parts) > 1 else (None, path)

def _verify_remote_path(ssh, path):
    """Check if remote path exists."""
    cmd = f'test -e $(eval echo {path}) && echo "EXISTS"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode().strip() == "EXISTS"

def _setup_ssh_connection(instance_id, metadata, token):
    """Setup and return SSH connection to instance."""
    keyfile = utils.get_key_file(metadata["uuid"])
    if not os.path.exists(keyfile):
        if not utils.add_key_to_instance(instance_id, token):
            raise click.ClickException(
                f"Unable to find or create SSH key file for instance {instance_id}"
            )

    # Try to connect for up to 60 seconds
    start_time = time.time()
    last_error = None
    while time.time() - start_time < 60:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                metadata["ip"],
                username="ubuntu",
                key_filename=keyfile,
                timeout=10
            )
            return ssh
        except Exception as e:
            last_error = e
            time.sleep(2)  # Add small delay between retries
            
    raise click.ClickException(
        f"Failed to connect to instance {instance_id} after 60 seconds: {str(last_error)}"
    )

def _get_remote_size(ssh, path):
    """Calculate total size of remote file or directory."""
    # Expand any ~ in the path
    cmd = f'eval echo {path}'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    expanded_path = stdout.read().decode().strip()
    
    # Check if it's a file
    cmd = f'if [ -f "{expanded_path}" ]; then stat --format=%s "{expanded_path}"; else echo "DIR"; fi'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode().strip()
    
    if result != "DIR":
        try:
            return int(result)
        except ValueError:
            return None
    
    # If it's a directory, get total size
    cmd = f'du -sb "{expanded_path}" | cut -f1'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    try:
        size = int(stdout.read().decode().strip())
        return size
    except (ValueError, IndexError):
        return None

def _get_local_size(path):
    """Calculate total size of local file or directory."""
    path = os.path.expanduser(path)
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total

def _perform_transfer(ssh, local_path, remote_path, instance_id, local_to_remote, progress):
    """Perform the actual SCP transfer with progress bar."""
    total_size = 0
    transferred_size = 0
    file_count = 0
    current_file = ""
    current_file_size = 0
    current_file_transferred = 0

    # Pre-calculate total size
    try:
        if local_to_remote:
            total_size = _get_local_size(local_path)
        else:
            total_size = _get_remote_size(ssh, remote_path)
    except Exception as e:
        click.echo(click.style("Warning: Could not pre-calculate total size", fg="yellow"))
        total_size = None

    def progress_callback(filename, size, sent):
        nonlocal transferred_size, file_count, current_file, current_file_size, current_file_transferred
        
        if sent == 0:  # New file started
            file_count += 1
            current_file = os.path.basename(filename)
            current_file_size = size
            current_file_transferred = 0
            if total_size is None:
                progress.update(
                    task,
                    description=f"File {file_count}: {current_file.decode('utf-8')} - {_format_size(0)}/{_format_size(size)}"
                )
            else:
                progress.update(
                    task,
                    description=f"File {file_count}: {current_file.decode('utf-8')} - {_format_size(0)}/{_format_size(size)}"
                )
        else:
            # Calculate the increment since last update
            increment = sent - current_file_transferred
            transferred_size += increment
            current_file_transferred = sent
            
            if total_size is not None:
                progress.update(task, completed=transferred_size)
            
            progress.update(
                task,
                description=f"File {file_count}: {current_file.decode('utf-8')} - {_format_size(sent)}/{_format_size(current_file_size)}"
            )

    if local_to_remote:
        action_text = f"Copying {local_path} to {remote_path} on remote instance {instance_id}"
    else:
        action_text = f"Copying {remote_path} from instance {instance_id} to {local_path}"

    click.echo(click.style(f"{action_text}...", fg="white"))
    
    task = progress.add_task(
        description="Starting transfer...",
        total=total_size if total_size else None
    )
    
    transport = ssh.get_transport()
    transport.use_compression(True)

    with SCPClient(transport, progress=progress_callback) as scp:
        if local_to_remote:
            scp.put(local_path, remote_path, recursive=True)
        else:
            scp.get(remote_path, local_path, recursive=True)

    click.echo(click.style(
        f"\nSuccessfully transferred {file_count} files ({_format_size(total_size)})",
        fg="cyan"
    ))

def _format_size(size):
    """Convert size in bytes to human readable format."""
    if size is None:
        return "unknown size"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024 or unit == 'TB':
            return f"{size:.2f} {unit}"
        size /= 1024


@cli.command(
    help="Logs in to Thunder Compute with an API token generated at console.thundercompute.com. Saves the API token to ~/.thunder/token",
    hidden=INSIDE_INSTANCE,
)
def login():
    if not logging_in:
        auth.login()


@cli.command(
    help="Logs out of Thunder Compute and deletes the saved API token",
    hidden=INSIDE_INSTANCE,
)
def logout():
    auth.logout()


def get_version_cache_file():
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "version_requirements.json")

def does_meet_min_required_version():
    CACHE_TTL = 3600  # 1 hour
    cache_file = get_version_cache_file()
    
    # Check if we have a valid cached result
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                # If a user updates, we want to wipe the cache
                if cached['current_version'] != version_parser.parse(version(PACKAGE_NAME)):
                    pass
                elif time.time() - cached['timestamp'] < CACHE_TTL:
                    return tuple(cached['result'])
    except Exception:
        # If there's any error reading cache, continue to make the API call
        pass

    try:
        current_version = version(PACKAGE_NAME)
        response = requests.get(
            f"https://api.thundercompute.com:8443/min_version", timeout=10
        )
        json_data = response.json() if response else {}
        min_version = json_data.get("version")
        
        if version_parser.parse(current_version) < version_parser.parse(min_version):
            result = (False, (current_version, min_version))
        else:
            result = (True, None)

        # Cache the result
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'result': result,
                    'min_version': min_version,  # Store the actual API response
                    'current_version': current_version
                }, f)
        except Exception:
            # If caching fails, just continue
            pass
        return result

    except Exception as e:
        print(e)
        click.echo(
            click.style(
                "Warning: Failed to fetch minimum required tnr version",
                fg="yellow",
            )
        )
        return True, None

@cli.command(hidden=True)
def creds():
    token = get_token()
    uid = utils.get_uid(token)
    click.echo(f'{token},{uid}')

if __name__ == "__main__":
    cli()
