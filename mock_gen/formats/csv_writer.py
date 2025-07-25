import csv
import sys

def write_csv(data, output_file=None):
    """Write data to CSV format. If output_file is None, print to stdout."""
    if not data:
        return
    fieldnames = data[0].keys()
    if output_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data) 