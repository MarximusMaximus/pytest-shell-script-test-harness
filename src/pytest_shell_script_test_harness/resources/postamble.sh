#!/usr/bin/env sh

# TODO: do we need all or parts of marximus-shell-extensions Postamble here?

################################################################################
#region pytest-shell-script-test-harness Test Postamble

func_to_call="$1"
shift
(
    # call ensure_include_GXY ./_pssth-exports.sh
    command printf "Calling shell func '%s' with args '%s'\n" "${func_to_call}" "$*"
    call "${func_to_call}" "$@"
    ret=$?
    command printf "func return code was %s\n" "$ret"
    exit "$ret"
)
ret=$?
exit "$ret"

#endregion pytest-shell-script-test-harness Test Postamble
################################################################################
