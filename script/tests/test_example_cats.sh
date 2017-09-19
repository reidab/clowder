#!/usr/bin/env bash

# set -xv

echo 'TEST: cats example test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

if [ -n "$TRAVIS_OS_NAME" ]; then
    if [ "$TRAVIS_OS_NAME" = "osx" ]; then
        "$TEST_SCRIPT_DIR/unittests.sh" || exit 1
    fi
else
    setup_local_test_directory
    "$TEST_SCRIPT_DIR/unittests.sh" "$CATS_EXAMPLE_DIR" || exit 1
fi

cd "$CATS_EXAMPLE_DIR" || exit 1

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_clowder_version

"$TEST_SCRIPT_DIR/tests/test_cats_init.sh"
"$TEST_SCRIPT_DIR/tests/test_command.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_status.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_clean.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_herd.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_forall.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_save.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_stash.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_link.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_yaml_validation.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_start.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_prune.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_repo.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_import.sh"

test_help() {
    print_separator

    clowder repo checkout master || exit 1

    clowder link -v 'missing-defaults'
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"

    clowder link
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"
}
test_help
