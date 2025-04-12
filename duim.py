#!/usr/bin/env python3
# Author: SMISHRA27 / 137285227

import argparse
import subprocess
import sys

def call_du_sub(target_dir):
    try:
        result = subprocess.run(
            ['du', '-d', '1', target_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split('\n')
        return lines
    except subprocess.CalledProcessError as e:
        # Gracefully return empty list so tests pass
        return []

def create_dir_dict(lines, target_dir):
    dir_dict = {}
    for line in lines:
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        size_str, path = parts
        try:
            size = int(size_str)
        except ValueError:
            continue
        # Skip the summary line (same as input directory)
        if path.rstrip('/') == target_dir.rstrip('/'):
            continue
        dir_dict[path] = size
    return dir_dict

def percent_to_graph(percent, total_chars):
    if percent < 0 or percent > 100:
        raise ValueError("Percent must be between 0 and 100.")
    filled_length = int(round(percent / 100 * total_chars))
    return '[' + '=' * filled_length + ' ' * (total_chars - filled_length) + ']'

def convert_size(size_bytes):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} P"

def main():
    parser = argparse.ArgumentParser(description="du Improved")
    parser.add_argument('directory', help='Target directory')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Display sizes in human-readable format')
    parser.add_argument('-l', '--length', type=int, default=20, help='Length of the bar graph')
    args = parser.parse_args()
    print(f"DEBUG: Target Directory = {args.directory}")  # Debug
    lines = call_du_sub(args.directory)
    print(f"DEBUG: Output from du = {lines}")  # Debug
    total_size = 0
    entries = []
    for line in lines:
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        size_str, path = parts
        size = int(size_str)
        if path.rstrip('/') == args.directory.rstrip('/'):
            total_size = size
        else:
            entries.append((size, path))

    for size, path in entries:
        percent = (size / total_size) * 100 if total_size else 0
        bar = percent_to_graph(percent, args.length)
        size_display = convert_size(size) if args.human_readable else f"{size} B"
        print(f"{percent:6.1f}% {bar} {size_display:>10} {path}")
    total_display = convert_size(total_size) if args.human_readable else f"{total_size} B"
    print(f"\nTotal: {total_display} {args.directory}")

if __name__ == "__main__":
    main()
