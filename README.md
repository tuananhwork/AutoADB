# ADB Automation Framework

Framework Python automation cho Android dựa trên ADB và uiautomator dump.

## Mục đích

- Dump UI XML từ thiết bị Android
- Parse XML để tìm element với text normalization
- Thực hiện các action: tap, swipe, keyevent, touch by text
- Thiết kế nhẹ, dễ mở rộng, code clean
- Hỗ trợ wait/retry mechanism
- Tự động chụp screenshot và dump XML khi cần

## Yêu cầu hệ thống

- **Python**: 3.7 trở lên
- **ADB**: Đã cài đặt và trong PATH
- **Thiết bị Android**:
  - Đã kết nối qua USB hoặc WiFi ADB
  - USB Debugging đã bật
  - Kiểm tra: `adb devices`

## Cài đặt

1. Clone repository:

```bash
git clone <repository-url>
cd adb
```

2. Không cần cài đặt dependencies (chỉ dùng Python standard library)

3. Kiểm tra ADB:

```bash
adb devices
```

Nếu thấy device ID là OK.

## Cấu hình

### 1. Cấu hình Device (`config/device.py`)

```python
DEVICE_ID = None  # None = dùng device mặc định, hoặc set device ID cụ thể
ADB_OPTIONS = []  # Tùy chọn ADB bổ sung nếu cần
```

**Ví dụ:**

```python
DEVICE_ID = "emulator-5554"  # Dùng device cụ thể
```

### 2. Cấu hình App (`config/app.py`)

```python
PACKAGE_NAME = "vn.vsf.app.uat"  # Package name của app
LAUNCH_DELAY = 10.0  # Thời gian chờ sau khi launch app (giây)
```

### 3. Cấu hình Settings (`config/settings.py`)

```python
TIMEOUT = 10  # Timeout mặc định (giây)
RETRY_COUNT = 5  # Số lần retry mặc định
DUMP_ON_EACH_STEP = False  # Dump sau mỗi step (tắt để tăng tốc)
DUMP_ON_ERROR = True  # Luôn dump khi có lỗi (nên bật)
DUMP_ON_WAIT = False  # Dump khi wait/retry
```

## Cấu trúc dự án

```
adb/
├── config/              # Cấu hình
│   ├── device.py        # Device ID, ADB options
│   ├── app.py           # Package name, launch delay
│   └── settings.py      # Timeout, retry, dump settings
│
├── core/                # Core modules
│   ├── adb.py           # ADB command wrapper
│   ├── device.py        # tap, swipe, keyevent
│   ├── app.py           # start/stop app
│   ├── dump.py          # UI dump + screenshot
│   ├── parser.py        # Parse XML → Element list
│   ├── selector.py      # Find element in XML
│   ├── element.py       # Element abstraction
│   ├── waiter.py        # Wait/retry mechanism
│   ├── utils.py         # Text normalization, bounds parsing
│   └── exceptions.py    # Custom exceptions
│
├── commons/             # Common utilities
│   ├── setup.py         # Common setup/teardown
│   └── helpers.py       # Helper functions (click_element, execute_steps)
│
├── tests/               # Test cases
│   ├── test_dump.py     # Ví dụ test flow
│   ├── test_mixed_actions.py  # Ví dụ mixed actions
│   └── test_example.py  # Template test
│
├── scripts/             # Utility scripts
│   ├── dump_once.py     # Dump UI nhanh
│   └── debug_dump.py    # Debug dump
│
├── artifacts/           # Output (không commit)
│   ├── dumps/           # XML dumps
│   └── screenshots/     # Screenshots
│
├── main.py              # Entry point
└── README.md
```

## Hướng dẫn sử dụng

### 1. Dump UI nhanh

```bash
python scripts/dump_once.py
```

Kết quả: XML và screenshot trong `artifacts/`

### 2. Viết test case đơn giản

**File: `tests/my_test.py`**

```python
from commons.setup import setup_app
from commons.helpers import execute_steps

def test_my_flow():
    """Test flow example."""
    print("=" * 60)
    print("STARTING TEST")
    print("=" * 60)

    # Setup app
    setup_app()

    # Steps - format đơn giản
    steps = [
        "Khám phá",  # Touch by text
        ("Hậu mãi VinFast", 0),  # Touch với nth
        "Tiếp theo",
    ]

    execute_steps(steps)

    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_my_flow()
```

