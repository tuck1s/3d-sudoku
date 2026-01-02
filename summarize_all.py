#!/usr/bin/env python3

import re
import glob

def parse_solution_count(line):
    """Extract solution count from a line, removing commas."""
    # Match pattern: dashes, with part, time, solution count
    pattern = r'^(--)\s+with.*?\t[\d.]+s\t\s*([0-9,]+)\s+solutions'
    match = re.match(pattern, line)
    
    if match:
        dashes, count_str = match.groups()
        # Remove commas and convert to int
        count = int(count_str.replace(',', ''))
        return count
    return None

def summarize_file(filename):
    """Summarize level-two lines from a single file."""
    total = 0
    count = 0
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                solution_count = parse_solution_count(line)
                if solution_count is not None:
                    total += solution_count
                    count += 1
        
        return total, count
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return 0, 0

def main():
    # Get all out-cube*.txt files sorted by number
    files = sorted(glob.glob('out-cube*.txt'), 
                   key=lambda x: int(re.search(r'\d+', x).group()))
    
    if not files:
        print("No out-cube*.txt files found")
        return
    
    grand_total = 0
    
    for filename in files:
        total, count = summarize_file(filename)
        if count > 0:
            print(f"{filename}: {count} slot[1] alternatives found, {total:,} total solutions")
            grand_total += total
    
    print(f"\nGrand total: {grand_total:,} solutions")

if __name__ == '__main__':
    main()
