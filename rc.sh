#!/bin/bash
# This bash script recursively traverses from the provided directory
# and removes all occurences of the __pycache__ directory, containing
# Cpython binaries created after running local Python modules.

function traverse() {
    for file in "$1"/*
    do
        if [ ! -d "${file}" ]; then
            continue
        else
            if [[ "${file}" == *"pycache"* ]]; then
                rm -rf "${file}"
            else
                traverse "${file}"
            fi
        fi
    done
}

function main() {
    traverse "$1"
}

main "."

