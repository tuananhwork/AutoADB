"""Debug dump to see available elements."""
from core import dump, parser
from core.utils import normalize_text


def main():
    """Dump and show all elements."""
    xml_path, screenshot_path = dump.dump_ui("debug")
    print(f"XML: {xml_path}")
    print(f"Screenshot: {screenshot_path}")
    
    elements = parser.parse_xml(xml_path)
    print(f"\nTotal elements: {len(elements)}")
    
    tappable_count = 0
    text_count = 0
    
    print("\n=== Tappable elements with text ===")
    for i, el in enumerate(elements):
        if el.is_tappable():
            tappable_count += 1
            display_text = el.get_display_text()
            if display_text:
                text_count += 1
                normalized = normalize_text(display_text)
                print(f"{i}: text='{el.text}' content-desc='{el.content_desc}' "
                      f"normalized='{normalized}' bounds={el.bounds}")
    
    print(f"\nTappable: {tappable_count}/{len(elements)}")
    print(f"With text: {text_count}/{len(elements)}")
    
    print("\n=== All elements (first 50) ===")
    for i, el in enumerate(elements[:50]):
        display_text = el.get_display_text()
        normalized = normalize_text(display_text) if display_text else ""
        print(f"{i}: class={el.class_name} text='{el.text}' "
              f"content-desc='{el.content_desc}' "
              f"tappable={el.is_tappable()} bounds={el.bounds}")


if __name__ == "__main__":
    main()

