#!/usr/bin/env bash

printf "%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
