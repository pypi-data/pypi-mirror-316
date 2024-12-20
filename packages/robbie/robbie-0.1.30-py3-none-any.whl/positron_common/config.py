from pydantic import BaseModel, field_validator
from typing import Dict, Optional, List, Union
import os
import copy
import yaml
import re
from yaml import dump
from enum import Enum
from positron_common.utils import get_version, current_python_version
from positron_common.exceptions import RobbieException
from positron_common.user_config import user_config, REMOTE_FUNCTION_SECRET_KEY_NAME
from positron_common.constants import JOB_CONF_YAML_PATH, RUNTIME_ENV_PREFIX
from positron_common.cli.logging_config import logger
from positron_common.enums import JobRunType
from positron_common.cli.console import console
from positron_common.image_name import get_auto_image_name_and_cluster
from positron_common.job_api.funding_envs_images import *

class PositronJob(BaseModel):
    """
    The Job details as defined in the `python_job` from the `job_config.yaml` file.
    """
    name: Optional[str] = None
    funding_group_id: Optional[str] = None
    environment_id: Optional[str] = None
    image: Optional[str] = None # this is not written to the config file
    job_type: Optional[JobRunType] = None
    commands: Optional[List[str]] = None
    workspace_dir: Optional[str] = None
    max_tokens: Optional[int] = None
    max_time: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    dependencies: Optional[str] = None
    conda_env: Optional[str] = None
    # below are values not writtent to the config file
    cluster: Optional[str] = None
    python_version: Optional[str] = current_python_version()
    robbie_sdk_version: Optional[str] = get_version()
    image_selection: Optional[str] = None
    funding_selection: Optional[str] = None
    environment_selection: Optional[str] = None

    @field_validator('commands', mode='after')
    def ensure_non_empty(cls, commands):
        return commands if len(commands) else None

    @field_validator('env', mode='after')
    def ensure_env_is_dict(cls, v):
        if isinstance(v, dict):
            return v
        raise ValueError('env must be a dictionary')

    @field_validator('max_time', mode='before')
    def ensure_max_time_is_int(cls, max_time: Union[int, str, None]) -> Union[int, None]:
        return cls._max_time_to_minutes(max_time)

    @field_validator('max_tokens', mode='before')
    def ensure_max_tokens_is_int(cls, max_tokens: Union[int, str, None]) -> Union[int, None]:
        return cls._max_tokens_to_int(max_tokens)

    def create_runtime_env(self) -> Dict[str, str]:
        """
        Used on the client side to create the prefixed runtime environment variables
        to avoid conflicts with the local environment variables.
        """
        env: Dict[str, str] = {}
        # without env_prefix?? yes, but maybe not in this file, but part of the deploy.py file.
        env[REMOTE_FUNCTION_SECRET_KEY_NAME] = user_config.user_auth_token
        if not self.env:
            return env
        for key, value in self.env.items():
            if (value == ""):
                env_var = os.environ.get(key)
                if env_var is None:
                    raise ValueError(f"The env prop {key} is unset inside job_config.yaml and also unset in local env vars. Please set this value.")
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = env_var
            else:
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = value
        return env

    @staticmethod
    def _max_time_to_minutes(max_time: Union[int, str, None]) -> Union[int, None]:
        if not max_time:
            return None
        if isinstance(max_time, int):
            return max_time
        matches = re.search(r'^(\d+):(\d{2})$', max_time)
        if matches is None:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
        except:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        if minutes >= 60:
            raise ValueError('Invalid Job Config: Field "max_time" ({max_time}) has invalid minutes! Must be 0 <= minutes < 60!')
        return hours * 60 + minutes

    @staticmethod
    def _max_tokens_to_int(max_tokens: Union[int, str, None]) -> Union[int, None]:
        if not max_tokens:
            return None
        if isinstance(max_tokens, int):
            return max_tokens
        try:
            max_tokens = int(max_tokens)
        except:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        if max_tokens <= 0:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        return max_tokens

    def validate_values(self) -> None:
        errors = []
        if self.env and not validate_env_vars(self.env):
            errors.append('At least one of the environment variables provided is invalid')
        if errors:
            raise RobbieException(f'Invalid configuration. Errors: {errors}')
        return None
    
    def namestr(self, obj, namespace):
        return [name for name in namespace if namespace[name] is obj]

    def to_string(self, title: str = 'None'):
        message = f"""
- python_version: {self.python_version}
- robbie_sdk_version: {self.robbie_sdk_version}
- name: {self.name}
- funding_group_id: {self.funding_group_id}
    - funding_selection: {self.funding_selection}
- environment_id: {self.environment_id}
    - environment_selection: {self.environment_selection}
- image: {self.image}
    - image_selection: {self.image_selection}
- cluster: {self.cluster}
- dependencies: {self.dependencies}
- conda_env: {self.conda_env}
- job_type: {self.job_type}
- workspace_dir: {self.workspace_dir}
- max_tokens: {self.max_tokens}
- max_time: {self.max_time}
- env: {self.env}
- commands: {self.commands}"""

        if title:
            return f"========== {title} ==========\n{message}"
        else:
            return message
        

