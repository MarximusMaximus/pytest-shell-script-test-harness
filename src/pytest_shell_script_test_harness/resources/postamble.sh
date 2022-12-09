#!/usr/bin/env sh

################################################################################
#region PytestShellScriptTestHarness Test Postamble

# HACK: for some reason we're losing the command line args, so let's re-instate them
OLDIFS="$IFS"
IFS=$(printf "\n\t")
# shellcheck disable=SC2086
set -- $COMMANDLINE_ARGS
IFS="$OLDIFS"

func_to_call="$1"
shift
(
    command printf "Calling shell func '%s'\n" "${func_to_call}"
    "${func_to_call}" "$@"
    ret=$?
    command printf "func return code was %s\n" "$ret"
    exit $ret
)
ret=$?
exit $ret

#endregion PytestShellScriptTestHarness Test Postamble
################################################################################
