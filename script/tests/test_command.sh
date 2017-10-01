#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Clowder command"

test_command() {
    print_single_separator
    echo "TEST: Fail with unrecognized command"
    clowder cat && exit 1
    echo "TEST: Fail with no arguments"
    clowder && exit 1
    echo ''
}
test_command
