#! false
# pylint: disable=duplicate-code
"""
tests/pytest_shell_script_test_harness/test___impl/test_shell_script_test_harness.py (pytest-shell-script-test-harness)
"""  # noqa: E501,W505,B950

################################################################################
#region Imports

#===============================================================================
#region stdlib


#endregion stdlib
#===============================================================================

#===============================================================================
#region Ours

# import pytest_shell_script_test_harness as MODULE_UNDER_TEST
from pytest_shell_script_test_harness import (
    PytestShellScriptTestHarness          as pytest_shell_script_test_harness_PytestShellScriptTestHarness,  # noqa: E501,B950
)

#endregion Ours
#===============================================================================

#endregion Imports
################################################################################

################################################################################
#region shell_script_test_harness Tests

class Test_shell_script_test_harness():
    """
    Tests for shell_script_test_harness
    """

    #---------------------------------------------------------------------------
    def test_shell_script_test_harness(
        self,
        shell_script_test_harness:
            pytest_shell_script_test_harness_PytestShellScriptTestHarness,
    ) -> None:
        """
        Test that fixture returns correct object type.

        Args:
            shell_script_test_harness
                (pytest_shell_script_test_harness.PytestShellScriptTestHarness):
                PytestShellScriptTestHarness fixture
        """

        assert (
            shell_script_test_harness.__class__.__name__ ==
                "PytestShellScriptTestHarness"
        )

#endregion shell_script_test_harness Tests
################################################################################

################################################################################
#region shell_script Tests

class Test_shell_script():
    """
    Tests for shell_script_test_harness
    """

    #---------------------------------------------------------------------------
    def test_shell_script_test_harness(
        self,
        shell_script:
            pytest_shell_script_test_harness_PytestShellScriptTestHarness,
    ) -> None:
        """
        Test that fixture returns correct object type.

        Args:
            shell_script_test_harness
                (pytest_shell_script_test_harness.PytestShellScriptTestHarness):
                PytestShellScriptTestHarness fixture
        """

        assert (
            shell_script.__class__.__name__ == "PytestShellScriptTestHarness"
        )

#endregion shell_script Tests
################################################################################
