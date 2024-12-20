import os
import typer
import copy
from typing_extensions import Annotated
from typing import Optional
from positron_common.deploy import command_runner_deploy
from positron_common.config import parse_job_config, PositronJob, merge_from_yaml_and_args
from positron_common.cli_args import args
from positron_common.cli.console import console, ROBBIE_DEFAULT, ROBBIE_BLUE
from positron_common.constants import JOB_CONF_YAML_PATH
from positron_common.image_name import get_auto_image_name_and_cluster
from positron_common.cli.interactive import prompt_and_build_positron_job_config
from positron_common.cli.logging_config import logger
from positron_common.enums import JobRunType
from positron_common.observability.main import track_command_usage
from positron_cli.download import filename_is_valid
from positron_common.job_api.funding_envs_images import *
from positron_common.job_api.validate_user_auth_token import is_auth_token_valid
from positron_common.user_config import user_config
from positron_cli.login import login
from pipreqs.pipreqs import init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style



@track_command_usage("run")
def run(
  # the following options control the job configuration
  name_arg: Annotated[str, typer.Option("--name", help="Name of the run")] = None,
  funding_arg: Annotated[str, typer.Option("--funding_group_id", help="Specify the team to run the job on.")] = None,
  environment_arg: Annotated[str, typer.Option("--environment_id", help="Specify the hardware to run the job on.")] = None,
  image_arg: Annotated[str, typer.Option("--image", help="Specify the image to run the job on or 'auto-select'.")] = None,
  commands_arg: Annotated[Optional[str], typer.Argument(help='String of shell commands, a .py file, or a .ipynb file.')] = None,
  auto_capture_deps: Annotated[bool, typer.Option("--auto-dep", help='(EXPERIMENTAL) Automatically resolve Python dependencies.')] = None,
  # the following options control how the job is run
  tail: Annotated[bool, typer.Option("--tail", help='Tail the run\'s stdout back to your CLI.')] = False,
  status: Annotated[bool, typer.Option("--s", help='Monitor run status in your CLI.')] = False,
  skip_prompts: Annotated[bool, typer.Option("--y", help='Bypass the prompts and execute the run immediately.')] = False,
  interactive: Annotated[bool, typer.Option("--i", help="Interactively choose your run configuration.")] = False,
  download: Annotated[str, typer.Option("--download", help="Download a results <file> to your local machine. Specify 'all' for the complete list.")] = None,
  path: Annotated[str, typer.Option("--path", help="Local directory where the downloaded files will be stored.")] = None,
  create_only: Annotated[bool, typer.Option("--create-only", help="Only create the run, do not execute it. [Robbie internal use only]")] = False,
) -> None:
    """
    Run shell commands as a batch job in Robbie

    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created/overwritten

    In scenerio 1 and 2, user's can pass in funding groups and enviroments as arguments to override the job_config.yaml file.

    """

    logger.debug(f"""========== run() arguments ==========
    - name_arg: {name_arg}
    - funding_arg: {funding_arg}
    - environment_arg: {environment_arg}
    - image_arg: {image_arg}
    - commands_arg: {commands_arg}
    - auto_capture_deps: {auto_capture_deps}
    - tail: {tail}
    - status: {status}
    - skip_prompts: {skip_prompts}
    - interactive: {interactive}
    - download: {download}
    - path: {path}
    - create_only: {create_only}""")

    # check if the user is logged in
    login()

    # we can either stream or monitor status but not both at the same time
    if tail and status:
        console.print('[red]Error: Choose either the -logs and -s option.')
        return
    
    if (download and not (tail or status)):    
        console.print('[red]Error: The --download option can only be used with the --tail or --s option.')
        return
    
    if download and not filename_is_valid(download):
        console.print('[red]Error: Please specify a valid file name or "all" to download all files.')
        return
    
    if path and not download:
        console.print('[red]Error: The --path option can only be used with the --download option.')
        return
    
    if path and not os.path.exists(path):
        console.print('[red]Error: The path you specified is not valid.')
        return

    # initialize the argument singleton
    args.init(
        name=name_arg,
        stream_stdout=tail,
        skip_prompts=skip_prompts,
        monitor_status=status,
        commands_to_run=commands_arg,
        interactive=interactive,
        create_only=create_only,
        download=download,
        local_path=path,
        auto_capture_deps=auto_capture_deps
    )

    # first-level sanity checks
    if commands_arg and interactive:
        console.print("[red]Sorry: Please specify command line or use the interactive mode.")
        return
    
    if interactive and (funding_arg or environment_arg or image_arg):
        console.print("[red]Sorry: You can't specify funding, environments, or images in interactive mode.")
        return

    # capture arguments job configuration
    job_config_args = PositronJob()
    if funding_arg:
        job_config_args.funding_group_id = funding_arg
        job_config_args.funding_selection = "Passed as argument to @remote decorator"
    if environment_arg:
        job_config_args.environment_id = environment_arg
        job_config_args.environment_selection = "Passed as argument to @remote decorator"
    if image_arg:
        job_config_args.image = image_arg
        job_config_args.image_selection = "Passed as argument to @remote decorator"
    
    # Read in the job_config.yaml file if it exists
    yaml_job_config = None
    if os.path.exists(JOB_CONF_YAML_PATH) and os.path.getsize(JOB_CONF_YAML_PATH) != 0:
        console.print(f'Found run configuration file (reading...): {JOB_CONF_YAML_PATH}')
        yaml_job_config = parse_job_config(JOB_CONF_YAML_PATH)
        if yaml_job_config:
            if yaml_job_config.funding_group_id:
                yaml_job_config.funding_selection = "From job_config.yaml"
            if yaml_job_config.environment_id:
                yaml_job_config.environment_selection = "From job_config.yaml"
            if yaml_job_config.image:
                yaml_job_config.image_selection = "From job_config.yaml"
        else:
            console.print('[red]Error parsing job_config.yaml file. Disregarding it.')
            

    """
    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created

    There are three important variables in the code:
    - yaml_job_config - this is the PositronJob object created from the job_config.yaml file
    - job_config_to_run - this is the PositronJob object that will be passed to deploy to run the job
    - add_args_to_run_job_config - this is a flag that is set for scenerio 1 and 2 to merge the passed arguments into to the job_config_to_run object
    """
    add_args_to_run_job_config = False
    # 
    # Scenerio 1: User types: "robbie run" - commands are run from the job_config.yaml file
    #
    if not commands_arg and not interactive:
        logger.debug("@@@@@@@@@@@   Scenerio 1: User types: robbie run")
        if not yaml_job_config:
            console.print('[red]Error: No job_config.yaml file found or it is invalid. Cannot find commands to run.')
            return
        if not yaml_job_config.commands:
            console.print('[red]Error: No commands found in job_config.yaml file.')
            return
        job_config_to_run = yaml_job_config
        add_args_to_run_job_config = True

    # 
    # Scenerio 2. User types: robbie run "command" - commands override the job_config.yaml file if it exists
    #
    if commands_arg:
        logger.debug("@@@@@@@@@@ Scenerio 2: User types: robbie run 'command'")

        # Is there a job_config.yaml file?
        if yaml_job_config:
            if yaml_job_config.commands:
                console.print('[yellow]Overriding commands in existing job_config.yaml file.')
            job_config_to_run = yaml_job_config
        else:
            console.print('No job_config.yaml file found, using defaults.')
            job_config_to_run = PositronJob()
        
        # Add the commands to the job_config
        job_config_to_run.commands = []
        job_config_to_run.commands.append(commands_arg)

        add_args_to_run_job_config = True
        
    # now lets deal with the arguments for the first two scenarios
    if add_args_to_run_job_config:
        logger.debug("Adding arguments to job_config")

        job_config_to_run = merge_from_yaml_and_args(job_config_to_run, job_config_args)
        if not job_config_to_run:
            logger.debug('[red]Error: Unable to merge yaml and arguments.')
            return
        
    # 
    # Scenerio 3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created or modified
    #
    if interactive:
        logger.debug("@@@@@@@@@ Scenerio 3: User types: robbie run --i")
        preserve = False
        if yaml_job_config and yaml_job_config.commands:
            response = prompt('You are about to override your job_config.yaml, do you want preserve the enviroment variables and commands [[y]/n]:', style=Style.from_dict({'prompt': 'yellow'}))
            if response in ["y", "yes", "Yes", "Y", ""]:
                preserve = True        
                       
        # lets prompt the user 
        console.print(f"Please follow the prompts to configure your run ([{ROBBIE_DEFAULT}][] = default[/{ROBBIE_DEFAULT}], <tab> for options)")
        captured_job_config = prompt_and_build_positron_job_config(preserve)
        if captured_job_config == None:
            console.print(f"[red]Sorry, failed to create a file {JOB_CONF_YAML_PATH}")
            return
        
        logger.debug(captured_job_config.python_job.to_string("Interactive cfg"))
        # keeping the previous commands and envs from the job_config.yaml file
        if preserve:
            if yaml_job_config.env:
                # this prevents a null env from being copied over
                captured_job_config.python_job.env = yaml_job_config.env
            
            captured_job_config.python_job.commands = yaml_job_config.commands

        if captured_job_config.python_job.commands == None:
            console.print("[red]Error: You did not specify any commands to run.")
            return
        captured_job_config.write_to_file(filename=JOB_CONF_YAML_PATH)
        job_config_to_run = captured_job_config.python_job

    # Handle auto capturing dependencies for non-Conda environments
    # this comes in two forms:
    # 1. User types: robbie run --auto-dep
    # 2. job_config.yaml file has dependencies: auto-capture
    overwrite_reqs = False
    if auto_capture_deps or (yaml_job_config and yaml_job_config.dependencies == "auto-capture"):
        logger.debug("Auto-capturing dependencies")
        if os.path.exists("./requirements.txt"):
            if args.skip_prompts == False:
                overwrite_reqs = prompt('A requirement.txt file already exist, do you want to overwrite it? [y/N]:', style=Style.from_dict({'prompt': 'yellow'}))
                if overwrite_reqs in ["no", "n", "No", "N", ""]:
                    console.print("[yellow]See you soon![/yellow]")
                    return
            else:
                overwrite_reqs = True
            
        # arguments for pipreqs package - https://github.com/bndr/pipreqs
        pipreq_args = {
            "<path>": ".",
            "--print": False,
            "--savepath": None,
            "--pypi-server": None,
            "--proxy": None,
            "--use-local": False,
            "--diff": None,
            "--clean": None,
            "--mode": None,
            "--scan-notebooks": True,
            "--force": False
        }
        if overwrite_reqs:
            pipreq_args["--force"] = True

        console.print("Analyzing Python (.py) and Notebook (.ipynb) files for dependencies...", style=ROBBIE_BLUE)
        init(pipreq_args) # this is the pipreqs call    
        console.print("[green]✔[/green] Dependency analysis complete, requirements.txt file created.")
        job_config_to_run.dependencies = "./requirements.txt"
        # hack to remove robbie from the generated requirements.txt file
        _remove_package_from_requirements('robbie')

    job_config_to_run.job_type = JobRunType.BASH_COMMAND_RUNNER
    logger.debug("Calling command_runner_deploy")
    command_runner_deploy(job_config_to_run)

def _remove_package_from_requirements(package_name, file_path='./requirements.txt'):
    """ this is hack when the robbie package gets auto-added to the requirements.txt file in the auto-capture dependencies mode """
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Write back all lines except the one with the package name
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.strip().startswith(package_name):
                file.write(line)
