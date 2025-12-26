#!/usr/bin/env python3

import re
import sys
import argparse

# Show lines with dashcount <= this value
SHOW_DEPTH = 4

def parse_line(line):
    """Parse a line into components: dashcount, with_part, seconds, solution_count."""
    line = line.rstrip('\n')

    # Regex to parse: leading dashes, space(s), "with" part, tab, seconds, tab, solution count
    pattern = r'^(-*)\s+(with.*?)\t([\d.]+s)\t\s*(.*)$'
    match = re.match(pattern, line)

    if match:
        dashes, with_part, seconds, solution_count = match.groups()
        return {
            'dashcount': len(dashes),
            'with_part': with_part,
            'seconds': seconds,
            'solution_count': solution_count
        }
    else:
        raise(ValueError(f"Line format incorrect: {line}"))

def parse_line_generator(filename):
    """Generator that yields parsed lines one at a time."""
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('Hint:'):
                    yield parse_line(line)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)

def count_lines(filename):
    """Count lines in a file without loading into memory."""
    try:
        with open(filename, 'r') as f:
            return sum(1 for line in f if line.strip() and not line.startswith('Hint:'))
    except FileNotFoundError:
        return 0

def main():
    parser = argparse.ArgumentParser(description='Compare two output files, ignoring runtime columns')
    parser.add_argument('file1', help='First file (e.g., out.txt)')
    parser.add_argument('file2', help='Second file (e.g., out-cpp.txt)')
    args = parser.parse_args()

    print(f"Comparing {args.file1} vs {args.file2}")
    print(f"Showing lines with dashcount <= {SHOW_DEPTH}")
    print("=" * 70)

    # Count lines for reporting
    count1 = count_lines(args.file1)
    count2 = count_lines(args.file2)

    print(f"{args.file1}: {count1} lines")
    print(f"{args.file2}: {count2} lines")
    print()

    if count1 != count2:
        print(f"Note: Different number of lines - comparing up to shorter length")
        print()

    # Compare line by line using generators
    differences = []
    line_num = 0
    last_parsed1 = None
    last_parsed2 = None

    gen1 = parse_line_generator(args.file1)
    gen2 = parse_line_generator(args.file2)

    while True:
        try:
            parsed1 = next(gen1)
            parsed2 = next(gen2)
            line_num += 1

            last_parsed1 = parsed1
            last_parsed2 = parsed2

            # Show lines with dashcount <= threshold
            if parsed1['dashcount'] <= SHOW_DEPTH:
                match_symbol = "✓" if (parsed1['dashcount'] == parsed2['dashcount'] and
                                       parsed1['with_part'] == parsed2['with_part'] and
                                       parsed1['solution_count'] == parsed2['solution_count']) else "✗"

                # Calculate speed factor (cpp seconds / python seconds)
                time1 = float(parsed1['seconds'].rstrip('s'))
                time2 = float(parsed2['seconds'].rstrip('s'))
                speed_factor = time1 / time2 if time2 > 0 else 0

                print(f"{match_symbol} {'-' * parsed1['dashcount']} {parsed1['with_part']} {parsed1['solution_count']} | {'-' * parsed2['dashcount']} {parsed2['with_part']} {parsed2['solution_count']} | {speed_factor:.2f}x")

            # Compare ignoring seconds
            if (parsed1['dashcount'] != parsed2['dashcount'] or
                parsed1['with_part'] != parsed2['with_part'] or
                parsed1['solution_count'] != parsed2['solution_count']):
                differences.append((line_num, parsed1, parsed2))
        except StopIteration:
            break

    print()
    print("=" * 70)

    if differences:
        print(f"Found {len(differences)} differences:")
        print()
        for line_num, parsed1, parsed2 in differences[:20]:  # Show first 20
            print(f"Line {line_num}:")
            print(f"  Dashes: {parsed1['dashcount']} vs {parsed2['dashcount']}")
            print(f"  With: '{parsed1['with_part']}' vs '{parsed2['with_part']}'")
            print(f"  Solutions: {parsed1['solution_count']} vs {parsed2['solution_count']}")
            print()

        if len(differences) > 20:
            print(f"... and {len(differences) - 20} more differences")
    else:
        print("✓ No differences found! Outputs match.")

        # Show the final line from both
        if last_parsed1 and last_parsed2:
            print()

if __name__ == "__main__":
    main()
