"""Test tappable logic."""
from core.parser import parse_xml

xml_path = 'artifacts/dumps/wait_20251226_152602_848251.xml'
elements = parse_xml(xml_path)

print(f"Total elements: {len(elements)}")
print(f"With content-desc: {sum(1 for e in elements if e.content_desc)}")
print(f"Clickable: {sum(1 for e in elements if e.clickable)}")
print(f"Tappable: {sum(1 for e in elements if e.is_tappable())}")

# Check first element with content-desc
sample = next((e for e in elements if e.content_desc), None)
if sample:
    print(f"\nSample element:")
    print(f"  content-desc length: {len(sample.content_desc)}")
    print(f"  text length: {len(sample.text)}")
    print(f"  get_display_text() length: {len(sample.get_display_text())}")
    print(f"  bool(get_display_text()): {bool(sample.get_display_text())}")
    print(f"  clickable: {sample.clickable}")
    print(f"  bounds: {sample.bounds}")
    print(f"  is_tappable(): {sample.is_tappable()}")
    
    # Check bounds parsing
    from core.utils import parse_bounds
    bounds_dict = parse_bounds(sample.bounds)
    if bounds_dict:
        width = bounds_dict['x2'] - bounds_dict['x1']
        height = bounds_dict['y2'] - bounds_dict['y1']
        print(f"  bounds parsed: {bounds_dict}")
        print(f"  width: {width}, height: {height}")

