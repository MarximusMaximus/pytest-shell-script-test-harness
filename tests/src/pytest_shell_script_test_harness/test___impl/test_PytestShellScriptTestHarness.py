#! false
# pylint: disable=duplicate-code
"""
tests/pytest_shell_script_test_harness/test___impl/test_PytestShellScriptTestHarness.py (pytest-shell-script-test-harness)
"""  # noqa: E501,W505,B950

# NOTE: we cannot use the shell_script_test_harness fixture in this file, we must
#   create the PytestShellScriptTestHarness object manually

################################################################################
#region Imports

#===============================================================================
#region stdlib

from copy import (
    deepcopy                        as copy_deepcopy,
)
from os.path import (
    join                            as os_path_join,
)
from platform import (
    python_version                  as platform_python_version,
    uname_result                    as platform_uname_result,
)
from shutil import (
    copy2                           as shutil_copy2,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

#endregion stdlib
#===============================================================================

#===============================================================================
#region third party

from packaging import (
    version                         as packaging_version,
)
import pytest  # required to use pytest.fixture which cannot be aliased via 'as'
from pytest import (
    FixtureRequest                  as pytest_FixtureRequest,
    mark                            as pytest_mark,
    MonkeyPatch                     as pytest_MonkeyPatch,
    param                           as pytest_param,
    raises                          as pytest_raises,
    TempPathFactory                 as pytest_TempPathFactory,
)

#endregion third party
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
#region Fixtures

@pytest.fixture
def mock_repo(
    mock_repo: str,  # pylint: disable=redefined-outer-name
    request: pytest_FixtureRequest,
) -> str:
    """
    Create a mock repo to use that looks like a repo that uses
        pytest-shell-script-test-harness, but named pytest_shell_script_test_harness
        so we can re-use the already available conda environment.

    Args:
        monkeypatch (pytest_MonkeyPatch): pytest monkeypatch fixture
        request (pytest_FixtureRequest): pytest request fixture

    Returns:
        str: path of mock repo
    """
    example_shell_script_path = os_path_join(
        request.node.fspath.dirname,
        "example_shell_script.sh",
    )

    shutil_copy2(
        example_shell_script_path,
        mock_repo,
    )

    return mock_repo

#endregion Fixtures
################################################################################

################################################################################
#region Helper Functions

def coerceSubprocessCommandToString(
    *args: Any,
    **kwargs: Any,
) -> Union[str, None]:  # pragma: no cover
    """
    Coerce a subprocess's call into a str.

    Returns:
        Union[str, None]: The subprocess's command as a str if exists, or None.
    """
    cmd: Optional[List[str]] = None
    if (
        len(args) > 0 and
        isinstance(args[0], list)
    ):
        cmd = args[0]
    elif (
        len(kwargs) > 0 and
        "cmd" in kwargs
    ):
        if isinstance(kwargs["cmd"], list):
            cmd = kwargs["cmd"]
        else:
            cmd = [kwargs["cmd"]]

    cmd_str = None
    if isinstance(cmd, list):
        cmd_str = " ".join(cmd)

    return cmd_str

#endregion Helper Functions
################################################################################

################################################################################
#region PytestShellScriptTestHarness::init Tests

class Test_PytestShellScriptTestHarness____init__():
    """
    Tests for PytestShellScriptTestHarness::__init__
    """

    def test_PytestShellScriptTestHarness____init__(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test obj construction & initialization for PytestShellScriptTestHarness.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """

        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        assert obj.mock_repo == mock_repo
        assert obj.request == request

#endregion PytestShellScriptTestHarness::init
################################################################################

################################################################################
#region PytestShellScriptTestHarness::run Tests

#===============================================================================
class Test_PytestShellScriptTestHarness__run():
    """
    Tests for PytestShellScriptTestHarness::run
    """

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__success(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        monkeypatch: pytest_MonkeyPatch,
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run python only during a successful test,
            without calling out to shell.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """

        #.......................................................................
        def mock_subprocess_run(*args: Any, **kwargs: Any) -> object:
            cmd_str = args[0]

            assert \
                (
                    "test_shell.sh"
                ) in cmd_str
            assert \
                (
                    "Test_PytestShellScriptTestHarness__run" +
                    "__" +
                    "test_PytestShellScriptTestHarness__run__success" +
                    " " +
                    "echo foo"
                ) in cmd_str

            assert "env" in kwargs
            assert len(kwargs["env"]) > 2
            assert "OMEGA_DEBUG" in kwargs["env"]
            assert kwargs["env"]["OMEGA_DEBUG"] == "all"
            assert "NO_COLOR" in kwargs["env"]
            assert kwargs["env"]["NO_COLOR"] == "true"
            assert "capture_output" in kwargs
            assert kwargs["capture_output"] is True
            assert "shell" in kwargs
            assert kwargs["shell"] is True

            class ReturnObject():
                pass
            o = ReturnObject()
            setattr(o, "returncode", 0)  # noqa: B010
            setattr(o, "stdout", b"foo\n")  # noqa: B010
            setattr(o, "stderr", b"")  # noqa: B010

            return o

        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setitem(
            obj.run.__globals__,
            "subprocess_run",
            mock_subprocess_run,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__assert(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        monkeypatch: pytest_MonkeyPatch,
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run python only during a failed test,
            without calling out to shell.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """

        #.......................................................................
        def mock_subprocess_run(*args: Any, **kwargs: Any) -> object:
            cmd_str = args[0]

            assert \
                (
                    "test_shell.sh"
                ) in cmd_str
            assert \
                (
                    "Test_PytestShellScriptTestHarness__run" +
                    "__" +
                    "test_PytestShellScriptTestHarness__run__assert" +
                    " " +
                    "echo foo"
                ) in cmd_str

            assert "env" in kwargs
            assert len(kwargs["env"]) > 2
            assert "OMEGA_DEBUG" in kwargs["env"]
            assert kwargs["env"]["OMEGA_DEBUG"] == "all"
            assert "NO_COLOR" in kwargs["env"]
            assert kwargs["env"]["NO_COLOR"] == "true"
            assert "capture_output" in kwargs
            assert kwargs["capture_output"] is True
            assert "shell" in kwargs
            assert kwargs["shell"] is True

            class ReturnObject():
                pass
            o = ReturnObject()
            setattr(o, "returncode", 252)  # noqa: B010
            setattr(o, "stdout", b"")  # noqa: B010
            setattr(o, "stderr", b"error: foo")  # noqa: B010

            return o

        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setitem(
            obj.run.__globals__,
            "subprocess_run",
            mock_subprocess_run,
        )

        err = None
        with pytest_raises(AssertionError):
            try:
                _ = obj.run(["echo", "foo"])
            except Exception as e:
                err = e
                raise

        assert isinstance(err, AssertionError)
        assert err.args[0] == b"error: foo"

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_success(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during a successful test.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_success__empty_args(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during a successful test.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run([])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_success__no_args(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during a successful test.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run()

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_assert_pass(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during a successful test,
            using our shell test harness's assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_assert_fail(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during a failed test,
            using our shell test harness's assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        err = None
        with pytest_raises(AssertionError):
            try:
                _ = obj.run(["echo", "foo"])
            except Exception as e:
                err = e
                raise

        assert isinstance(err, AssertionError)
        assert err.args[0] == b"FATAL: expected: asdf is not empty string"

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___main_invoked(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during invoking a script
            with a __main.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 151  # RET_ERROR_SCRIPT_WAS_NOT_SOURCED
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should be sourced\n"
            in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___main(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __main but setting _CALL_MAIN_ANYWAY.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 151  # RET_ERROR_SCRIPT_WAS_NOT_SOURCED
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should be sourced\n"
            in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___main_overridden(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __main but setting _CALL_MAIN_ANYWAY using default
            monkeypatch.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___main_overridden_custom(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __main but setting _CALL_MAIN_ANYWAY.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: manually overridden __main was called\n"
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___sourced_main(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __sourced_main.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 149  # RET_ERROR_SCRIPT_WAS_SOURCED
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___sourced_main_overridden(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __sourced_main using default monkeypatch.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell___sourced_main_overridden_custom(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            with a __sourced_main using custom monkeypatch.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: manually overridden __sourced_main was called"  # noqa: E501,W505,B950
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_public_function(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a public function.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            not in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_public_function_overridden(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a public function that is monkeypatched.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: overridden public_function"
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_public_function_overridden_assert_pass(  # noqa: E501,W505,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a public function that is monkeypatched and has a passing
            assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: overridden public_function"
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_public_function_overridden_assert_fail(  # noqa: E501,W505,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a public function that is monkeypatched and has a failing
            assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        err = None
        with pytest_raises(AssertionError):
            try:
                _ = obj.run(["echo", "foo"])
            except Exception as e:
                err = e
                raise

        assert isinstance(err, AssertionError)
        assert err.args[0] == b"FATAL: expected: asdf is not empty string"

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_private_function(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a private function.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            not in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_private_function_overridden(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a private function that is monkeypatched.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: overridden private_function"
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_private_function_overridden_assert_pass(  # noqa: E501,W505,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a private function that is monkeypatched and has a passing
            assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert (
            b"PytestShellScriptTestHarness: 0 echo foo\n"
            in p.stdout
        )
        assert (
            b"PytestShellScriptTestHarness: overridden private_function"
            in p.stdout
        )
        assert (
            b"ULTRADEBUG: example_shell_script.sh called with 'echo foo'\n"
            not in p.stdout
        )
        assert (
            b"FATAL: example_shell_script.sh should not be sourced\n"
            not in p.stderr
        )

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_private_function_overridden_assert_fail(  # noqa: E501,W505,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell during sourcing a script
            calling a private function that is monkeypatched and has a failing
            assert.

        Args:
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        err = None
        with pytest_raises(AssertionError):
            try:
                _ = obj.run(["echo", "foo"])
            except Exception as e:
                err = e
                raise

        assert isinstance(err, AssertionError)
        assert err.args[0] == b"FATAL: expected: asdf is not empty string"

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell adding an environment
        variable via monkeypatch.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("TEST_ENV_VAR", "ADDED")

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell overwriting an environment
        variable via monkeypatch.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("_IS_UNDER_TEST", "alt")

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_remove(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell removing an environment
        variable via monkeypatch.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.delenv("_IS_UNDER_TEST")

        p = obj.run(["echo", "foo"])

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_harness_add(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell adding an environment
        variable via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"TEST_ENV_VAR_2": "ADDED"},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_harness_overwrite(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell overwriting an environment
        variable via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"_IS_UNDER_TEST": "alt"},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_harness_remove(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell removing an environment
        variable via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"_IS_UNDER_TEST": None},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_harness_remove_non_existing(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell removing an environment
        variable via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"___ENV_VAR_THAT_SHOULD_NOT_EXIST": None},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_add(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell adding an environment
        variable via monkeypatch and a adding second environment variable via
        harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("TEST_ENV_VAR", "ADDED")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"TEST_ENV_VAR_2": "ADDED"},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_overwrite(  # noqa: E501,W505,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell adding an environment
        variable via monkeypatch and overwriting it via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("TEST_ENV_VAR", "ADDED")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"TEST_ENV_VAR": "OVERWRITTEN"},
        )

        assert p.returncode == 0
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_remove(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell adding an environment
        variable via monkeypatch and removing it via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("TEST_ENV_VAR", "ADDED")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"TEST_ENV_VAR": None},
        )

        assert p.returncode == 0
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite_harness_overwrite(  # noqa: E501,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell overwriting an environment
        variable via monkeypatch and overwriting it via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("_IS_UNDER_TEST", "alt")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"_IS_UNDER_TEST": "alt2"},
        )

        assert p.returncode == 0
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite_harness_remove(  # noqa: E501,B950
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell overwriting an environment
        variable via monkeypatch and removing it via harness.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.setenv("_IS_UNDER_TEST", "alt")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"_IS_UNDER_TEST": None},
        )

        assert p.returncode == 0
        assert b"error: " not in p.stderr

    #---------------------------------------------------------------------------
    def test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_remove_harness_add(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::run with shell removing an environment
        variable via monkeypatch.

        Args:
            request (pytest_FixtureRequest): pytest Request fixture
            monkeypatch (pytest_MonkeyPatch): pytest MonkeyPatch fixture
        """
        obj = pytest_shell_script_test_harness_PytestShellScriptTestHarness(
            mock_repo,
            request=request,
            tmp_path_factory=tmp_path_factory,
        )

        monkeypatch.delenv("_IS_UNDER_TEST")

        p = obj.run(
            ["echo", "foo"],
            additional_env_vars={"_IS_UNDER_TEST": "alt2"},
        )

        assert p.returncode == 0
        assert b"foo\n" in p.stdout
        assert b"error: " not in p.stderr

#endregion PytestShellScriptTestHarness::run
################################################################################

################################################################################
#region PytestShellScriptTestHarness::isActuallyWindowsFileSystem

class Test_PytestShellScriptTestHarness_isActuallyWindowsFileSystem():
    """
    Test PytestShellScriptTestHarness::isActuallyWindowsFileSystem function.
    """

    @pytest_mark.parametrize(
        (
            "mock_uname_dict," +
            "mock_uname_dict_expected_result"
        ),
        [
            # macOS Apple Silicon
            pytest_param(
                {
                    "system": "Darwin",
                    "node": "my-machine",
                    "release": "21.6.0",
                    "version": (
                        "Darwin Kernel Version 21.6.0: " +
                        "Wed Aug 10 14:28:23 PDT 2022; " +
                        "root:xnu-8020.141.5~2/RELEASE_ARM64_T6000"
                    ),
                    "machine": "arm64",
                },
                False,
                id="macOSAppleSilicon",
            ),
            # macOS Intel
            pytest_param(
                {
                    "system": "Darwin",
                    "node": "my-machine",
                    "release": "11.0.0",
                    "version": (
                        "Darwin Kernel Version 11.0.0 " +
                        "Sat Jun 18 12:56:35 PDT 2011; " +
                        "root:xnu-1699.22.73~1/RELEASE_X86_64"
                    ),
                    "machine": "x86_64",
                },
                False,
                id="macOSIntel",
            ),
            # Linux AMD
            pytest_param(
                {
                    "system": "Linux",
                    "node": "my-machine",
                    "release": "2.6.32-21-generic",
                    "version": (
                        "2.6.32-21-generic #32-Ubuntu SMP " +
                        "Fri Apr 16 08:09:38 UTC 2010"
                    ),
                    "machine": "x86_64",
                },
                False,
                id="LinuxAMD",
            ),
            # Linux Intel
            pytest_param(
                {
                    "system": "Linux",
                    "node": "my-machine",
                    "release": "2.6.18-194.e15PAE",
                    "version": (
                        "2.6.18-194.e15PAE #1 SMP " +
                        "Fri Apr 2 15:37:44 EDT 2010 i686"
                    ),
                    "machine": "i686",
                },
                False,
                id="LinuxIntel",
            ),
            # WSL1 Intel
            pytest_param(
                {
                    "system": "Linux",
                    "node": "my-machine",
                    "release": "4.4.0-19041-Microsoft",
                    "version": (
                        "4.4.0-19041-Microsoft #1-Microsoft " +
                        "Sat Sep 11 14:32:00 PST 2021"
                    ),
                    "machine": "x86_64",
                },
                True,
                id="WSL1Intel",
            ),
            # WSL2 Intel
            pytest_param(
                {
                    "system": "Linux",
                    "node": "my-machine",
                    "release": "2.6.32-21-microsoft-standard-WSL2",
                    "version": (
                        "2.6.32-21-microsoft-standard-WSL2 #1-Microsoft " +
                        "Sat Sep 11 14:32:00 PST 2021"
                    ),
                    "machine": "x86_64",
                },
                True,
                id="WSL2Intel",
            ),
        ],
    )
    @pytest_mark.parametrize(
        (
            "mock_subprocess_return_code," +
            "mock_subprocess_return_code_expected_result"
        ),
        [
            pytest_param(
                0,  # mounts of C:\ exist
                True,
                id="mountRet0",
            ),
            pytest_param(
                1,  # mounts of C:\ do NOT exist
                False,
                id="mountRet1",
            ),
            pytest_param(
                -1,  # there was an Exception
                False,
                id="mountRetNeg1",
            ),
        ],
    )
    @pytest_mark.parametrize(
        (
            "mock_real_platform," +
            "mock_real_platform_expected_result"
        ),
        [
            pytest_param(
                "Linux",
                False,
                id="PlatformLinux",
            ),
            pytest_param(
                "Darwin",
                False,
                id="PlatformDarwin",
            ),
            pytest_param(
                "MINGW64NT",  # "Windows
                True,
                id="PlatformMINGW64NT",
            ),
        ],
    )
    @pytest_mark.parametrize(
        (
            "mock_wsl_distro_name," +
            "mock_wsl_distro_name_expected_result"
        ),
        [
            pytest_param(
                "",
                False,
                id="DistroEmpty",
            ),
            pytest_param(
                "NotEmpty",  # e.g. Ubuntu, Debian, CentOS, etc
                True,
                id="DistroNotEmpty",
            ),
        ],
    )
    def test_PytestShellScriptTestHarness_isActuallyWindowsFileSystem(
        self,
        mock_uname_dict: Dict[str, str],
        mock_uname_dict_expected_result: bool,
        mock_subprocess_return_code: int,
        mock_subprocess_return_code_expected_result: bool,
        mock_real_platform: str,
        mock_real_platform_expected_result: bool,
        mock_wsl_distro_name: str,
        mock_wsl_distro_name_expected_result: bool,
        monkeypatch: pytest_MonkeyPatch,
    ) -> None:
        """
        Test PytestShellScriptTestHarness::isActuallyWindowsFileSystem when
        """
        # if any of the expected results are True,
        # then the final expected result is also True
        expected_result = (
            mock_uname_dict_expected_result or
            mock_subprocess_return_code_expected_result or
            mock_real_platform_expected_result or
            mock_wsl_distro_name_expected_result
        )

        mock_uname_dict_copy = copy_deepcopy(mock_uname_dict)

        def mock_platform_uname() -> platform_uname_result:
            if (
                packaging_version.parse(platform_python_version()) <
                packaging_version.parse("3.9")
            ):  # pragma: no cover
                mock_uname_dict_copy["processor"] = "cpu"

            return platform_uname_result(**mock_uname_dict_copy)

        monkeypatch.setitem(
            (
                pytest_shell_script_test_harness_PytestShellScriptTestHarness\
                    .isActuallyWindowsFileSystem.__globals__
            ),
            "platform_uname",
            mock_platform_uname,
        )

        def mock_subprocess_call(*args: Any, **kwargs: Any) -> int:
            # silence the "variable not used" complaints in function signature
            args = args  # noqa: F841  # pylint: disable=self-assigning-variable
            kwargs = kwargs  # noqa: F841  # pylint: disable=self-assigning-variable

            if mock_subprocess_return_code == -1:
                raise Exception("generic unit test exception")
            return mock_subprocess_return_code

        monkeypatch.setitem(
            (
                pytest_shell_script_test_harness_PytestShellScriptTestHarness\
                    .isActuallyWindowsFileSystem.__globals__
            ),
            "subprocess_call",
            mock_subprocess_call,
        )

        monkeypatch.setenv("REAL_PLATFORM", mock_real_platform)
        monkeypatch.setenv("WSL_DISTRO_NAME", mock_wsl_distro_name)

        res = pytest_shell_script_test_harness_PytestShellScriptTestHarness\
            .isActuallyWindowsFileSystem()

        assert res is expected_result

#endregion PytestShellScriptTestHarness::isActuallyWindowsFileSystem
################################################################################