class PositronJobConfig(BaseModel):
    """
    The `job_config.yaml` schema class.
    """
    version: float
    python_job: PositronJob

    def write_to_file(this, filename: str = JOB_CONF_YAML_PATH):
        copy_of_config = copy.deepcopy(this)
        del copy_of_config.python_job.robbie_sdk_version
        del copy_of_config.python_job.python_version
        del copy_of_config.python_job.cluster
        del copy_of_config.python_job.image_selection
        del copy_of_config.python_job.funding_selection
        del copy_of_config.python_job.environment_selection
        config_dict = copy_of_config.model_dump(
            exclude_unset=True
        )
        config_dict = convert_enums_to_values(config_dict)

        with open(filename, 'w') as file:
            file.write(dump(config_dict, sort_keys=False))


def convert_enums_to_values(d: dict) -> dict:
    """
    Converts Enum type values in the dictionary to their respective values.
    """
    for key, value in d.items():
        if isinstance(value, Enum):
            d[key] = value.value
        elif isinstance(value, dict):
            convert_enums_to_values(value)
    return d


def is_valid_key_value(keyvalue):
    """
    Validate that the key-value contains only alphanumeric characters, dashes, and underscores, and has no spaces.
    """
    return bool(re.match(r'^[\w-]+$', keyvalue))

def validate_env_vars(env_dict):
    """
    Validate the environment variables from the given dictionary.
    """
    valid = True
    for key, value in env_dict.items():
        if not is_valid_key_value(key):
            print(f"Invalid key (contains invalid characters or spaces): {key}")
            valid = False
        if value != "" and not is_valid_key_value(value):
            print(f"Invalid value (contains invalid characters or spaces): {value}")
            valid = False
    return valid

def merge_config(base_config: PositronJob, override_config: PositronJob) -> PositronJob:
    """
    Makes it easy to merge decorator configs on top of the YAML config.
    """
    update_data = override_config.dict(exclude_unset=True)
    updated_config = base_config.copy(update=update_data)
    return updated_config


def invalid_yaml_keys(yaml_job_keys) -> bool:
    """
    Validates the yaml keys against the PositronJob class.
    """
    # Get only attributes from PositronJob
    base_attrs = set(dir(BaseModel))
    derived_attrs = set(dir(PositronJob()))
    additional_attrs = derived_attrs - base_attrs

    # Exclude built-in attributes (e.g., __init__, __module__)
    validKeys = [attr for attr in additional_attrs if not attr.startswith('__')]
    
    weHaveInvalidYamlKeys = False
    for key in yaml_job_keys:
        if key not in validKeys:
            weHaveInvalidYamlKeys = True
            raise RobbieException(f'Error: wrong param in the job_config.yaml: -> {key}')

    return weHaveInvalidYamlKeys

def parse_job_config(config_path: str = 'job_config.yaml') -> Optional[PositronJob]:
    """
    Load the job configuration from the `job_config.yaml` file if it exists
    """
    
    if not os.path.exists(config_path):
        logger.debug('job_config.yaml file not found')
        return None
    
    try:
        # this happens sometimes and it causes the job to fail
        if os.path.getsize(config_path) == 0:
            logger.debug('job_config.yaml file is empty')
            return None
        with open(config_path, 'r') as job_config_file:
            job_config_dict = yaml.safe_load(job_config_file)
            job = job_config_dict["python_job"]
            if invalid_yaml_keys(job.keys()):
                return None
            job_config = PositronJobConfig(**job_config_dict)
            return job_config.python_job
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')
        return None

