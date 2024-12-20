import os
import pytest

from edna2 import config


@pytest.fixture
def set_ispyb_user_env():
    """Fixture to temporarily set the ISPyB_user environment variable."""
    old_ispyb_user = os.environ.get("ISPyB_user")
    os.environ["ISPyB_user"] = "ispybuser"
    yield
    if old_ispyb_user is None:
        del os.environ["ISPyB_user"]
    else:
        os.environ["ISPyB_user"] = old_ispyb_user


def test_load_config():
    dict_config = config.load_config(site="esrf_id30a2")
    assert "ExecDozor" in dict_config


def test_get_task_config(set_ispyb_user_env):
    dict_config = config.get_task_config("ExecDozor", site="esrf_id30a2")
    assert "ix_min" in dict_config

    dict_config = config.get_task_config("ISPyB", site="esrf_id30a2")
    assert "username" in dict_config
    assert dict_config["username"] == os.environ["ISPyB_user"]


def test_get(set_ispyb_user_env):
    username = config.get("ISPyB", "username", site="esrf_id30a2")
    assert username == os.environ["ISPyB_user"]
