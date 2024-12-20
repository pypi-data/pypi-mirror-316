import os
import pathlib
import yaml
from functools import lru_cache
from typing import Optional, Any, Union, Type


def get_site() -> str:
    return os.environ.get("EDNA2_SITE", "Default")


def set_site(site:str) -> str:
    os.environ["EDNA2_SITE"] = site


def load_config(site: Optional[str] = None) -> dict:
    """Load and cache the YAML configuration for a specific site."""
    if site is None:
        site = get_site()
    config_dir = os.environ.get("EDNA2_CONFIG")
    if config_dir:
        pathlib.Path(config_dir)
    else:
        config_dir = pathlib.Path(__file__).parent

    return _load_config(config_dir, site)


@lru_cache(maxsize=None)
def _load_config(config_dir: str, site: str) -> dict:
    config_path = pathlib.Path(config_dir) / f"{site}.yaml".lower()
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return dict()


def get_task_config(task_name: str, site: Optional[str] = None) -> dict:
    task_config = {}

    # Load the site configuration
    config = load_config(site=site)

    # Check for "Include" section to load additional site configurations
    if "Include" in config:
        for included_site in config["Include"]:
            task_config.update(get_task_config(task_name, site=included_site))

    # Update with the current site's configuration
    if task_name in config:
        task_config.update(config[task_name])

    # Substitute environment variables (expand ${} in strings)
    for key, value in task_config.items():
        if isinstance(value, str):
            task_config[key] = os.path.expandvars(value)

    return task_config


def is_embl(site: Optional[str] = None):
    if not site:
        site = get_site()
    return site.lower().startswith("embl")


def is_esrf(site: Optional[str] = None):
    if not site:
        site = get_site()
    return site.lower().startswith("esrf")


def get(
    task: Optional[Union[Type[Any], str]],
    parameterName: str,
    default: Any = None,
    site: Optional[str] = None,
):
    if isinstance(task, str):
        task_config = get_task_config(task, site=site)
    else:
        task_config = get_task_config(task.__class__.__name__, site=site)
    return task_config.get(parameterName, default)
