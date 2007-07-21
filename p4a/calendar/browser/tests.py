import unittest
from zope.testing import doctest
from p4a.calendar.browser.test_month import TestHourTimeFormatter

def test_suite():
    suite = unittest.TestSuite((
        doctest.DocTestSuite('p4a.calendar.browser.month'),
        ))
    suite.addTest(unittest.makeSuite(TestHourTimeFormatter))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
