#!/usr/bin/env bash
set -e

tmp=$(mktemp -d kindsealion.XXXXX)

if [ -z "${tmp+x}" ] || [ -z "$tmp" ]; then
    echo "error: $tmp is not set or is an empty string."
    exit 1
fi

if ! command -v txtar-c >/dev/null; then
    echo go install github.com/rogpeppe/go-internal/cmd/txtar-c@latest
	exit 1
fi

declare -a files=(
	# .pre-commit-config.yaml # loc: 10
	# Makefile # loc: 3
	# README.md # loc: 5
	# Taskfile.yml # loc: 0
	# kindsealion.code-workspace # loc: 8
	# make_txtar.sh # loc: 114
	# manifest.yml # loc: 84
	# pyproject.toml # loc: 36
	# requirements-dev.lock # loc: 35
	# requirements.lock # loc: 20
	# src/kindsealion/__init__.py # loc: 8
	# src/kindsealion/__main__.py # loc: 5
	src/kindsealion/main2.py # loc: 146
	src/kindsealion/parse_args.py # loc: 32
	# src/kindsealion/templates/Taskfile.yml.j2 # loc: 17
	# src/kindsealion/templates/base.j2 # loc: 3
	# src/kindsealion/templates/extended.j2 # loc: 3
	# src/kindsealion/templates/script.sh.j2 # loc: 14
	# src/kindsealion/templates/ubuntu.pkr.hcl # loc: 36
	
)
for file in "${files[@]}"; do
    echo $file
done | tee $tmp/filelist.txt

tar -cf $tmp/kindsealion.tar -T $tmp/filelist.txt
mkdir -p $tmp/kindsealion
tar xf $tmp/kindsealion.tar -C $tmp/kindsealion
rg --files $tmp/kindsealion

mkdir -p $tmp/gpt_instructions_XXYYBB

cat >$tmp/gpt_instructions_XXYYBB/1.txt <<EOF

EOF

{
    cat $tmp/gpt_instructions_XXYYBB/1.txt
    echo txtar archive is below
    txtar-c $tmp/kindsealion
} | pbcopy

rm -rf $tmp
