from zope import interface
from zope import schema

class IPossibleCalendar(interface.Interface):
    """A marker interface for representing what *could* be a calendar.
    """

class ICalendarEnhanced(interface.Interface):
    """A marker interface to indicate an item that has calendar 
    functionality.
    """

class ICalendarConfig(interface.Interface):
    """Configuration information for a calendar.
    """
    
    calendar_activated = schema.Bool(
        title=u'Calendar Capabilities Activated',
        description=u'Whether calendar capabilities are or should be '
                    u'activated on this item'
        )

class IEventProvider(interface.Interface):
    """Provides events.
    """
    
    def gather_events(start, stop):
        """Return all appropriate events for the given time interval.  The
        *start* and *stop* arguments are expected to be python datetime
        objects.
        """

    def all_events():
        """Return all events. Used for exports and such.
        """

class IEvent(interface.Interface):
    """An event.
    """
    
    title = schema.TextLine(title=u'Title',
                            required=True,
                            readonly=True)
    description = schema.Text(title=u'Description',
                              required=False,
                              readonly=True)
    start = schema.Datetime(title=u'Start Time',
                            required=True,
                            readonly=True)
    end = schema.Datetime(title=u'End Time',
                          required=False,
                          readonly=True)
    local_url = schema.TextLine(title=u'URL',
                                required=True,
                                readonly=True)
    type = schema.TextLine(title=u'Type',
                           required=True,
                           readonly=False)
