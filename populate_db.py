"""Populate db with some dummy data"""
import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth import get_user_model

from bakersoft.trackings.models import Project, Work

USER = get_user_model()

# account=admin, id 1
admin = USER.objects.get(id=1)
project = Project.objects.create(account=admin, manager=admin, name="Bake")
work = Work.objects.create(account=admin, project=project, name="mold")
time.sleep(2)
work.completed = True
work.status = "done"
work.save()
work = Work.objects.create(account=admin, project=project, name="ferment")
