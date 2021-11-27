def handle_call_count(counter, text):
    if text == 'stupid':
        counter.stupid += 1
    elif text == 'fat':
        counter.fat += 1
    elif text == 'dumb':
        counter.dumb += 1
    else:
        counter.query += 1

    counter.save()
