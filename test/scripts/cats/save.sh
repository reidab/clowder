#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
$COMMAND herd $PARALLEL || exit 1

print_double_separator
echo "TEST: Test clowder save"

test_save() {
    print_single_separator
    echo "TEST: Fail linking a previously saved version that doesn't exist"
    $COMMAND link -v v100 && exit 1
    echo "TEST: Fail saving a previously saved version"
    $COMMAND save v0.1 && exit 1
    echo "TEST: Fail saving a saved version named 'default'"
    $COMMAND save default && exit 1
    $COMMAND save DEFAULT && exit 1
    echo "TEST: Successfully save a new version"
    $COMMAND save v0.11 || exit 1
    echo "TEST: Successfully save version with path separator in input name"
    $COMMAND save path/separator || exit 1
    $COMMAND link -v path-separator || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status || exit 1
}
test_save

test_save_missing_directories() {
    print_single_separator
    echo "TEST: Remove directories"
    rm -rf "$@"
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    echo "TEST: Fail saving version with missing directories"
    $COMMAND save missing-directories && exit 1
    echo ''
}
test_save_missing_directories 'duke' 'mu'
