#!/bin/bash
python manage.py makemessages -l en --extension=py,html \
  --ignore=venv/* \
  --ignore=manage.py \
  --ignore=*/migrations/*