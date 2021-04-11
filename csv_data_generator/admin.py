from django.contrib import admin

from csv_data_generator.models import Schema, SchemaColumn

admin.site.register(Schema)
admin.site.register(SchemaColumn)
