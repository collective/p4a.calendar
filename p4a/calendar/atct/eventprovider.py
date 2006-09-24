from zope import interface
from zope import component

from p4a.calendar import interfaces
from DateTime import DateTime
from Products.CMFCore import utils as cmfutils
from Products.Archetypes import atapi
from Products.ATContentTypes.content import topic

def dt2DT(dt):
    s = "%04i-%02i-%02i %02i:%02i" % (dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return DateTime(s)

class ATEventProvider(object):
    interface.implements(interfaces.IEventProvider)
    component.adapts(atapi.BaseObject)

    def __init__(self, context):
        self.context = context
        
    def gather_events(self, start, stop):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        event_brains = catalog(portal_type='Event',
                               path=path,
                               start={'query': dt2DT(start), 'range': 'min'},
                               end={'query': dt2DT(stop), 'range': 'max'})

        return event_brains

class TopicEventProvider(object):
    interface.implements(interfaces.IEventProvider)
    component.adapts(topic.ATTopic)

    def __init__(self, context):
        self.context = context
        
    def gather_events(self, start, stop):
        return (x for x in self.context.queryCatalog() 
                if x.portal_type == 'Event')
