Asset Manager
=================

Installation
------------

  1. Install [pip](http://www.pip-installer.org/en/latest/installing.html)
  2. Make a [virtualenv](http://virtualenvwrapper.readthedocs.org/en/latest/#introduction) for this project
  3. Install the required dependencies: `pip install -r requirements.txt`

Import data from RSS:

   python manage.py import -u http://www.wdcdn.net/rss/presentation/library/client/iowa/id/e5d10087fd878ba5dc8ea7857495710b

Run the app:
------------

    python manage.py runserver

Goto: [http://localhost:8888/asset](http://localhost:8888/asset)
