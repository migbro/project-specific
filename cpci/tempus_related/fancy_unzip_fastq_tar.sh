#!/usr/bin/env bash

cat $1 | xargs -IFN -P $2 sh -c 'tar -xzf FN -C $(dirname FN)' &