from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmailSubscription
import datetime
import random
from django.utils.translation import gettext as _
from django.utils import timezone

# Dictionary containing fun facts or quotes for each holiday/event
event_facts = {
    'newyear': [
        _("The first New Year's celebration dates back 4,000 years to ancient Babylon."),
        _("In Spain, it's tradition to eat 12 grapes at midnight on New Year's Eve for good luck."),
        _("The famous Times Square New Year's Eve Ball weighs 11,875 pounds!")
    ],
    'eid_fitr': [
        _("Eid al-Fitr marks the end of Ramadan, a month of fasting and prayer."),
        _("On Eid al-Fitr, it's customary to give Zakat al-Fitr, a charity for the needy."),
        _("Eid al-Fitr is also known as the 'Festival of Breaking the Fast'.")
    ],
    'eid_adha': [
        _("Eid al-Adha commemorates the willingness of Ibrahim (Abraham) to sacrifice his son as an act of obedience to God."),
        _("It is also called the 'Festival of Sacrifice'."),
        _("On Eid al-Adha, Muslims around the world perform the act of Qurbani (animal sacrifice).")
    ],
    'ramadan': [
        _("Ramadan is the ninth month of the Islamic lunar calendar."),
        _("During Ramadan, Muslims fast from dawn until sunset."),
        _("The last ten nights of Ramadan are considered the most sacred.")
    ]
}

def get_random_fact(event):
    """
    Returns a random fact for the given event type.
    If no facts are found, returns an empty string.
    """
    return random.choice(event_facts.get(event, [""]))

def event_view(request, event_type, template, event_date_func, is_range=False):
    """
    Generic view for displaying event information.
    - event_type: string key for the event (e.g., 'newyear', 'eid_fitr')
    - template: template path to render
    - event_date_func: function that returns event date(s) given current datetime
    - is_range: if True, event is a date range; else, a single date
    """
    now = timezone.now()
    event_info = event_date_func(now)
    if is_range:
        # For events spanning a range of dates (e.g., Ramadan, Eid al-Adha)
        is_event = event_info['start'] <= now <= event_info['end']
        if now < event_info['start']:
            days_left = (event_info['start'].date() - now.date()).days
        elif is_event:
            days_left = 0
        else:
            # After event, set days_left to 0 (could be extended for next year logic)
            days_left = 0
    else:
        # For single-day events (e.g., New Year, Eid al-Fitr)
        days_until = (event_info['date'].date() - now.date()).days
        is_event = days_until == 0
        days_left = max(days_until, 0)
    fact = get_random_fact(event_type)
    context = {
        'days_left': days_left,
        'fact': fact,
        'tz': str(now.tzinfo)
    }
    # Add event-specific context variables for template logic
    if event_type == 'newyear':
        context['newyear'] = is_event
        context['event_date'] = event_info['date']
    elif event_type == 'eid_fitr':
        context['eid_type'] = 'fitr'
        context['is_eid'] = is_event
        context['event_date'] = event_info['date']
    elif event_type == 'eid_adha':
        context['eid_type'] = 'adha'
        context['is_eid'] = is_event
        context['event_start'] = event_info['start']
        context['event_end'] = event_info['end']
    elif event_type == 'ramadan':
        context['is_ramadan'] = is_event
        context['event_start'] = event_info['start']
        context['event_end'] = event_info['end']
    return render(request, template, context)

def home(request):
    """
    Landing page view for /newyear/
    Handles email subscription form submission and displays a random New Year fact.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Add email to subscription list if not already present
            if not EmailSubscription.objects.filter(email=email).exists():
                EmailSubscription.objects.create(email=email)
                messages.success(request, _('You have subscribed for event reminders!'))
            else:
                messages.info(request, _('You are already subscribed.'))
        else:
            messages.error(request, _('Please enter a valid email address.'))
        return redirect('home')
    fact = get_random_fact('newyear')
    return render(request, "newyear/home.html", {"fact": fact})

def index(request):
    """
    View for New Year's event page.
    Calculates the next New Year's date and passes it to the event_view.
    """
    def newyear_date(now):
        # If today is after Jan 1, get next year's Jan 1; else, this year's Jan 1
        next_new_year = datetime.datetime(now.year + 1, 1, 1, tzinfo=now.tzinfo) if (now.month, now.day) > (1, 1) else datetime.datetime(now.year, 1, 1, tzinfo=now.tzinfo)
        return {'date': next_new_year}
    return event_view(request, 'newyear', 'newyear/index.html', newyear_date)

def eid_el_fitr(request):
    """
    View for Eid al-Fitr event page.
    Uses a fixed date for Eid al-Fitr (March 20, 2026).
    """
    def eid_fitr_date(now):
        eid_date = datetime.datetime(2026, 3, 20, tzinfo=now.tzinfo)
        return {'date': eid_date}
    return event_view(request, 'eid_fitr', 'newyear/eid.html', eid_fitr_date)

def eid_el_adha(request):
    """
    View for Eid al-Adha event page.
    Uses a fixed date range for Eid al-Adha (May 26–30, 2026).
    """
    def eid_adha_range(now):
        eid_start = datetime.datetime(2026, 5, 26, tzinfo=now.tzinfo)
        eid_end = datetime.datetime(2026, 5, 30, 23, 59, 59, tzinfo=now.tzinfo)
        return {'start': eid_start, 'end': eid_end}
    return event_view(request, 'eid_adha', 'newyear/eid.html', eid_adha_range, is_range=True)

def ramadan(request):
    """
    View for Ramadan event page.
    Uses a date range for Ramadan based on the current year (Feb 17 – Mar 18).
    """
    def ramadan_range(now):
        ramadan_start = datetime.datetime(now.year, 2, 17, tzinfo=now.tzinfo)
        ramadan_end = datetime.datetime(now.year, 3, 18, tzinfo=now.tzinfo)
        if now > ramadan_end:
            # If Ramadan has passed, use next year's dates
            ramadan_start = datetime.datetime(now.year + 1, 2, 17, tzinfo=now.tzinfo)
            ramadan_end = datetime.datetime(now.year + 1, 3, 18, tzinfo=now.tzinfo)
        return {'start': ramadan_start, 'end': ramadan_end}
    return event_view(request, 'ramadan', 'newyear/ramadan.html', ramadan_range, is_range=True)
