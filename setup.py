from setuptools import setup, find_packages

version = '2.0a4'

f = open('README.txt')
readme = f.read()
f.close()

f = open('CHANGES.txt')
changes = f.read()
f.close()


setup(name='p4a.calendar',
      version=version,
      description="Plone4Artists calendar abstraction library",
      long_description=readme + '\n\n' + changes,
      classifiers=[
          'Framework :: Zope3',
          'Programming Language :: Python',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      keywords='Plone4Artists calendar event calendaring icalendar ical',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      url='http://www.plone4artists.org/products/plone4artistscalendar',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['p4a'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.common >= 1.0.1, <= 1.0.9999',
          'p4a.z2utils >=1.0, <= 1.0.9999',
      ],
      )
