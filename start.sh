#!/bin/bash
# Start Daphne server
daphne -b 0.0.0.0 -p 8001 transport_system.asgi:application &
# Start Django's development server (if needed)
python manage.py runserver

