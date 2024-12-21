# Usage

```python
from android_notify.core import send_notification
from android_notify.styles import NotificationStyles

# Send a basic notification
send_notification("Hello", "This is a basic notification.")

# Send a big text notification
send_notification("Big Text", "This is a notification with a lot of text to show.", style=NotificationStyles.BIG_TEXT)

# Send a big picture notification
from jnius import autoclass
Uri = autoclass('android.net.Uri')
image_uri = Uri.parse("file:///path/to/image.jpg")
send_notification("Big Picture", "Here's a notification with a picture.", style=NotificationStyles.BIG_PICTURE, image=image_uri)

# Send an inbox style notification
send_notification(
    "Inbox Style",
    "Line 1\nLine 2\nLine 3\nLine 4",
    style=NotificationStyles.INBOX
)

```