def merge_from_yaml_and_args(input_job_config: PositronJob, args_job_config: Union[PositronJob, None]) -> PositronJob:
    """
    Merge the job_config (from the yaml or empty object) file with the command line arguments for funding, environment, and image.
    Ensure that environment is in the funding group.

    Behavior:
    - Command line arguments take precedence over the job_config.yaml file
    - Command line arguments are not memorized in the job_config.yaml file 
    - Defaults are applied where selections are missing

    """

    funding_arg = args_job_config.funding_group_id if args_job_config else None
    environment_arg = args_job_config.environment_id if args_job_config else None
    image_arg = args_job_config.image if args_job_config else None
    
    logger.debug(input_job_config.to_string("Entering _merge_from_yaml_and_args()"))
    return_config = copy.deepcopy(input_job_config)
    logger.debug(f"return_config: {id(return_config)} created from input_job_config: {id(input_job_config)}")

    # Is there a funding group in the input config?
    if input_job_config.funding_group_id:
        logger.debug(f"return_config.funding_group_id: already set: {return_config.funding_group_id}")
        # ok the correct funding group is already in return_config.funding_group_id
        pass

    # Is there a funding group argument?
    if funding_arg:
        logger.debug(f"Setting or overriding return_config.funding_group_id: {return_config.funding_group_id} <-- funding_arg: {funding_arg}")
        return_config.funding_selection = "Overridden by argument"
        return_config.funding_group_id = funding_arg
        
    # pre-fetch the funding sources info and def env
    fs = list_funding_sources()
    if len(fs) == 0:
        logger.debug("No funding sources found.")
        return None

    def_env_id = None
    # Have we identified a funding group yet?
    if return_config.funding_group_id:
        logger.debug(f"Yes, we have a funding group: {return_config.funding_group_id}")
        if not return_config.environment_id:
            for _, val in fs.items():
                if (val[FS_ID] == return_config.funding_group_id):
                    def_env_id = val.get(FS_DEF_ENV_ID)
            if not def_env_id:
                console.print(f"[bold red]Can't get the default environment for the funding group: {return_config.funding_group_id}")
                return None   
            if not return_config.environment_id:
                logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
                return_config.environment_id = def_env_id
                return_config.environment_selection = "Default"
        else:
            if not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not the funding group: {return_config.funding_group_id}")
                return None
    else: 
        # No funding group id, let's get the user's personal and defaut environment
        logger.debug("Still no funding group id, let's get the user's personal one.")
        for _, val in fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return_config.funding_group_id = val.get(FS_ID)
                def_env_id = val.get(FS_DEF_ENV_ID)
                logger.debug(f"Setting return_config.funding_group_id to PERSONAL: {return_config.funding_group_id}, fetched def_env_id: {def_env_id}")
        if return_config.funding_group_id:
            return_config.funding_selection = "Default"
        else:
            console.print("[bold red]Can't get the default funding source (personal).")
            return None
        if not def_env_id:
            console.print("[bold red]Can't get the default environment for the personal funding source.")
            return None
        # the user specified an environment in the job_config.yaml file
        if return_config.environment_id:
            # just for fun, lets check if its in the funding group
            if not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not the funding group: {return_config.funding_group_id}")
                return None
        else:
            logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
            return_config.environment_id = def_env_id
            return_config.environment_selection = "Default from Funding Source"
        
    # At this point we should have a funding group id and a default environment id
    if environment_arg:
        # check to make certain the environment argument is in the funding group
        if not _env_in_funding_group(environment_arg, return_config.funding_group_id):
            console.print(f"[bold red] Sorry, the environment you passed as an argument: {environment_arg} is not the funding group: {return_config.funding_group_id}")
            return None
        logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- environment_arg: {environment_arg}")
        return_config.environment_id = environment_arg
        return_config.environment_selection = "Overridden by argument"

    # Use configured image or auto-select
    if return_config.image and not image_arg:
            logger.debug(f'Using the image: {return_config.image} found in job_config.yaml. To override, please use the --image option.')
            return_config.image_selection = "From job_config.yaml"
    elif return_config.image and image_arg:
        logger.debug(f'overriding image job_config.yaml image: {return_config.image}, setting image to: {image_arg}')
        return_config.image = image_arg
        return_config.image_selection = "Overridden by argument"
    elif not return_config.image and image_arg:
        logger.debug(f'setting image job_config.yaml image: {return_config.image}, setting image to: {image_arg}')
        return_config.image = image_arg
        return_config.image_selection = "Set by argument"
    elif not return_config.image:
        logger.debug(f'No image in job_config.yaml file, setting to auto-select')
        return_config.image = "auto-select"
    
    # Handle special case
    if return_config.image == "auto-select":
        return_config.image, return_config.cluster = get_auto_image_name_and_cluster(return_config.funding_group_id, return_config.environment_id)
        return_config.image_selection = "Automatically Selected"
        
    logger.debug(return_config.to_string("Exiting _merge_from_yaml_and_args()"))

    return return_config

def _env_in_funding_group(env_id, funding_group_id):
    """ sanity check a environment id is in the funding group """
    envs = list_environments(funding_group_id)
    for _, val in envs.items():
        if (val[FS_ID] == env_id):
            return True
    return False

# if main then load and validate
if __name__ == "__main__":
    job_config = parse_job_config()
    if job_config:
        job_config.validate_values()
        print(job_config)
