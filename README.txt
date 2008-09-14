;-*-rst-*-

============
p4a.calendar
============

TODO: Add some info here about how to install with buildout and what the dependencies are (see setup.py)

Overview
========

The *p4a.calendar* package is a package for producing calendars from
collection of events. Features include:

Monthly, Weekly, Daily view
  Any calendar activated (smart) folder can has several default views
  including a monthly, weekly and daily view.

Chronological event view
  The events gathered together by the activated calendar can be displayed
  using a chronological event listing.
  
Past events view
  Events that have already occurred are grouped into a past events listing page.

Color coding by event type
  Events can be color coded based on what event type (keyword) they have 
  been assigned.


Installation
============

  1. When you're reading this you have probably already run 
     ``easy_install p4a.calendar``. Find out how to install setuptools
     (and EasyInstall) here:
     http://peak.telecommunity.com/DevCenter/EasyInstall

  2. For installation into a Zope environment, create a file called 
     ``p4a.calendar-configure.zcml`` in the 
     ``/path/to/instance/etc/package-includes`` directory.  The file
     should only contain this::

        <include package="p4a.calendar" />


Credits
=======

  * Maintainer, Lennart Regebro - regebro (at) gmail.com
  * Rocky Burt - rocky (at) serverzen.com
  * Nate Aune - natea (at) jazkarta.com
