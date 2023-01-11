"""
src/pytest_shell_script_test_harness/__impl.py (pytest-shell-script-test-harness)
"""  # noqa: E501,W505,B950
################################################################################
#region Python Library Preamble

# we know that the repo path is ./../../ b/c we should be in ./src/<project name>/
import os.path as os_path
MY_DIR_FULLPATH = os_path.dirname(__file__)
MY_REPO_FULLPATH = os_path.dirname(os_path.dirname(MY_DIR_FULLPATH))
del os_path

from logging import (  # noqa: F401
    FATAL                           as logging_FATAL,
    getLogger                       as logging_getLogger,
)
logger = logging_getLogger(__name__)
logger_log = logger.log

#endregion Python Library Preamble
################################################################################

###############################################################################
#region Imports

#===============================================================================
#region stdlib

from os import (
    chmod                           as os_chmod,
    environ                         as os_environ,
    mkdir                           as os_mkdir,
)
from os.path import (
    abspath                         as os_path_abspath,
    basename                        as os_path_basename,
    dirname                         as os_path_dirname,
    exists                          as os_path_exists,
    join                            as os_path_join,
    sep                             as os_path_sep,
)
from platform import (
    uname                           as platform_uname,
)
from shlex import (
    join                            as shlex_join,
    quote                           as shlex_quote,
)
from shutil import (
    copytree                        as shutil_copytree,
)
from subprocess import (  # noqa: F401  # nosec
    call                            as subprocess_call,
    CompletedProcess                as subprocess_CompletedProcess,
    run                             as subprocess_run,
)
import sys
from typing import (
    Any,
    List,
    Dict,
    Optional,
    Union,
)

#endregion stdlib
#===============================================================================

#===============================================================================
#region third party

from coverage.plugin_support import (  # type: ignore
    Plugins                         as coverage_plugin_support_Plugins,  # type: ignore
)
import pytest
from pytest import (
    FixtureRequest                  as pytest_FixtureRequest,
    MonkeyPatch                     as pytest_MonkeyPatch,
    TempPathFactory                 as pytest_TempPathFactory,
)

#endregion third party
#===============================================================================

#===============================================================================
#region ours

try:
    from .coverage_plugin import (  # pylint: disable=useless-import-alias
        CoverageShellScriptPlugin as CoverageShellScriptPlugin,
    )
except ImportError:  # pragma: no cover
    sys.path.insert(0, os_path_dirname(__file__))
    from coverage_plugin import (  # type: ignore  # pylint: disable=useless-import-alias
        CoverageShellScriptPlugin as CoverageShellScriptPlugin,  # type: ignore
    )

#endregion ours
#===============================================================================

#endregion Imports
################################################################################

################################################################################
#region Public Functions

def coverage_init(
    reg: coverage_plugin_support_Plugins,  # type: ignore
    options: Dict[str, Any],
) -> None:
    """
    _summary_

    Args:
        reg (coverage_plugin_support_Plugins): _description_
        options (Dict[str, Any]): _description_
    """
    plugin = CoverageShellScriptPlugin(options)  # type: ignore
    reg.add_file_tracer(plugin)  # type: ignore
    reg.add_configurer(plugin)  # type: ignore

#endregion Public Functions
################################################################################

################################################################################
#region Public Classes

