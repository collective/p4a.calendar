from zope.formlib import form
from p4a.calendar import interfaces

class ConfigView(form.PageEditForm):
    """Calendar configuration.
    """
    
    form_fields = form.FormFields(interfaces.ICalendarConfig)
