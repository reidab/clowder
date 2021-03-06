#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo "TEST: Test clowder start"

    cd "$CATS_EXAMPLE_DIR" || exit 1
    ./clean.sh
    ./init.sh
    $COMMAND herd $PROTOCOL $PARALLEL || exit 1

    test_start_tracking() {
        print_single_separator
        echo "TEST: Test start tracking branch"

        echo "TEST: No local or remote branches"
        $COMMAND prune -af tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, remote tracking branch exists"
        $COMMAND prune -af tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, remote tracking branch exists"
        $COMMAND prune -af tracking_branch || exit 1
        $COMMAND start -t tracking_branch || exit 1
        $COMMAND forall $PARALLEL -c 'git checkout master' || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: No local branch, existing remote branch"
        $COMMAND prune -af tracking_branch || exit 1
        $COMMAND start -t tracking_branch || exit 1
        $COMMAND prune -f tracking_branch || exit 1

        pushd mu || exit 1
        test_branch knead
        test_remote_branch_exists tracking_branch
        test_no_local_branch_exists tracking_branch
        popd || exit 1
        pushd duke || exit 1
        test_branch purr
        test_remote_branch_exists tracking_branch
        test_no_local_branch_exists tracking_branch
        popd || exit 1
        for project in "${black_cats_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch && exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, existing remote branch, no tracking relationship"
        $COMMAND prune -af tracking_branch || exit 1
        $COMMAND start -t tracking_branch || exit 1
        $COMMAND prune -f tracking_branch || exit 1
        $COMMAND forall $PARALLEL -c 'git checkout -b tracking_branch' || exit 1
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done
        $COMMAND start -t tracking_branch && exit 1
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, existing remote branch, no tracking relationship"
        $COMMAND prune -af tracking_branch || exit 1
        $COMMAND start -t tracking_branch || exit 1
        $COMMAND prune -f tracking_branch || exit 1
        $COMMAND forall $PARALLEL -c 'git checkout -b tracking_branch' || exit 1
        $COMMAND forall $PARALLEL -c 'git checkout master' || exit 1
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_local_branch_exists tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done
        $COMMAND start -t tracking_branch && exit 1
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_local_branch_exists tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, no remote branch"
        $COMMAND prune -af tracking_branch || exit 1
        $COMMAND start tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_local_branch_exists tracking_branch
            test_no_remote_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, no remote branch"
        $COMMAND prune -r tracking_branch || exit 1
        $COMMAND start tracking_branch || exit 1
        $COMMAND forall $PARALLEL -c 'git checkout master' || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_local_branch_exists tracking_branch
            test_no_remote_branch_exists tracking_branch
            popd || exit 1
        done

        $COMMAND start -t tracking_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done
    }
    test_start_tracking
fi