#===============================================================================
class PytestShellScriptTestHarness:
    """
    Test Harness for running unit tests against shell scripts.
    """

    #---------------------------------------------------------------------------
    def __init__(
        self,
        mock_repo: str,  # pylint: disable=redefined-outer-name
        request: pytest_FixtureRequest,
        tmp_path_factory: pytest_TempPathFactory,
    ) -> None:
        """
        Initialize.
        """
        super().__init__()
        self.mock_repo = mock_repo
        self.request = request
        self.tmp_path_factory = tmp_path_factory

    #---------------------------------------------------------------------------
    def run(
        self,
        additional_args: Optional[List[Union[str, int]]] = None,
        additional_env_vars: Optional[Dict[str, Optional[str]]] = None,
        use_bfi_run: bool = True,
    ) -> "subprocess_CompletedProcess[bytes]":
        """
        Call the matching shell func in .sh file with same name as this .py file.

        Args:
            additional_args (Optional[List[str]], optional): list of args for shell
                function. Defaults to None.

        Returns:
            subprocess_CompletedProcess[bytes]: process object from subprocess
        """
        if additional_args is None:
            additional_args = []
        if additional_env_vars is None:
            additional_env_vars = {}

        mock_repo_fullpath = self.mock_repo

        export_filepath = os_path_join(
            mock_repo_fullpath,
            "_pssth-exports.sh",
        )
        # mock repo project's run.sh
        run_sh_fullpath = os_path_join(
            mock_repo_fullpath,
            "run.sh",
        )
        # path to the actual script file we will run
        final_script_path = os_path_join(
            mock_repo_fullpath,
            "_pssth-test.sh",
        )

        # pass along our entire environment + OMEGA_DEBUG=all
        env: Dict[str, Any] = {}
        k: str
        v: Optional[str]
        for k, v in os_environ.items():
            env[k] = v
        env["OMEGA_DEBUG"] = "all"
        env["NO_COLOR"] = "true"
        env["_PSSTH"] = "true"
        env["_PSSTH_EXECUTOR"] = final_script_path
        env["DO_SET_X_RUN"] = "true"
        if os_path_exists(run_sh_fullpath) and use_bfi_run:
            env["_PSSTH_EXECUTOR"] = run_sh_fullpath
        for k, v in additional_env_vars.items():
            env[k] = v

        quoted_env: List[str] = []
        for k, v in env.items():
            if v is not None:
                quoted_env.append(f"{k}={shlex_quote(str(v))}")
                quoted_env.append(f"export {k}")
            else:
                quoted_env.append(f"unset {k}")

        quoted_env_str = "\n".join(quoted_env)

        # write out exports data to be sourced by the postamble later
        export_file = None
        try:
            export_file = open(export_filepath, "w", encoding="utf8")
            _ = export_file.write(quoted_env_str)
            export_file.flush()
        finally:
            if export_file is not None:
                export_file.close()

        # path to test script file we are supposed to run
        original_script_path = os_path_join(
            self.request.node.fspath.dirname,
            f"{self.request.node.fspath.purebasename}.sh",
        )
        original_script_file = open(original_script_path, "rb")
        original_script_data = original_script_file.read()
        original_script_file.close()

        # build the actual script file we will run
        out_file = open(final_script_path, "wb")

        preamble_filepath = os_path_join(
            MY_DIR_FULLPATH,
            "resources",
            "preamble.sh",
        )
        preamble_file = open(preamble_filepath, "rb")
        preamble_data = preamble_file.read()
        preamble_file.close()

        postamble_filepath = os_path_join(
            MY_DIR_FULLPATH,
            "resources",
            "postamble.sh",
        )
        postamble_file = open(postamble_filepath, "rb")
        postamble_data = postamble_file.read()
        postamble_file.close()

        _ = out_file.write(preamble_data)
        _ = out_file.write(original_script_data)
        _ = out_file.write(postamble_data)

        out_file.flush()
        out_file.close()

        os_chmod(final_script_path, 0o755)  # nosec

        # build up command to run
        cmd: List[str] = []

        if os_path_exists(run_sh_fullpath) and use_bfi_run:
            cmd.append(run_sh_fullpath)

        cmd.extend([
            final_script_path,
            f"{self.request.cls.__name__}__{self.request.function.__name__}",  # type: ignore[reportUnknownMemberType]  # noqa: E501,B950
        ])

        str_additional_args = [str(x) for x in additional_args]
        if str_additional_args:
            cmd.extend(str_additional_args)

        cmd_str = shlex_join(cmd)

        print(f"Running Command:\n{cmd_str}\n")

        p = subprocess_run(
            cmd_str,
            capture_output=True,
            cwd=mock_repo_fullpath,
            shell=True,  # nosec
            env={
                "OMEGA_DEBUG": "all",
                # "DO_SET_X_RUN": "true",
            },
        )

        print(f"\nRaw stdout bytes:\n{repr(p.stdout)}\n")
        print(f"\nRaw stderr bytes:\n{repr(p.stderr)}\n")
        print(f"\nstdout:\n{str(p.stdout)}\n")
        print(f"\nstderr:\n{str(p.stderr)}\n")
        print(f"\nReturn Code: {p.returncode}\n")

        if p.returncode == 252:
            raise AssertionError(p.stderr.strip().split(b"\n")[-1])

        return p

    @staticmethod
    def isActuallyWindowsFileSystem() -> bool:
        """
        Check if we are probably actually on Windows.

        Returns:
            bool: true if Windowsy, false if not Windowsy
        """
        platform_uname_str = " ".join(platform_uname()).casefold()
        if (
            any(
                x in platform_uname_str
                for x in ["microsoft", "wsl"]
            ) or
            os_environ.get("REAL_PLATFORM", "") == "MINGW64NT" or
            os_environ.get("WSL_DISTRO_NAME", "") != ""
        ):
            return True

        # we don't care if this fails b/c if it does,
        # we've got many other problems
        windows_fs = 1  # 1 is False
        try:
            windows_fs = subprocess_call(  # nosec
                "mount | grep -e '[A-Z]:\\\\'",
                shell=True,
            )
        except Exception:  # pylint: disable=broad-except # noqa: E722 # nosec
            pass
        if windows_fs == 0:
            return True

        return False

#endregion Public Classes
################################################################################

################################################################################
#region Fixtures

#-------------------------------------------------------------------------------
@pytest.fixture(name="shell_script_test_harness")
def shell_script_test_harness(
    mock_repo: str,  # pylint: disable=redefined-outer-name
    request: pytest_FixtureRequest,
    tmp_path_factory: pytest_TempPathFactory,
) -> PytestShellScriptTestHarness:
    """
    Fixture wrapper for PytestShellScriptTestHarness.

    Args:
        tmp_path_factory (pytest_TempPathFactory): pytest tmp_path_factory fixture

    Returns:
        PytestShellScriptTestHarness: PytestShellScriptTestHarness instance.
    """
    return PytestShellScriptTestHarness(
        mock_repo=mock_repo,
        request=request,
        tmp_path_factory=tmp_path_factory,
    )