**Chạy:**

```bash
python tests/my_test.py
```

### 3. Test với mixed actions

```python
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key, sleep

def test_mixed():
    setup_app()

    steps = [
        # Touch by text (format đơn giản)
        "Khám phá",
        ("Button", 1),  # nth element

        # Dùng helper functions
        touch("Đặt lịch dịch vụ", nth=0),
        tap(540, 1200),  # Tap tại tọa độ
        swipe(540, 1500, 540, 500, duration=500),  # Swipe lên
        key(4),  # BACK button (code 4)
        sleep(2.0),  # Đợi 2 giây

        # Hoặc dùng dict format (linh hoạt nhất)
        {"action": "touch", "text": "Button", "nth": 1, "wait_after": 2.0},
    ]

    execute_steps(steps)

if __name__ == "__main__":
    test_mixed()
```

## Các format step

### Format đơn giản (backward compatible)

```python
steps = [
    "Text",                    # Touch by text
    ("Text", nth),            # Touch với nth element
    ("Text", nth, wait_after), # Đầy đủ options
]
```

### Helper functions

```python
from commons.helpers import touch, tap, swipe, key, sleep

steps = [
    touch("Text", nth=0, wait_after=1.0),
    tap(x=540, y=1200),
    swipe(x1=540, y1=1500, x2=540, y2=500, duration=500),
    key(code=4),  # BACK=4, HOME=3
    sleep(duration=2.0),
]
```

### Dict format (linh hoạt nhất)

```python
steps = [
    {"action": "touch", "text": "Text", "nth": 0, "wait_after": 1.0},
    {"action": "tap", "x": 540, "y": 1200},
    {"action": "swipe", "x1": 540, "y1": 1500, "x2": 540, "y2": 500, "duration": 500},
    {"action": "key", "code": 4},
    {"action": "sleep", "duration": 2.0},
]
```

## Action types

### 1. Touch by text

```python
# Đơn giản
"Khám phá"

# Với nth
("Khám phá", 1)  # Element thứ 2 (0-based)

# Helper function
touch("Khám phá", nth=1, wait_after=2.0)

# Dict format
{"action": "touch", "text": "Khám phá", "nth": 0}
```

**Tính năng:**

- Tự động normalize text (strip, collapse spaces)
- Fallback content-desc nếu text rỗng
- Tự động filter tappable elements
- Wait/retry tự động

### 2. Tap at coordinates

```python
tap(540, 1200)  # Tap tại (x, y)
{"action": "tap", "x": 540, "y": 1200}
```

### 3. Swipe

```python
swipe(540, 1500, 540, 500, duration=500)  # Swipe từ (540,1500) đến (540,500)
{"action": "swipe", "x1": 540, "y1": 1500, "x2": 540, "y2": 500, "duration": 300}
```

### 4. Key event

```python
key(4)  # BACK button
{"action": "key", "code": 4}
```

**Key codes phổ biến:**

- `3` - HOME
- `4` - BACK
- `24` - VOLUME_UP
- `25` - VOLUME_DOWN
- `66` - ENTER

### 5. Sleep/Wait

```python
sleep(2.0)  # Đợi 2 giây
{"action": "sleep", "duration": 2.0}
```

## API Reference

### Core APIs

#### `Wait(timeout=15, interval=1.0)`

```python
from core.waiter import Wait

# Wait until element found
element = Wait(timeout=15).until_element(text_contains="Khám phá")
element.click()

# Wait with custom interval
element = Wait(timeout=20, interval=0.5).until_element(text_contains="Button", nth=1)
```

#### `find(xml_path, text_contains=None, nth=0)`

```python
from core.selector import find

element = find("artifacts/dumps/dump.xml", text_contains="Khám phá", nth=0)
if element:
    element.click()
```

#### `dump_ui(prefix="dump")`

```python
from core import dump

xml_path, screenshot_path = dump.dump_ui("my_dump")
```

### Common Setup

#### `setup_app(package=None, stabilize_delay=2.0)`

