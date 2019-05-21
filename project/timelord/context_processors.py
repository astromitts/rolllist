from datetime import datetime, date, timedelta


def chronology(request, *args, **kwargs):
    context = {}
    target_date = date.today()
    path_parts = request.path.split('/')
    for part in path_parts:
        try:
            target_date = datetime.strptime(part, "%Y%m%d").date()
            break
        except:
            pass

    context['is_today'] = target_date == date.today()
    context['target_next_day'] = '{0:%Y%m%d}'.format(target_date + timedelta(days=1))
    context['target_previous_date'] = '{0:%Y%m%d}'.format(target_date - timedelta(days=1))
    return context
