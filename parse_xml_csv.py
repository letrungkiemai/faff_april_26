import xml.etree.ElementTree as ET
import csv
import sys
from pathlib import Path


def parse_xml_to_csv(xml_file, csv_file):
    print(f"Parsing {xml_file.name}...")

    # First pass: collect all unique field names across every row
    headers = []
    seen = set()
    for _, elem in ET.iterparse(xml_file, events=('start',)):
        if elem.tag == 'row':
            for key in elem.attrib:
                if key not in seen:
                    seen.add(key)
                    headers.append(key)
            elem.clear()

    if not headers:
        print(f"  -> No rows found, skipping.")
        return

    # Second pass: write CSV with the full header set
    with open(csv_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        for _, elem in ET.iterparse(xml_file, events=('start',)):
            if elem.tag == 'row':
                writer.writerow(elem.attrib)
                elem.clear()

    print(f"  -> {csv_file}")


def parse_folder(folder):
    folder = Path(folder)
    xml_files = list(folder.glob('*.xml'))

    if not xml_files:
        print(f"No XML files found in {folder}")
        return

    csv_dir = folder / 'csv'
    csv_dir.mkdir(exist_ok=True)

    for xml_file in xml_files:
        csv_file = csv_dir / xml_file.with_suffix('.csv').name
        parse_xml_to_csv(xml_file, csv_file)

    print(f"\nDone! Processed {len(xml_files)} file(s).")


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else '.'
    parse_folder(folder)