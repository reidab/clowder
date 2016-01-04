#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1

OLD_VERSION=$1
NEW_VERSION=$2

perl -pi -e "s/$OLD_VERSION/$NEW_VERSION/g" README.md
perl -pi -e "s/$OLD_VERSION/$NEW_VERSION/g" setup.py
perl -pi -e "s/$OLD_VERSION/$NEW_VERSION/g" clowder/cmd.py
