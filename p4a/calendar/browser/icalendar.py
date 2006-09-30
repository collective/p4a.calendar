from Products.CMFCore.utils import getToolByName
from p4a.calendar.interfaces import IEventProvider

class iCalendarView(object):
    """ Export the contents of this Calendar as an iCalendar file """
        
    def exportCalendar(self, REQUEST=None):
        """ Export the contents of this Calendar as an iCalendar file """
        ct = getToolByName(self, 'portal_calendar')
        eventprovider = IEventProvider(self.context)
        events = [x.getObject() for x in eventprovider.all_events()]
        self.request.RESPONSE.setHeader(
            'Content-Type', 'text/calendar;charset=utf-8')
        return ct.exportCalendar(events=events, REQUEST=REQUEST)

    def PUT(self, REQUEST, RESPONSE):
        """This is a PUT method for iCalendar access.
        
        The PUT method is found on the view "icalendar.ics". This
        can be slightly confusing, as it's there is no configure.zcml
        entry for it.
        """
        #ical_text = REQUEST['BODYFILE']
        #file.seek(0)
        ct = getToolByName(self.context, 'portal_calendar')
        ct.importCalendar(REQUEST['BODYFILE'], dest=self.context, do_action=True)
        RESPONSE.setStatus(204)
        return RESPONSE