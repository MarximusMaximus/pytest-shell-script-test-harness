#!/usr/bin/env sh

################################################################################
#region PytestShellScriptTestHarness Test Postamble

func_to_call="$1"
shift
(
    command printf "Calling shell func '%s' with args '%s'\n" "${func_to_call}" "$*"
    "${func_to_call}" "$@"
    ret=$?
    command printf "func return code was %s\n" "$ret"
    exit $ret
)
ret=$?
exit $ret

#endregion PytestShellScriptTestHarness Test Postamble
################################################################################
