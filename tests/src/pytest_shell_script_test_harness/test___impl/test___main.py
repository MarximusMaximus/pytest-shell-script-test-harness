#! false
# pylint: disable=duplicate-code
"""
tests/pytest_shell_script_test_harness/test___impl/test___main.py (pytest-shell-script-test-harness)
"""  # noqa: E501,W505,B950


################################################################################
#region Imports

#===============================================================================
#region stdlib

from importlib.metadata import (
    metadata                        as importlib_metadata_metadata,
)
from os import (
    environ                         as os_environ,
)
from os.path import (
    basename                        as os_path_basename,
    dirname                         as os_path_dirname,
    join                            as os_path_join,
)
from subprocess import (
    run                             as subprocess_run,
)
from typing import (
    List,
)

#endregion stdlib
#===============================================================================

#===============================================================================
#region Ours

import pytest_shell_script_test_harness.__impl as MODULE_UNDER_TEST

#endregion Ours
#===============================================================================

#endregion Imports
################################################################################


################################################################################
#region Helper Functions

#-------------------------------------------------------------------------------
def get_project_python_path() -> str:
    """
    Get the project's conda environment's python path.

    Returns:
        str: project's conda environment's python path
    """
    print(f"ASDF MODULE_UNDER_TEST.__file__={MODULE_UNDER_TEST.__file__}")

    # check if in site-packages
    # "asdf/python/site-packages/package/__impl.py" ->
    # "site-packages"
    is_in_site_packages = os_path_basename(
        os_path_dirname(
            os_path_dirname(
                MODULE_UNDER_TEST.__file__,
            ),
        ),
    ) == "site-packages"

    # "asdf/repo/src/package/__impl.py" ->
    # "repo"
    repo_name: str = os_path_basename(
        os_path_dirname(
            os_path_dirname(
                os_path_dirname(
                    MODULE_UNDER_TEST.__file__,
                ),
            ),
        ),
    )

    if is_in_site_packages:
        # get the true package name (as would be used for pip install)
        m = importlib_metadata_metadata(MODULE_UNDER_TEST.__package__)
        repo_name = m["name"]

    python_path: List[str] = []
    python_path.append(
        os_path_dirname(
            os_environ.get(
                "CONDA_PREFIX",
                "/opt/conda/miniforge/envs/placeholder",
            ),
        ),
    )
    python_path.append(repo_name)
    python_path.append("bin")
    python_path.append("python")
    python_path_str = os_path_join("", *python_path)

    return python_path_str

#endregion Helper Functions
################################################################################

################################################################################
#region __main Tests

class Test___main():
    """
    Tests loading the test suite.
    """

    #-------------------------------------------------------------------------------
    def test___main(self) -> None:
        """
        Tests that the library cannot be invoked directly.
        """
        ret = getattr(MODULE_UNDER_TEST, "__main")([])  # noqa: B009
        assert ret != 0

    #-------------------------------------------------------------------------------
    def test___main__shell_invocation(self) -> None:
        """
        Tests that the library cannot be invoked directly.
        """
        python_path_str = get_project_python_path()

        # "asdf/repo/src/package/__impl.py" ->
        # "package"
        package_name = os_path_basename(
            os_path_dirname(
                MODULE_UNDER_TEST.__file__,
            ),
        )

        cmd = [
            python_path_str,
            f"./src/{package_name}/__impl.py",
        ]

        p = subprocess_run(cmd, capture_output=True)

        assert p.returncode == 1
        assert b"This module should not be run directly." in p.stderr

#endregion Tests
################################################################################
