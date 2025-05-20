#!/bin/bash
python manage.py makemessages -l fr --extension=py,html \
  --ignore=venv/* \
  --ignore=manage.py \
  --ignore=*/migrations/*