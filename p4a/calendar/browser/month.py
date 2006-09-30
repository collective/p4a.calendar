import datetime
import calendar
from p4a.calendar import interfaces
from p4a.calendar.atct import eventprovider

DAYS = [
        'Monday', 
        'Tuesday', 
        'Wednesday', 
        'Thursday', 
        'Friday', 
        'Saturday',
        'Sunday',                 
        ]

MONTHS = [
          'N/A',
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
          ]

ONEDAY = datetime.timedelta(days=1)

def event_label(event):
    """Return a clean label representing the given event.
    
    Here's the sort of object that is meant to represent an event.
    
      >>> from datetime import datetime
      >>> def event(title, hour, minute):
      ...     class Mock(object): pass
      ...     event = Mock()
      ...     event.start = datetime(2006, 9, 30, hour, minute)
      ...     event.Title = title
      ...     return event
      
    Make sure the label is clean.
    
      >>> event_label(event('Some Event', 9, 30))
      '9:30 Some Event'
      
      >>> event_label(event('Some Event', 9, 0))
      '9 Some Event'

      >>> event_label(event('Some Event', 13, 0))
      '1p Some Event'

      >>> event_label(event('Some Event', 13, 20))
      '1:20p Some Event'
    """
    
    if not isinstance(event.start, datetime.date):
        dt = eventprovider.DT2dt(event.start)
    else:
        dt = event.start

    ampm = ''
    hour = ''
    if dt.hour > 12:
        hour = dt.hour - 12
        ampm = 'p'
    else:
        hour = dt.hour
    minutes = ''
    if dt.minute != 0:
        minutes = ':%02i' % dt.minute
    
    time = str(hour) + minutes + ampm
    
    return time + ' ' + event.Title

def monthweeks(year=None, month=None, daydate=None, firstweekday=None):
    """Return an iterable of week tuples where each element in the week
    tuple is an instance of *datetime.date*.  If *datedate* is ommitted
    then the date chosen is based on the *year* and *month*.
    
    The following are equivalent.
    
      >>> from datetime import date
      >>> list(monthweeks(2006, 2)) == list(monthweeks(daydate=date(2006, 2, 13)))
      True
      
    Now lets check out some week day values.
    
      >>> weeks = list(monthweeks(2006, 2, firstweekday=6))
      
    There will of course be 5 weeks.
    
      >>> len(weeks)
      5

    The first day of the first week will be January 1st, 2006.
      
      >>> weeks[0][0]
      datetime.date(2006, 1, 29)
      
    The last day of the first week will be February 4, 2006.

      >>> weeks[0][-1]
      datetime.date(2006, 2, 4)
      
    The first day of the last week will be February 26, 2006.

      >>> weeks[-1][0]
      datetime.date(2006, 2, 26)

    The last day of the last week will be March 4, 2006.
    
      >>> weeks[-1][-1]
      datetime.date(2006, 3, 4)

    For a month where the last day of the month is the last day of the
    week.
    
      >>> weeks = weeks = list(monthweeks(2006, 9, firstweekday=6))
      >>> weeks[-1][-1]
      datetime.date(2006, 9, 30)

    """
    
    if firstweekday == None:
        firstweekday = calendar.firstweekday()

    if firstweekday == 0:
        lastweekday = 6
    else:
        lastweekday = firstweekday - 1
    
    if daydate is None:
        today = datetime.date.today()
        y = year or today.year
        m = month or today.month
        firstdate = datetime.date(y, m, 1)
    else:
        firstdate = datetime.date(daydate.year,
                                  daydate.month,
                                  1)

    firstcalday = firstdate
    while calendar.weekday(firstcalday.year, 
                           firstcalday.month, 
                           firstcalday.day) != firstweekday:
        firstcalday -= ONEDAY
    
    done = False
    weeks = []
    day = firstcalday
    nextday = day + ONEDAY
    weekday = calendar.weekday(day.year, day.month, day.day)

    while day.month <= firstdate.month or \
          (day.month > firstdate.month and weekday != firstweekday):

        if weekday == firstweekday:
            week = []
            weeks.append(week)
        week.append(day)
        
        day += ONEDAY
        nextday = day + ONEDAY
        weekday = calendar.weekday(day.year, day.month, day.day)

    return (tuple(x) for x in weeks)

