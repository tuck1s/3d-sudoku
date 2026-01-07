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
    
    max_counts = {
        'out-cube8.txt':  28,
        'out-cube9.txt':  39,
        'out-cube10.txt': 38,
        'out-cube11.txt': 38,
        'out-cube12.txt': 70,
        'out-cube13.txt': 70,
        'out-cube14.txt': 76,
        'out-cube15.txt': 74,
        'out-cube16.txt': 42,
        'out-cube17.txt': 76,
        'out-cube18.txt': 76
    }
    grand_count = 0
    grand_m = 0
    for filename in files:
        total, count = summarize_file(filename)
        if count > 0:
            m = max_counts.get(filename, 1)
            print(f"{filename:20}: {count} / {m} = {count / m * 100:.2f}% slot[1] alternatives found, {total:,} total solutions")
            grand_total += total
            grand_m += m
            grand_count += count
    
    print(f"\nGrand total: {grand_count} / {grand_m} = {grand_count / grand_m * 100:.2f}% slot[1] alternatives found, {grand_total:,} solutions")

if __name__ == '__main__':
    main()