```python
from commons.setup import setup_app

setup_app()  # Dùng package từ config
setup_app(package="com.example.app", stabilize_delay=3.0)  # Custom
```

#### `execute_steps(steps, start_step_num=1)`

```python
from commons.helpers import execute_steps

steps = ["Button1", "Button2"]
execute_steps(steps, start_step_num=1)
```

## Ví dụ đầy đủ

### Ví dụ 1: Test flow đơn giản

```python
from commons.setup import setup_app
from commons.helpers import execute_steps

def test_simple():
    setup_app()

    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
        ("Đặt lịch dịch vụ", 0),
        "Bảo dưỡng",
    ]

    execute_steps(steps)

if __name__ == "__main__":
    test_simple()
```

### Ví dụ 2: Test với mixed actions

```python
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key

def test_complex():
    setup_app()

    steps = [
        touch("Khám phá"),
        tap(540, 1200),  # Tap tại center
        swipe(540, 1500, 540, 500),  # Swipe lên để scroll
        touch("Button"),
        key(4),  # Back
    ]

    execute_steps(steps)

if __name__ == "__main__":
    test_complex()
```

### Ví dụ 3: Custom wait và error handling

```python
from commons.setup import setup_app
from core.waiter import Wait
from core.exceptions import TimeoutException

def test_with_error_handling():
    setup_app()

    try:
        # Wait với timeout dài hơn
        element = Wait(timeout=30).until_element(text_contains="Slow loading button")
        element.click()
    except TimeoutException as e:
        print(f"Element not found: {e}")
        # Dump đã tự động được tạo khi error (nếu DUMP_ON_ERROR=True)

if __name__ == "__main__":
    test_with_error_handling()
```

## Troubleshooting

### 1. Device không kết nối

```bash
# Kiểm tra device
adb devices

# Nếu không thấy device:
# - Kiểm tra USB debugging đã bật
# - Thử cắm lại USB
# - Chạy: adb kill-server && adb start-server
```

### 2. Element không tìm thấy

- Kiểm tra text có đúng không (có thể có space, newline)
- Thử dùng `text_contains` thay vì `text`
- Kiểm tra XML dump trong `artifacts/dumps/`
- Tăng timeout: `Wait(timeout=30)`
- Bật `DUMP_ON_EACH_STEP = True` để debug

### 3. App không start

- Kiểm tra package name trong `config/app.py`
- Tăng `LAUNCH_DELAY` nếu app load chậm
- Kiểm tra app đã cài đặt: `adb shell pm list packages | grep <package>`

### 4. Text không khớp

Framework tự động normalize text:

- Strip whitespace
- Collapse multiple spaces
- Replace newlines với space
- Fallback content-desc nếu text rỗng

Nếu vẫn không khớp, kiểm tra XML dump để xem text thực tế.

## Best Practices

1. **Sử dụng `text_contains` thay vì `text`** - Linh hoạt hơn với text có thể thay đổi

2. **Tắt `DUMP_ON_EACH_STEP` khi chạy thường xuyên** - Tăng tốc độ

3. **Luôn bật `DUMP_ON_ERROR`** - Dễ debug khi có lỗi

4. **Sử dụng `setup_app()` từ commons** - Tái sử dụng code

5. **Thêm `sleep()` sau các action quan trọng** - Đảm bảo UI ổn định

6. **Sử dụng helper functions** - Code ngắn gọn, dễ đọc

7. **Đặt tên test rõ ràng** - Dễ maintain

## Mở rộng

### Thêm action type mới

1. Thêm function trong `core/device.py`:

```python
def my_action(param1, param2):
    adb.run(f"shell my_command {param1} {param2}")
```

2. Thêm vào `commons/helpers.py`:

```python
def my_action_helper(param1, param2, wait_after=1.0, desc=None):
    return {"action": "my_action", "param1": param1, "param2": param2, "wait_after": wait_after, "desc": desc}
```

3. Xử lý trong `execute_action()`:

```python
elif action_type == "my_action":
    param1 = action_dict["param1"]
    param2 = action_dict["param2"]
    device.my_action(param1, param2)
```

### Thêm selector mới

Mở rộng `core/selector.py` để thêm các cách tìm element mới.

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
