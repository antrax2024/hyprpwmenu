#!/usr/bin/env bash

MINOR_VERSION="$(git rev-list --count HEAD)"
MAJOR_VERSION="$(git rev-parse --short HEAD)"

echo "$MINOR_VERSION.$MAJOR_VERSION"

echo "$MINOR_VERSION.$MAJOR_VERSION" >version.txt
