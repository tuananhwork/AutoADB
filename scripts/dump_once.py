"""Quick dump script."""
from core import dump


def main():
    """Dump UI once."""
    xml_path, screenshot_path = dump.dump_ui("quick")
    print(f"XML: {xml_path}")
    print(f"Screenshot: {screenshot_path}")


if __name__ == "__main__":
    main()

