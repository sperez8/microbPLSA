#!/bin/sh

git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "sperez" ];
        then
                GIT_COMMITTER_NAME="sperez8";
                GIT_AUTHOR_NAME="sperez8";
                GIT_COMMITTER_EMAIL="karatezeus21@gmail.com";
                GIT_AUTHOR_EMAIL="karatezeus21@gmail.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD