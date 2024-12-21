from jnius import autoclass
import random

def send_notification(title, message, style=None, image=None, channel_id="default_channel"):
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

    # Apply styles
    if style == "big_text":
        big_text_style = NotificationCompatBigTextStyle()
        big_text_style.bigText(message)
        builder.setStyle(big_text_style)
    elif style == "big_picture" and image:
        bitmap = BitmapFactory.decodeStream(context.getContentResolver().openInputStream(image))
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
