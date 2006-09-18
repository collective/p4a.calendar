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