#-------------------------------------------------------------------------------
@pytest.fixture(name="shell_script")
def shell_script(shell_script_test_harness):  # type: ignore  # noqa  # pylint: disable=all
    yield shell_script_test_harness

#-------------------------------------------------------------------------------
@pytest.fixture
def mock_repo(
    monkeypatch: pytest_MonkeyPatch,
    request: pytest_FixtureRequest,
    tmp_path_factory: pytest_TempPathFactory,
) -> str:
    """
    Create a mock repo to use that looks like a repo that uses
        pytest-shell-script-test-harness, but also named
        pytest-shell-script-test-harness so we can re-use the already available
        conda environment.

    Args:
        monkeypatch (pytest_MonkeyPatch): pytest monkeypatch fixture
        tmp_path_factory (pytest_TempPathFactory): pytest tmp_path_factory fixture

    Returns:
        str: path of mock repo
    """
    node_safe_name = request.node.name\
        .replace("[", "-")\
        .replace("]", "-")

    tempdir = tmp_path_factory.mktemp(node_safe_name, numbered=True)
    monkeypatch.chdir(tempdir)

    # "a.b.c.d" ->
    # 4
    subfolder_depth = len(request.module.__name__.split("."))  # type: ignore[reportUnknownMemberType]  # noqa: E501,B950
    # "/path/to/repo/a/b/c/d" ->
    # "/path/to/repo"
    repo_fullpath = os_path_join(
        "/",
        *request.module.__file__.split(os_path_sep)[:(-1 * subfolder_depth)],  # type: ignore[reportUnknownArgumentType]  # noqa: E501,B950
    )

    # "/path/to/repo" ->
    # "repo"
    repo_name = os_path_basename(repo_fullpath)

    # # "/path/to/repo" ->
    # # "/path/to/repo/src"
    # repo_src_fullpath = os_path_join(
    #     repo_fullpath,
    #     "src",
    # )

    # # "/path/to/repo" ->
    # # "/path/to/repo/bin"
    # repo_bin_fullpath = os_path_join(
    #     repo_fullpath,
    #     "bin",
    # )

    mock_repo_fullpath: str = os_path_abspath(repo_name)

    os_mkdir(mock_repo_fullpath)
    monkeypatch.chdir(mock_repo_fullpath)

    # # write a pyproject.toml for the mock repo
    # with open("pyproject.toml", "w", encoding="utf-8") as f:
    #     _ = f.write("""\
    #             name = "template_project"
    #             version = "0.0.0"
    #             description = "A template project."
    #         """)
    #     f.flush()

    # # copy src/** into mock repo
    # mock_src_fullpath = os_path_join(
    #     mock_repo_fullpath,
    #     "src",
    # )
    # if os_path_exists(repo_src_fullpath):
    #     shutil_copytree(
    #         repo_src_fullpath,
    #         mock_src_fullpath,
    #         dirs_exist_ok=True,
    #         symlinks=True,
    #         ignore_dangling_symlinks=True,
    #     )

    # # copy src/** into mock repo
    # mock_bin_fullpath = os_path_join(
    #     mock_repo_fullpath,
    #     "bin",
    # )
    # if os_path_exists(repo_bin_fullpath):
    #     shutil_copytree(
    #         repo_bin_fullpath,
    #         mock_bin_fullpath,
    #         symlinks=True,
    #         ignore_dangling_symlinks=True,
    #         dirs_exist_ok=True,
    #     )

    shutil_copytree(
        repo_fullpath,
        mock_repo_fullpath,
        symlinks=True,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    # # copy the test .sh into mock repo
    # shell_harness_path = os_path_join(
    #     request.node.fspath.dirname,
    #     f"{request.node.fspath.purebasename}.sh",
    # )
    # if os_path_exists(shell_harness_path):  # pragma: no branch
    #     shutil_copy2(
    #         shell_harness_path,
    #         mock_repo_fullpath,
    #     )

    return mock_repo_fullpath

#endregion Fixtures
################################################################################

################################################################################
#region Private Functions

#-------------------------------------------------------------------------------
def __main(argv: List[str]) -> int:
    """
    Entry point.

    Args:
        argv (list[str]): command line arguments

    Returns:
        int: return code
    """
    # ignore unused vars from func signature
    argv = argv  # pylint: disable=self-assigning-variable

    logger_log(logging_FATAL, "This module should not be run directly.")

    return 1

#endregion Private Functions
################################################################################

################################################################################
#region Immediate

if __name__ == "__main__":  # pragma: no cover
    __ret = __main(sys.argv[1:])  # pylint: disable=invalid-name
    sys.exit(__ret)

#endregion Immediate
################################################################################
