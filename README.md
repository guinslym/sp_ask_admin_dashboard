
Sp Ask DashBoard
======================================================

Yet Another LibraryH3lp Ask Dashboard


## Screenshots
<p float="left">
<img src="screenshots/homepage.png" width="100%"/>
</p>


## Installation
Clone this repository. On your command line, navigate in the location of this local repository, type this:

		pip install -r requirements.txt

## Configuration - Mac OSX and Linux

In ~/.lh3/config::

        [default]
        server = ca.libraryh3lp.com
        timezone = America/Toronto
        salt = "you should probably change this"

The `salt` is used when generating system-level utility accounts.
This is not something you do often.  If your `salt` is unique, your
passwords will be unique.

In ~/.lh3/credentials::

        [default]
        username = <ADMIN_USER>
        password = <ADMIN_PASS>

## Configuration - Windows

In the current directory, rename **.env-exemple** to **.env**. Add your LibraryH3lp username and password

        salt=asjdflkajs
        scheme=https
        server=ca.libraryh3lp.com
        timezone=America/Toronto
        version=v2
        username=
        password=


## Usage
	python manage.py runserver
        
open your browser on http://127.0.0.1:8000/
