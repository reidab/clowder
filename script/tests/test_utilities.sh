#!/usr/bin/env bash

make_dirty_repos()
{
    echo "TEST: Make dirty repos"
    for project in "$@"
    do
    	pushd $project
        touch newfile
        git add newfile
        popd
    done
    clowder diff || exit 1
}

test_branch()
{
    echo "TEST: Check local branch $1 is checked out"
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

test_local_branch_exists()
{
    echo "TEST: Local branch exists: $1"
    git rev-parse --quiet --verify "$1" || exit 1
}

test_no_local_branch_exists()
{
    echo "TEST: Local branch doesn't exist: $1"
    git rev-parse --quiet --verify "$1" && exit 1
}

test_remote_branch_exists()
{
    echo "TEST: Remote branch exists: $1"
    local remote_branch_count
    remote_branch_count="$(git ls-remote --heads origin $1 | wc -l | tr -d '[:space:]')"
    if [ "$remote_branch_count" -eq "0" ]; then
        exit 1
    fi
}

test_no_remote_branch_exists()
{
    echo "TEST: Remote branch doesn't exist: $1"
    local remote_branch_count
    remote_branch_count="$(git ls-remote --heads origin $1 | wc -l | tr -d '[:space:]')"
    if [ "$remote_branch_count" -eq "1" ]; then
        exit 1
    fi
}

test_tracking_branch_exists()
{
    echo "TEST: Tracking branch exists: $1"
    git config --get branch.$1.merge || exit 1
}

test_no_tracking_branch_exists()
{
    echo "TEST: Tracking branch doesn't exist: $1"
    git config --get branch.$1.merge && exit 1
}

test_clowder_version()
{
    print_separator
    echo "TEST: Print clowder version"
    clowder --version || exit 1
    clowder -v || exit 1
}

print_help()
{
    print_separator
    echo "TEST: Help output"
    print_separator
    echo "TEST: clowder -h"
    clowder -h
    print_separator
    echo "TEST: clowder clean -h"
    clowder clean -h
    print_separator
    echo "TEST: clowder diff -h"
    clowder diff -h
    print_separator
    echo "TEST: clowder forall -h"
    clowder forall -h
    print_separator
    echo "TEST: clowder herd -h"
    clowder herd -h
    print_separator
    echo "TEST: clowder init -h"
    clowder init -h
    print_separator
    echo "TEST: clowder link -h"
    clowder link -h
    print_separator
    echo "TEST: clowder prune -h"
    clowder prune -h
    print_separator
    echo "TEST: clowder repo -h"
    clowder repo -h
    print_separator
    echo "TEST: clowder repo add -h"
    clowder repo add -h
    print_separator
    echo "TEST: clowder repo checkout -h"
    clowder repo checkout -h
    print_separator
    echo "TEST: clowder repo clean -h"
    clowder repo clean -h
    print_separator
    echo "TEST: clowder repo commit -h"
    clowder repo commit -h
    print_separator
    echo "TEST: clowder repo pull -h"
    clowder repo pull -h
    print_separator
    echo "TEST: clowder repo push -h"
    clowder repo push -h
    print_separator
    echo "TEST: clowder repo run -h"
    clowder repo run -h
    print_separator
    echo "TEST: clowder repo status -h"
    clowder repo status -h
    print_separator
    echo "TEST: clowder save -h"
    clowder save -h
    print_separator
    echo "TEST: clowder start -h"
    clowder start -h
    print_separator
    echo "TEST: clowder stash -h"
    clowder stash -h
    print_separator
    echo "TEST: clowder status -h"
    clowder status -h
}

print_separator()
{
    echo '--------------------------------------------------------------------------------'
}
