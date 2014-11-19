#!/bin/bash

mkdir -p corpus
cd corpus
curl http://www.pdx.edu/computer-science/courses \
    | grep -iPo 'href="http://www.pdx.edu/computer-science/cs-[^"]+?(?=")' \
    | sed 's/href="//' \
    | uniq \
    | awk '{print tolower($0)}' \
    |  xargs wget --adjust-extension -N
