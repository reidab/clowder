#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ -z "$COMMAND" ]; then
    COMMAND='clowder'
fi

$COMMAND init https://github.com/jrgoodle/cocos2d-clowder.git || exit 1
