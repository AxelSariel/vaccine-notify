# vaccine-notify
 
Python script to filter vaccine tweets and send push notifications to iOS Devices accordingly based on user input words.
Feel free to adapt it to your needs like using Email or IFTTT Webhooks to send the notifications.

Requires ```config.py``` file with following structure:

```
consumer_key = 'Twitter API Consumer Key'
consumer_secret = 'Twitter API Consumer Secret'
words_all = ['CVS', 'Walgreens'] // Words that will be matched first - i.e. gets all tweets with 'CVS' or 'Walgreens"
words_any = ['Boston', 'Cambridge', 'Allston'] // Words that will be matched after - i.e. filters previously matched tweets by other words
tokens = ['DeviceNotificationToken', 'Token2'] // Device Notificaiton Tokens to be used by APNS to send notifications to Apple Devices (Requires an iOS app with Remote Push Notifications to get the Device Tokens)
vaccine_bot_username = 'vaccinetime' // Twitter username for vaccine bot
```

Requires Certificates from Apple Developer Account to send Push Notifications.

## To Run:
1. Create a virtualenv (Optional)
1. Install Tweepy with ```pip install tweepy```
1. Run ```python notify.py```

Built with Tweepy.
Uses apns.py developed by Simon Whitaker to send iOS Push Notifications.

