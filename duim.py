#!/usr/bin/env python3
# Author: SMISHRA27 / 137285227

OPS445 Assignment 2 - Winter 2025
Program: duim.py 
Author: "SMISHRA27 / 137285227"

'''
The python code in this file (duim.py) is original work written by
"SMISHRA27". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or online resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script mimics the functionality of `du`, displaying disk usage
with a bar graph representing space usage in a directory
Date:April 12, 2025
'''

import sys
import os
import subprocess
import argparse

def parse_args():
    """Parses command-line options using argparse."""
    parser = argparse.ArgumentParser(
        description="Enhanced Disk Usage Viewer with bar chart visualization"
    )
    parser.add_argument(
        "-l", "--length", type=int, default=20,
        help="Length of the bar graph in characters (default: 20)"
    )
    parser.add_argument(
        "-H", "--human-readable", action="store_true",
        help="Display sizes in human-readable format (KB, MB, GB...)"
    )
    parser.add_argument(
        "directory", nargs="?", default=os.getcwd(),
        help="Target directory to analyze (default: current directory)"
    )
    return parser.parse_args()


def draw_bar(percent, width):
    """Constructs a bar graph string based on percentage and desired width."""
    if not (0 <= percent <= 100):
        raise ValueError("Percentage value must be within 0–100.")
    filled = round((percent / 100) * width)
    return "=" * filled + " " * (width - filled)


def create_dir_dict(lines):
    dir_dict = {}
    if not lines:
        return dir_dict

    # Excluing the last line (it's the total for the directory)
    for line in lines[:-1]:  # excludes last line
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        size_str, path = parts
        try:
            size = int(size_str)
        except ValueError:
            continue
        dir_dict[path] = size

    return dir_dict

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
