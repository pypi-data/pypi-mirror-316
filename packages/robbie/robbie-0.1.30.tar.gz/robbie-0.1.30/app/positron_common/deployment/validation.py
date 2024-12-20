from typing import Optional
from positron_common.cli.console import console
from positron_common.utils import current_python_version

def validate_python_version(image: Optional[str]) -> bool:
    # example python version: 3.12
    # example image: robbie:1.0.0-gpu-py3.12-torch2.5-ubuntu22.04-dev
    if image:
        image_python_version = image.split("-")[2].replace("py", "")
        python_version = current_python_version()
        if image_python_version != python_version:
            console.print(f"[red]Error: Python version mismatch. The image you are using is built for Python {image_python_version}, but you are running Python {python_version}[/red]")
            return False
    return True
