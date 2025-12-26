"""Test parsing."""
import xml.etree.ElementTree as ET
from core.parser import parse_xml

xml_path = 'artifacts/dumps/wait_20251226_152602_848251.xml'

# Parse with ElementTree directly
tree = ET.parse(xml_path)
root = tree.getroot()
nodes = list(root.iter())
content_desc_nodes = [n for n in nodes if n.get('content-desc')]

print(f"Total nodes: {len(nodes)}")
print(f"Nodes with content-desc: {len(content_desc_nodes)}")
print("\nFirst 10 content-desc:")
for i, node in enumerate(content_desc_nodes[:10]):
    cd = node.get('content-desc', '')
    print(f"{i}: {repr(cd)}")

# Parse with our parser
elements = parse_xml(xml_path)
print(f"\nOur parser - Total elements: {len(elements)}")
elements_with_cd = [e for e in elements if e.content_desc]
print(f"Elements with content-desc: {len(elements_with_cd)}")
print("\nFirst 10 content-desc from our parser:")
for i, el in enumerate(elements_with_cd[:10]):
    print(f"{i}: {repr(el.content_desc)}")

