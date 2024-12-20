#!/usr/bin/env bash

set -e
set -u

usage() {
    echo "Usage: $0 --user=<username> [--ip=<ip_address>] --source-dir=<source_directory> [--target-basedir=<target_base_directory>]"
    echo
    echo "Required parameters:"
    echo "  --user=<username>          SSH username"
    echo "  --source-dir=<source_directory>  Source directory to sync"
    echo
    echo "Optional parameters:"
    echo "  --ip=<ip_address>          IP address of the remote host (if not provided, the user will be prompted)"
    echo "  --target-basedir=<target_base_directory>  Base directory on the target host (default: empty string)"
    exit 1
}

user="root"
source_dir="/Users/mtm/pdev/taylormonacelli/kindsealion"
target_basedir=""""

for i in "$@"; do
    case $i in
    --user=*)
        user="${i#*=}"
        shift
        ;;
    --ip=*)
        ip="${i#*=}"
        shift
        ;;
    --source-dir=*)
        source_dir="${i#*=}"
        shift
        ;;
    --target-basedir=*)
        target_basedir="${i#*=}"
        shift
        ;;
    *)
        echo "Unknown parameter passed: $i"
        usage
        ;;
    esac
done

if [[ -z ${ip-} ]]; then
    read -r -p "Enter the IP address: " ip
fi

if [[ -z ${user-} || -z ${source_dir-} ]]; then
    echo "Error: --user and --source-dir parameters are required."
    usage
fi

watchexec --watch="${source_dir}" \
    "${source_dir}"/.project_rsync.sh \
    --user="$user" \
    --ip="$ip" \
    --source-dir="${source_dir}" \
    --target-basedir="${target_basedir}"
