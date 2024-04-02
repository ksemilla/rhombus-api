from django.contrib import admin
from .models import Ingest, Column, Record

admin.site.register(Ingest)
admin.site.register(Column)
admin.site.register(Record)
