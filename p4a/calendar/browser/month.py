import datetime
import calendar

class MonthView(object):
    """View for a month.
    """

    def events_for_interval(self, start, stop):
        pass

    def weeks(self, day=None):
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
          >>> weeks = mt.weeks(datetime(2006, 9, 23))
          >>> len(weeks)
          5
          
        First day of the week period should be an outside month day.
        
          >>> weeks[0]['days'][0]
          {'extrastyleclass': ' outside-month first-week-day', 'day': None}

          >>> weeks[4]['days'][0]
          {'extrastyleclass': ' first-week-day', 'day': 25}
          
        Inspect the last day.  Should be outside the month as well.
        
          >>> weeks[-1]['days'][-1]
          {'extrastyleclass': ' outside-month last-week-day', 'day': None}
          
        """        
        
        if day is None:
            day = datetime.datetime.today()
        
        weektuples = list(calendar.monthcalendar(day.year, day.month))
        weeks = []
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
                
                day['extrastyleclass'] = ''
                
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
        
        return weeks
