from django.db import models


class DataABS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Schema(DataABS):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SchemaColumn(DataABS):
    TYPE_OF_COLUMN = (
        ('full_name', 'FullName'),
        ('integer', 'Integer'),
        ('company', 'Company'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain name', 'Domain name'),
        ('text', 'Text'),
        ('address', 'Address'),
        ('date', 'Date'),
        ('phone number', 'Phone number'),
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='columns')
    column_name = models.CharField(max_length=255)
    type_of_column = models.CharField(max_length=50, choices=TYPE_OF_COLUMN, default='full_name')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.column_name} {self.type_of_column} {self.order}'
