import datetime
import calendar
try:
    from Products.Five.browser.pagetemplatefile import \
         ZopeTwoPageTemplateFile as PageTemplateFile
except ImportError:
    from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from p4a.calendar import interfaces

class EventListingView(object):
    """View that lists events.
    """
    
    eventlist = PageTemplateFile('events.pt')
    
    def _getEventList(self, start=None, stop=None):
        provider = interfaces.IEventProvider(self.context)
        now = datetime.datetime.now()
        events = list(provider.gather_events(start=start, stop=stop))
        events.sort()
        months = []
        month_info = []
        old_month_year = None
        for event in events:
            start = event.start
            month = str(start.month)
            year = str(start.year)
            month_year = year+month
            if month_year != old_month_year:
                if month_info:
                    months.append(month_info)
                month_info = {'month': start.month,
                              'year': start.year,
                              'month_name': start.strftime("%B"),
                              'events': []}
            event_dict = {'event': event,
                          'day': start.day,
                          'title': event.title,
                          'description': event.description,
                          'url': event.local_url,
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)
            
        return months
        
    def upcomingEvents(self):
        now = datetime.datetime.now()
        months = self._getEventList(start=now)
        return self.eventlist(months=months, show_past=False)

    def pastEvents(self):
        now = datetime.datetime.now()
        months = self._getEventList(stop=now)
        return self.eventlist(months=months, show_past=True)

    def event_creation_link(self, start=None, stop=None):
        provider = interfaces.IEventProvider(self.context)
        return provider.event_creation_link(start, stop)
