#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats example test script'
print_double_separator

cd "$CATS_EXAMPLE_DIR" || exit 1

"$TEST_SCRIPT_DIR/cats/herd.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_tag.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/forall.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/reset.sh" || exit 1
"$TEST_SCRIPT_DIR/cocos2d/herd.sh" || exit 1
"$TEST_SCRIPT_DIR/cocos2d/skip.sh" || exit 1
"$TEST_SCRIPT_DIR/test_example_llvm.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/reset.sh" || exit 1
