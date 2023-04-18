import datetime


def format_time(timestamp):
    # Convert the timestamp string to a datetime object
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    # Get the current time
    now = datetime.datetime.now()

    # Calculate the time difference between the timestamp and the current time
    delta = now - timestamp

    # Calculate the number of seconds, minutes, hours, and days
    seconds = delta.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    # Return the appropriate time string
    if days > 0:
        return f"{int(days)} day{'s' if days > 1 else ''} ago"
    elif hours > 0:
        return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
    elif minutes > 0:
        return f"{int(minutes)} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"


def to_dict(rows, cursor):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
