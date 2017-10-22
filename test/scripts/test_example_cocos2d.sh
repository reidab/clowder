#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export external_projects=( 'cocos2d-objc/external/Chipmunk' \
                           'cocos2d-objc/external/ObjectAL' \
                           'cocos2d-objc/external/SSZipArchive' )

print_double_separator
echo 'TEST: cocos2d example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$COCOS2D_EXAMPLE_DIR" || exit 1

./clean.sh
./init.sh || exit 1

test_recurse() {
    print_single_separator
    echo "TEST: Herd recursive submodules"
    clowder herd || exit 1
    clowder status || exit 1
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule was initialized"
        if [ ! -f "$project/.git" ]; then
            echo "TEST: Submodule should exist"
            exit 1
        fi
    done
}
test_recurse

teast_clean_d() {
    print_single_separator
    echo "TEST: Clean untracked directories"
    clowder herd || exit 1

    pushd cocos2d-objc || exit 1
    touch newfile
    mkdir something
    touch something/something
    if [ ! -d 'something' ]; then
        exit 1
    fi
    if [ ! -f 'something/something' ]; then
        exit 1
    fi
    if [ ! -f 'newfile' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean || exit 1

    pushd cocos2d-objc || exit 1
    if [ ! -d 'something' ]; then
        exit 1
    fi
    if [ ! -f 'something/something' ]; then
        exit 1
    fi
    if [ -f 'newfile' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean -d || exit 1

    pushd cocos2d-objc || exit 1
    if [ -d 'something' ]; then
        exit 1
    fi
    if [ -f 'something/something' ]; then
        exit 1
    fi
    if [ -f 'newfile' ]; then
        exit 1
    fi
    popd || exit 1
}
teast_clean_d

test_clean_f() {
    print_single_separator
    echo "TEST: Clean git directories"
    clowder herd || exit 1

    pushd cocos2d-objc || exit 1
    git clone https://github.com/JrGoodle/cats.git
    if [ ! -d 'cats' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean || exit 1

    pushd cocos2d-objc || exit 1
    if [ ! -d 'cats' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean -fd || exit 1

    pushd cocos2d-objc || exit 1
    if [ -d 'cats' ]; then
        exit 1
    fi
    popd || exit 1
}
test_clean_f

test_clean_X() {
    print_single_separator
    echo "TEST: Clean only files ignored by git"
    clowder herd || exit 1

    pushd cocos2d-objc || exit 1
    touch .idea
    touch something
    if [ ! -f '.idea' ]; then
        exit 1
    fi
    if [ ! -f 'something' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean -X || exit 1

    pushd cocos2d-objc || exit 1
    if [ -f '.idea' ]; then
        exit 1
    fi
    if [ ! -f 'something' ]; then
        exit 1
    fi
    popd || exit 1

    pushd cocos2d-objc || exit 1
    rm -f something
    if [ -f '.idea' ]; then
        exit 1
    fi
    if [ -f 'something' ]; then
        exit 1
    fi
    popd || exit 1
}
test_clean_X

test_clean_x() {
    print_single_separator
    echo "TEST: Clean all untracked files"
    clowder herd || exit 1

    pushd cocos2d-objc || exit 1
    touch xcuserdata
    touch something
    if [ ! -f 'xcuserdata' ]; then
        exit 1
    fi
    if [ ! -f 'something' ]; then
        exit 1
    fi
    popd || exit 1

    clowder clean -x || exit 1

    pushd cocos2d-objc || exit 1
    if [ -f 'xcuserdata' ]; then
        exit 1
    fi
    if [ -f 'something' ]; then
        exit 1
    fi
    popd || exit 1
}
test_clean_x

test_clean_a() {
    print_single_separator
    echo "TEST: Clean all"
    clowder herd || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        if [ ! -d 'something' ]; then
            exit 1
        fi
        if [ ! -f 'something/something' ]; then
            exit 1
        fi
        if [ ! -f 'newfile' ]; then
            exit 1
        fi
        popd || exit 1
    done
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
            touch newfile
            mkdir something
            touch something/something
            if [ ! -d 'something' ]; then
                exit 1
            fi
            if [ ! -f 'something/something' ]; then
                exit 1
            fi
            if [ ! -f 'newfile' ]; then
                exit 1
            fi
        popd || exit 1
    done

    clowder clean -a || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        if [ -d 'something' ]; then
            exit 1
        fi
        if [ -f 'something/something' ]; then
            exit 1
        fi
        if [ -f 'newfile' ]; then
            exit 1
        fi
        popd || exit 1
    done
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
            if [ -d 'something' ]; then
                exit 1
            fi
            if [ -f 'something/something' ]; then
                exit 1
            fi
            if [ -f 'newfile' ]; then
                exit 1
            fi
            git branch -D something
        popd || exit 1
    done
}
test_clean_a

test_clean_submodules_untracked() {
    print_single_separator
    echo "TEST: Clean untracked files in submodules"
    clowder herd || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
            touch newfile
            mkdir something
            touch something/something
            if [ ! -d 'something' ]; then
                exit 1
            fi
            if [ ! -f 'something/something' ]; then
                exit 1
            fi
            if [ ! -f 'newfile' ]; then
                exit 1
            fi
        popd || exit 1
    done

    clowder clean -r || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
            if [ -f 'something/something' ]; then
                exit 1
            fi
            if [ -d 'something' ]; then
                exit 1
            fi
            if [ -f 'newfile' ]; then
                exit 1
            fi
        popd || exit 1
    done
}
test_clean_submodules_untracked

test_clean_submodules_dirty() {
    print_single_separator
    echo "TEST: Clean dirty submodules"
    clowder herd || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        if [ ! -f 'something/something' ]; then
            exit 1
        fi
        if [ ! -d 'something' ]; then
            exit 1
        fi
        if [ ! -f 'newfile' ]; then
            exit 1
        fi
        popd || exit 1
    done

    clowder clean -r || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        if [ -f 'something/something' ]; then
            exit 1
        fi
        if [ -d 'something' ]; then
            exit 1
        fi
        if [ -f 'newfile' ]; then
            exit 1
        fi
        git branch -D something
        popd || exit 1
    done
}
test_clean_submodules_dirty

./clean.sh
./init.sh || exit 1

test_no_recurse() {
    print_single_separator
    echo "TEST: Herd without updating submodules"
    clowder link -v no-recurse || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule wasn't initialized"
        if [ -f "$project/.git" ]; then
            echo "TEST: Submodule shouldn't exist"
            exit 1
        fi
    done
}
test_no_recurse