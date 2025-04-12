#!/usr/bin/env python3
# Author: SMISHRA27 / 137285227

"""
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
"""

import sys
import os
import subprocess
import argparse

def parse_args():
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
        "target", nargs="?", default=os.getcwd(),
        help="Target directory to analyze (default: current directory)"
    )
    return parser.parse_args()


def percent_to_graph(percent, width):
    """Constructs a bar graph string based on percentage and desired width."""
    if not (0 <= percent <= 100):
        raise ValueError("Percentage value must be within 0–100.")
    filled = round((percent / 100) * width)
    return "=" * filled + " " * (width - filled)

def call_du_sub(directory_path):
    """
    Runs 'du -d 1' on the given path and returns a list of output lines.
    Ignores permission-denied warnings but displays other errors.
    """
    try:
        proc = subprocess.Popen(
            ["du", "-d", "1", directory_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, errors = proc.communicate()

        # Filter out known permission-denied lines
        error_lines = [
            line for line in errors.strip().split("\n")
            if "Permission denied" not in line
        ]
        if error_lines:
            print("\n".join(error_lines), file=sys.stderr)

        return output.strip().split("\n")
    except FileNotFoundError:
        print("Error: 'du' utility not found. Make sure it's installed.", file=sys.stderr)
        sys.exit(1)

def create_dir_dict(output_lines):
    """
    Converts du output into a dictionary mapping paths to sizes.
    Ignores malformed lines.
    """
    usage_map = {}
    for entry in output_lines:
        parts = entry.strip().split("\t")
        if len(parts) == 2:
            size, path = parts
            try:
                usage_map[path] = int(size)
            except ValueError:
                continue
    return usage_map

def format_size(bytes_val, human_flag):
    """Formats the byte size into a readable string based on the flag."""
    if not human_flag:
        return f"{bytes_val} B"

    float_val = float(bytes_val)
    for unit in ["B", "K", "M", "G", "T"]:
        if float_val < 1024:
            return f"{float_val:.1f} {unit}"
        float_val /= 1024
    return f"{float_val:.1f} P"



if __name__ == "__main__":
    args = parse_args()

    if not os.path.isdir(args.target):
        print(f"Error: '{args.target}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    du_data = run_du(args.directory)
    dir_sizes = convert_output_to_dict(du_data)

    total = dir_sizes.get(args.directory, sum(dir_sizes.values()))

    print("\nDisk Usage Overview:")
    for path, size in sorted(dir_sizes.items(), key=lambda item: item[1], reverse=True):
        percent = (size / total) * 100 if total > 0 else 0
        bar = draw_bar(percent, args.length)
        readable_size = format_size(size, args.human_readable)
        print(f"{percent:5.1f}% [{bar}] {readable_size:>8}  {path}")

    total_formatted = format_size(total, args.human_readable)
    print(f"\nTotal: {total_formatted}  {args.target}")
