#!/usr/bin/env bash

set -e

usage() {
    echo "Usage: $0 --user=<username> --ip=<ip_address> --source-dir=<source_directory> [--target-basedir=<target_base_directory>]"
    echo
    echo "Required parameters:"
    echo "  --user=<username>          SSH username"
    echo "  --ip=<ip_address>          IP address of the remote host"
    echo "  --source-dir=<source_directory>  Source directory to sync"
    echo
    echo "Optional parameters:"
    echo "  --target-basedir=<target_base_directory>  Base directory on the target host (default: empty string)"
    exit 1
}

target_basedir=""

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

if [[ -z ${user-} || -z ${ip-} || -z ${source_dir-} ]]; then
    echo "Error: --user, --ip, and --source-dir parameters are all required."
    usage
fi

if [[ ! -d ${source_dir} ]]; then
    echo "Error: Source directory '${source_dir}' does not exist or is not a directory."
    usage
fi

rsync_cmd=(
    rsync
    --archive
    --compress
    --filter=". $HOME/.rsync-filters.txt"
    --max-size=0.2m
    --no-links
    --prune-empty-dirs
    --rsh='ssh -o "UserKnownHostsFile=/dev/null"'
    --verbose
)

if [[ -f "$HOME/.rsync-filters.txt" ]]; then
   rsync_cmd+=(--filter=". $HOME/.rsync-filters.txt")
fi

"${rsync_cmd[@]}" "${source_dir}" "$user"@"$ip":"${target_basedir}"
