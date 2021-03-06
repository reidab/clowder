#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo 'TEST: cocos2d protocol'
    print_double_separator
    cd "$COCOS2D_EXAMPLE_DIR" || exit 1
    ./clean.sh
    ./init.sh
    $COMMAND herd --protocol 'https' $PARALLEL || exit 1

    if [ -z "$CIRCLECI" ]; then
        pushd cocos2d-objc || exit 1
        test_remote_url 'origin' 'https://github.com/cocos2d/cocos2d-objc.git'
        popd || exit 1
        pushd cocos2d-x || exit 1
        test_remote_url 'origin' 'https://github.com/cocos2d/cocos2d-x.git'
        popd || exit 1
    fi

    ./clean.sh
    ./init.sh
    $COMMAND herd --protocol 'ssh' $PARALLEL || exit 1

    pushd cocos2d-objc || exit 1
    test_remote_url 'origin' 'git@github.com:cocos2d/cocos2d-objc.git'
    popd || exit 1
    pushd cocos2d-x || exit 1
    test_remote_url 'origin' 'git@github.com:cocos2d/cocos2d-x.git'
    popd || exit 1
fi
