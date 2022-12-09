#!/usr/bin/env sh

################################################################################
#region Tests

#===============================================================================
#region Test_PytestShellScriptTestHarness__run


#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__success()
{
    # this shouldn't get called due to mock_subprocess_run, fail if it is
    exit 1
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__assert() {
    # this shouldn't get called due to mock_subprocess_run, fail if it is
    exit 1
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_success() {
    (
        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_success__empty_args() {
    (
        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_success__no_args() {
    (
        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_assert_pass() {
    (
        command printf "foo\n"

        script_ret=0

        # shellcheck disable=SC2050
        assert [ "asdf" = "asdf" ] \
            "asdf is not asdf string"

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_assert_fail() {
    (
        script_ret=0

        # shellcheck disable=SC2050
        assert [ "asdf" = "" ] \
            "asdf is not empty string"

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___main_invoked() {
    (
        invoke ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___main() {
    (
        _CALL_MAIN_ANYWAY=true
        export _CALL_MAIN_ANYWAY

        inject_monkeypatch() { true; }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___main_overridden() {
    (
        _CALL_MAIN_ANYWAY=true
        export _CALL_MAIN_ANYWAY

        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___main_overridden_custom() {
    (
        _CALL_MAIN_ANYWAY=true
        export _CALL_MAIN_ANYWAY

        inject_monkeypatch() {
            __main() {
                test_harness_output "manually overridden __main was called"
                return 0
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___sourced_main() {
    (
        inject_monkeypatch() { true; }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___sourced_main_overridden() {
    (
        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell___sourced_main_overridden_custom() {
    (
        inject_monkeypatch() {
            __sourced_main() {
                test_harness_output "manually overridden __sourced_main was called"
                return 0
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_public_function() {
    (
        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        if [ "${script_ret}" -ne 0 ]; then
            exit $script_ret
        fi

        public_function 0 "$@"
        func_ret=$?
        exit $func_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_public_function_overridden() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            public_function() {
                test_harness_output "$*"
                test_harness_output "overridden public_function"
                return "$1"
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        if [ "${script_ret}" -ne 0 ]; then
            exit $script_ret
        fi

        public_function 0 "$@"
        func_ret=$?
        exit $func_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_public_function_overridden_assert_pass() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            public_function() {
                test_harness_output "$*"
                test_harness_output "overridden public_function"

                # shellcheck disable=SC2050
                assert [ "asdf" = "asdf" ] \
                    "asdf is not asdf string"

                return "$1"
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        if [ "${script_ret}" -ne 0 ]; then
            exit $script_ret
        fi

        public_function 0 "$@"
        func_ret=$?
        exit $func_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_public_function_overridden_assert_fail() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            public_function() {
                test_harness_output "$*"
                test_harness_output "overridden public_function"

                # shellcheck disable=SC2050
                assert [ "asdf" = "" ] \
                    "asdf is not empty string"

                return "$1"
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        if [ "${script_ret}" -ne 0 ]; then
            exit $script_ret
        fi

        public_function 0 "$@"
        func_ret=$?
        exit $func_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_private_function() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            __sourced_main() {
                private_function 0 "$@"
                ret=$?
                return $ret
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_private_function_overridden() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            private_function() {
                test_harness_output "$*"
                test_harness_output "overridden private_function"
                return "$1"
            }

            __sourced_main() {
                private_function 0 "$@"
                ret=$?
                return $ret
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_private_function_overridden_assert_pass() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            private_function() {
                test_harness_output "$*"
                test_harness_output "overridden private_function"

                # shellcheck disable=SC2050
                assert [ "asdf" = "asdf" ] \
                    "asdf is not asdf string"

                return "$1"
            }

            __sourced_main() {
                private_function 0 "$@"
                ret=$?
                return $ret
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_private_function_overridden_assert_fail() {
    (
        inject_monkeypatch() {
            default_inject_monkeypatch

            private_function() {
                test_harness_output "$*"
                test_harness_output "overridden private_function"

                # shellcheck disable=SC2050
                assert [ "asdf" = "" ] \
                    "asdf is not empty string"

                return "$1"
            }

            __sourced_main() {
                private_function 0 "$@"
                ret=$?
                return $ret
            }
        }

        include_G ./example_shell_script.sh "$@"
        script_ret=$?
        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add() {
    (
        assert [ "$TEST_ENV_VAR" = "ADDED" ] \
            "TEST_ENV_VAR was not 'ADDED' was $TEST_ENV_VAR"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite() {
    (
        assert [ "$_IS_UNDER_TEST" = "alt" ] \
            "_IS_UNDER_TEST was not 'alt' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_remove() {
    (
        assert [ "$_IS_UNDER_TEST" = "" ] \
            "_IS_UNDER_TEST was not '' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_harness_add() {
    (
        assert [ "$TEST_ENV_VAR_2" = "ADDED" ] \
            "TEST_ENV_VAR_2 was not 'ADDED' was $TEST_ENV_VAR_2"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_harness_overwrite() {
    (
        assert [ "$_IS_UNDER_TEST" = "alt" ] \
            "_IS_UNDER_TEST was not 'alt' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_harness_remove() {
    (
        assert [ "$_IS_UNDER_TEST" = "" ] \
            "_IS_UNDER_TEST was not '' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_harness_remove_non_existing() {
    (
        assert [ "$___ENV_VAR_THAT_SHOULD_NOT_EXIST" = "" ] \
            "___ENV_VAR_THAT_SHOULD_NOT_EXIST was not '' was $___ENV_VAR_THAT_SHOULD_NOT_EXIST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_add() {
    (
        assert [ "$TEST_ENV_VAR" = "ADDED" ] \
            "TEST_ENV_VAR was not 'ADDED' was $TEST_ENV_VAR"

        assert [ "$TEST_ENV_VAR_2" = "ADDED" ] \
            "TEST_ENV_VAR_2 was not 'ADDED' was $TEST_ENV_VAR_2"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_overwrite() {
    (
        assert [ "$TEST_ENV_VAR" = "OVERWRITTEN" ] \
            "TEST_ENV_VAR was not 'OVERWRITTEN' was $TEST_ENV_VAR"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_add_harness_remove() {
    (
        assert [ "$TEST_ENV_VAR" = "" ] \
            "TEST_ENV_VAR was not '' was $TEST_ENV_VAR"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite_harness_overwrite() {
    (
        assert [ "$_IS_UNDER_TEST" = "alt2" ] \
            "_IS_UNDER_TEST was not 'alt2' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_overwrite_harness_remove() {
    (
        assert [ "$_IS_UNDER_TEST" = "" ] \
            "_IS_UNDER_TEST was not '' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#-------------------------------------------------------------------------------
Test_PytestShellScriptTestHarness__run__test_PytestShellScriptTestHarness__run__shell_env_monkeypatch_remove_harness_add() {
    (
        assert [ "$_IS_UNDER_TEST" = "alt2" ] \
            "_IS_UNDER_TEST was not 'alt2' was $_IS_UNDER_TEST"

        command printf "foo\n"

        script_ret=0

        exit $script_ret
    )
}

#endregion Test_PytestShellScriptTestHarness__run
#===============================================================================

#endregion Tests
################################################################################
