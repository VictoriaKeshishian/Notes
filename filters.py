from datetime import datetime, timedelta

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)

def timedeltaformat(value):
    delta = datetime.utcnow() - value
    seconds = abs(delta.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes ago" if delta.total_seconds() < 0 else "just now"