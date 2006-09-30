import datetime
import calendar
from p4a.calendar import interfaces

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

class MonthView(object):
    """View for a month.
    """

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
        return calendar.firstweekday()

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

    def weeks(self, daydate=None):
        """Return as a list of of the (partial or full) weeks of the
        month which contains the datetime instance, *day*.  Each item
        in this list is a dict containing a key representing the day
        of the month (or in the case of a day that's not in that month,
        None).
        
        Start out by making sure we're able to get some weeks for today's
        date.
        
          >>> mt = MonthView()
          >>> len(mt.weeks()) > 1
          True

        Now lets query known dates.
        
          >>> from datetime import datetime
          >>> weeks = mt.weeks(datetime(2006, 2, 23))
          >>> len(weeks)
          5
          
        First day of the week period should be an outside month day.
        
          >>> weeks[0]['days'][0]
          {'extrastyleclass': ' outside-month first-week-day', 'events': [], 'day': None}

          >>> weeks[4]['days'][0]
          {'extrastyleclass': ' first-week-day', 'events': [], 'day': 27}
          
        Inspect the last day.  Should be outside the month as well.
        
          >>> weeks[-1]['days'][-1]
          {'extrastyleclass': ' outside-month last-week-day', 'events': [], 'day': None}
          
        """

        if daydate is None:
            daydate = self.default_day

        today = datetime.datetime.today().date()
        
        weektuples = list(calendar.monthcalendar(daydate.year, daydate.month))
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

            for daypos, weekday in enumerate(weektuple):
                day = {'events': []}
                week['days'].append(day)
                
                if weekday:
                    alldays[datetime.date(daydate.year, daydate.month, weekday)] = day
                
                day['extrastyleclass'] = ''
                
                if weekday and \
                        datetime.date(daydate.year, daydate.month, weekday) == today:
                    day['extrastyleclass'] += ' today'

                if weekday:
                    day['day'] = weekday
                else:
                    day['day'] = None
                    day['extrastyleclass'] += ' outside-month'
                    
                if daypos == 0:
                    day['extrastyleclass'] += ' first-week-day'
                elif daypos == 6:
                    day['extrastyleclass'] += ' last-week-day'
                    
                if weekday == 1:
                    day['extrastyleclass'] += ' first-month-day'

        # find the last day of the month and give it extra style class
        for day in reversed(weeks[-1]['days']):
            if day['day'] is not None:
                day['extrastyleclass'] += ' last-month-day'
                break
        
        self._fill_events(alldays)
        
        return weeks

    def _fill_events(self, days):
        if not hasattr(self, 'context'):
            return

        default = self.default_day
        
        start = datetime.datetime(default.year, default.month, 1, 0, 0)
        
        if default.month < 12:
            end = datetime.datetime(default.year, default.month+1, 1, 23, 59)
            end -= datetime.timedelta(days=1)
        elif default.month == 12:
            end = datetime.datetime(default.year, default.month, 31, 23, 59)
        
        eventprovider = interfaces.IEventProvider(self.context)

        for brain in eventprovider.gather_events(start, end):
            dt = datetime.date(brain.start.year(), 
                               brain.start.month(),
                               brain.start.day())
            day = days[dt]
            day['events'].append(brain)

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
