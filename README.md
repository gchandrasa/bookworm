# BookWorm
Just a simple book review system


## Quick Start Guide

- Clone the repository.

        git clone git@github.com:gchandrasa/bookworm.git

- Install libraries from requirements.txt, it's recommended to use virtualenv

        cd bookworm
        pip install -r requirements.txt
        
- Create your local settings

        cp bookworm/settings/local.example.py bookworm/settings/local.py
        
- Migrate database

        ./manage.py migrate
        
- Done. Start the local server

        ./manage.py runserver