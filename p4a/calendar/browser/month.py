import datetime
import calendar
from Products.CMFCore import utils as cmfutils
from DateTime import DateTime

DAYS = [
        'Monday', 
        'Tuesday', 
        'Wednesday', 
        'Thursday', 
        'Friday', 
        'Saturday'
        'Sunday',                 
        ]

def dt2DT(dt):
    s = "%04i-%02i-%02i %02i:%02i" % (dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return DateTime(s)

class MonthView(object):
    """View for a month.
    """

    def events_for_interval(self, start, stop):
        pass

    @property
    def default_day(self):
        if not hasattr(self, 'request'):
            return datetime.datetime.today()
        
        year = self.request.form.get('year', None)
        month = self.request.form.get('month', None)
        
        if month is None:
            return datetime.datetime.today()
        
        year = year or datetime.datetime.today().year
        year = int(year)
        month = int(month)
        
        return datetime.datetime(year, month, 1)

    def standard_week_days(self):
        days = [{'day': x} for x in DAYS[calendar.firstweekday():]]
        days += [{'day': x} for x in DAYS[0:calendar.firstweekday()]]

        days[0]['extrastyleclass'] = 'first-week-day'
        days[-1]['extrastyleclass'] = 'last-week-day'

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
          {'extrastyleclass': ' outside-month first-week-day', 'day': None}

          >>> weeks[4]['days'][0]
          {'extrastyleclass': ' first-week-day', 'day': 27}
          
        Inspect the last day.  Should be outside the month as well.
        
          >>> weeks[-1]['days'][-1]
          {'extrastyleclass': ' outside-month last-week-day', 'day': None}
          
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
            elif weekpos == len(weektuples):
                week['extrastyleclass'] += ' last-week'

            for daypos, weekday in enumerate(weektuple):
                day = {}
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
        default = self.default_day
        
        start = datetime.datetime(default.year, default.month, 1, 0, 0)
        
        if default.month < 12:
            end = datetime.datetime(default.year, default.month+1, 1, 23, 59)
            end -= datetime.timedelta(days=1)
        elif default.month == 12:
            end = datetime.datetime(default.year, default.month, 31, 23, 59)
        
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')
        catalog(portal_type='Event',
                start=dt2DT(start),
                end=dt2DT(end))

