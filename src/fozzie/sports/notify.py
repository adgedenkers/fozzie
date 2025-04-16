# fozzie/sports/notify.py
try:
    from win10toast import ToastNotifier
    notifier = ToastNotifier()
except ImportError:
    notifier = None

def notify_event(message):
    if notifier:
        notifier.show_toast("Fozzie Sports Alert", message, duration=10, threaded=True)
    else:
        print("🔔 Notification: ", message)
# # fozzie/sports/notify.py
# try:
#     from win10toast import ToastNotifier
#     notifier = ToastNotifier()
# except ImportError:
#     notifier = None

# def notify_event(message):
#     if notifier:
#         notifier.show_toast("Fozzie Sports Alert", message, duration=10, threaded=True)
#     else:
#         print("🔔 Notification: ", message)