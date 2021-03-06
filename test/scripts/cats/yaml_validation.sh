#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

print_double_separator
echo "TEST: Test yaml validation"

test_invalid_yaml() {
    pushd .clowder/versions || exit 1
    test_cases=( $(ls -d test-*) )
    popd || exit 1

    for test in "${test_cases[@]}"
    do
        $COMMAND link -v $test || exit 1
        print_single_separator
        $COMMAND herd
        exit_code=$?
        if [ "$exit_code" != '42' ]; then
            exit 1
        fi
        print_single_separator
        rm clowder.yaml || exit 1
    done
}
test_invalid_yaml
