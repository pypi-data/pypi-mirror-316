from jnius import autoclass
import random
from jnius import autoclass
import os
import shutil

def get_image_uri(relative_path):
    """
    Get the absolute URI for an image in the assets folder.
    :param relative_path: The relative path to the image (e.g., 'assets/imgs/icon.png').
    :return: Absolute URI (e.g., 'file:///path/to/file.png').
    """
    # Access Android's context and asset manager
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    context = PythonActivity.mActivity
    asset_manager = context.getAssets()

    # Construct the full path for the output file in cache directory
    cache_dir = context.getCacheDir().getAbsolutePath()
    file_name = os.path.basename(relative_path)
    output_path = os.path.join(cache_dir, file_name)

    # Copy the file from assets to cache directory
    with asset_manager.open(relative_path) as asset_file:
        with open(output_path, 'wb') as output_file:
            shutil.copyfileobj(asset_file, output_file)

    # Return the URI
    Uri = autoclass('android.net.Uri')
    return Uri.parse(f"file://{output_path}")

# # Example usage
# image_uri = get_image_uri("imgs/icon.png")
# print(image_uri)

def send_notification(title, message, style=None, img_path=None, channel_id="default_channel"):
    """
    Send a notification on Android.

    :param title: Title of the notification.
    :param message: Message body.
    :param style: Style of the notification ('big_text', 'big_picture', 'inbox').
    :param image: Image URL or drawable for 'big_picture' style.
    :param channel_id: Notification channel ID.
    """
    # Get the required Java classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationCompatBuilder = autoclass('androidx.core.app.NotificationCompat$Builder')
    NotificationCompatBigTextStyle = autoclass('androidx.core.app.NotificationCompat$BigTextStyle')
    NotificationCompatBigPictureStyle = autoclass('androidx.core.app.NotificationCompat$BigPictureStyle')
    NotificationCompatInboxStyle = autoclass('androidx.core.app.NotificationCompat$InboxStyle')
    BitmapFactory = autoclass('android.graphics.BitmapFactory')

    # Get the app's context and notification manager
    context = PythonActivity.mActivity
    notification_manager = context.getSystemService(context.NOTIFICATION_SERVICE)

    # Notification Channel (Required for Android 8.0+)
    if notification_manager.getNotificationChannel(channel_id) is None:
        channel = NotificationChannel(
            channel_id,
            "Default Channel",
            NotificationManager.IMPORTANCE_DEFAULT
        )
        notification_manager.createNotificationChannel(channel)

    # Build the notification
    builder = NotificationCompatBuilder(context, channel_id)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(context.getApplicationInfo().icon)

    
    # Get Image
    if img_path:
        try:
            img_path = get_image_uri(img_path)
        except Exception as e:
            print('Failed getting Image path',e)
    
    # Apply styles
    if style == "big_text":
        big_text_style = NotificationCompatBigTextStyle()
        big_text_style.bigText(message)
        builder.setStyle(big_text_style)
    elif style == "big_picture" and img_path:
        bitmap = BitmapFactory.decodeStream(context.getContentResolver().openInputStream(img_path))
        big_picture_style = NotificationCompatBigPictureStyle()
        big_picture_style.bigPicture(bitmap)
        builder.setStyle(big_picture_style)
    elif style == "inbox":
        inbox_style = NotificationCompatInboxStyle()
        for line in message.split("\n"):
            inbox_style.addLine(line)
        builder.setStyle(inbox_style)

    # Show the notification
    notification_manager.notify(random.randint(0, 100), builder.build())