class MonthView(object):
    """View for a month.
    """

    def __init__(self, context=None, request=None):
        if context is not None:
            self.context = context
        if request is not None:
            self.request = request
        
        self.__cached_weeks = {}
        self.__cached_alldays = {}

    @property
    def default_day(self):
        if hasattr(self, '__default_day'):
            return self.__default_day
        
        if not hasattr(self, 'request'):
            self.__default_day = datetime.datetime.today()
            return self.__default_day
        
        year = self.request.form.get('year', None)
        month = self.request.form.get('month', None)
        
        if month is None:
            return datetime.datetime.today()
        
        year = year or datetime.datetime.today().year
        year = int(year)
        month = int(month)
        
        self.__default_day = datetime.datetime(year, month, 1)
        
        return self.__default_day

    @property
    def firstweekday(self):
        return int(self.request.form.get('firstweekday', 
                                         calendar.firstweekday()))

    def standard_week_days(self, firstweekday=None):
        """Return the standard days of the week starting with the day
        that is most appropriate as the start day for the current locale.
        
        As an example, make sure using 6 as the first work day chooses a 
        week starting with Sunday.
        
          >>> mt = MonthView()
          >>> days = mt.standard_week_days(6)
          >>> days[0]
          {'extrastyleclass': 'first-week-day', 'day': 'Sunday'}
          >>> days[-1]
          {'extrastyleclass': 'last-week-day', 'day': 'Saturday'}
        """
        
        if firstweekday is None:
            firstweekday = self.firstweekday
        
        days = [{'day': x,
                 'extrastyleclass': ''} for x in DAYS[firstweekday:]]
        days += [{'day': x,
                  'extrastyleclass': ''} for x in DAYS[0:firstweekday]]

        days[0]['extrastyleclass'] = 'first-week-day'
        days[-1]['extrastyleclass'] = 'last-week-day'
        
        return days

    def weeks(self, daydate=None, firstweekday=None):
        """Return as a list of of the (partial or full) weeks of the
        month which contains the datetime instance, *day*.  Each item
        in this list is a dict containing a key representing the day
        of the month (or in the case of a day that's not in that month,
        None).
        
        Start out by making sure we're able to get some weeks for today's
        date.
        
          >>> mt = MonthView()
          >>> len(mt.weeks(firstweekday=6)) > 1
          True

        Now lets query known dates.
        
          >>> from datetime import datetime
          >>> weeks = mt.weeks(datetime(2006, 2, 23), 0)
          >>> len(weeks)
          5
          
        First day of the week period should be an outside month day.
        
          >>> weeks[0]['days'][0]['extrastyleclass']
          ' outside-month first-week-day'
          >>> weeks[0]['days'][0]['day']
          30

          >>> weeks[4]['days'][0]['extrastyleclass']
          ' first-week-day'
          >>> weeks[4]['days'][0]['day']
          27
          
        Inspect the last day.  Should be outside the month as well.
        
          >>> weeks[-1]['days'][-1]['extrastyleclass']
          ' outside-month last-week-day last-month-day'
          >>> weeks[-1]['days'][-1]['day']
          5
          
        Make sure if we use a different weekday things still work.
        
          >>> weeks = mt.weeks(datetime(2006, 2, 23), 0)
          >>> weeks[0]['days'][0]['day']
          30
          
        """

        if daydate is None:
            daydate = self.default_day

        today = datetime.datetime.today().date()
        
        if firstweekday is None:
            firstweekday = self.firstweekday

        weeks = self.__cached_weeks.get((daydate, firstweekday), None)
        if weeks is not None:
            return weeks

        weektuples = list(monthweeks(daydate=daydate, firstweekday=firstweekday))
        weeks = []
        alldays = {}
        for weekpos, weektuple in enumerate(weektuples):
            week = {'days': []}
            weeks.append(week)

            week['extrastyleclass'] = ''

            if weekpos == 0:
                week['extrastyleclass'] += ' first-week'
            elif weekpos == len(weektuples)-1:
                week['extrastyleclass'] += ' last-week'

            for daypos, weekdate in enumerate(weektuple):
                day = {'events': [],
                       'allevents': [],
                       'has_more': False}
                week['days'].append(day)
                
                alldays[weekdate] = day
                
                day['extrastyleclass'] = ''
                day['day'] = weekdate.day
                day['datestr'] = '%04i-%02i-%02i' % (weekdate.year,
                                                     weekdate.month,
                                                     weekdate.day)
                
                if weekdate == today:
                    day['extrastyleclass'] += ' today'

                if weekdate.month != daydate.month:
                    day['extrastyleclass'] += ' outside-month'
                    
                if daypos == 0:
                    day['extrastyleclass'] += ' first-week-day'
                elif daypos == 6:
                    day['extrastyleclass'] += ' last-week-day'
                    
                if weekdate.month == daydate.month and weekdate.day == 1:
                    day['extrastyleclass'] += ' first-month-day'

        # find the last day of the month and give it extra style class
        for day in reversed(weeks[-1]['days']):
            if day['day'] is not None:
                day['extrastyleclass'] += ' last-month-day'
                break
        
        self._fill_events(alldays)
        
        self.__cached_weeks[(daydate, firstweekday)] = weeks
        self.__cached_alldays[(daydate, firstweekday)] = alldays

        return weeks

    def alldays(self, daydate=None, firstweekday=None):
        if daydate is None:
            daydate = self.default_day

        today = datetime.datetime.today().date()
        
        if firstweekday is None:
            firstweekday = self.firstweekday

        # kick the day generation
        self.weeks(daydate, firstweekday)
        return self.__cached_alldays[(daydate, firstweekday)].values()

    @property
    def _events(self):
        events = getattr(self, '__cached_events', None)
        if events is not None:
            return events
        
        if not hasattr(self, 'context'):
            self.__cached_events = []
            return self.__cached_events

        default = self.default_day
        
        start = datetime.datetime(default.year, default.month, 1, 0, 0)
        
        if default.month < 12:
            end = datetime.datetime(default.year, default.month+1, 1, 23, 59)
            end -= datetime.timedelta(days=1)
        elif default.month == 12:
            end = datetime.datetime(default.year, default.month, 31, 23, 59)
        
        provider = interfaces.IEventProvider(self.context)

        self.__cached_events = provider.gather_events(start, end)
        return self.__cached_events

    def _fill_events(self, days):
        for brain in self._events:
            dt = datetime.date(brain.start.year(), 
                               brain.start.month(),
                               brain.start.day())
            day = days[dt]
            events = day['events']
            allevents = day['allevents']
            event_dict = {'label': event_label(brain),
                          'url': brain.getURL(),
                          'description': brain.Description}
            if len(events) < 2:
                day['events'].append(event_dict)
            else:
                day['has_more'] = True
            allevents.append(event_dict)
            
    def month(self):
        return MONTHS[self.default_day.month]
    
    def year(self):
        return '%04i' % self.default_day.year

    def _link(self, dt):
        return '%s?year=%s&month=' % (self.context.absolute_url(),
                                      next.year,
                                      next.month)

    def next_month_link(self):
        year = self.default_day.year
        month = self.default_day.month
        
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        
        return '%s?year=%s&month=%s' % (self.context.absolute_url(),
                                        year,
                                        month)

    def prev_month_link(self):
        year = self.default_day.year
        month = self.default_day.month
        
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        
        return '%s?year=%s&month=%s' % (self.context.absolute_url(),
                                        year,
                                        month)
