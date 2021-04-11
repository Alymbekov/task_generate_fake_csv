# Generated by Django 3.2 on 2021-04-11 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SchemaColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=255)),
                ('type_of_column', models.CharField(choices=[('full_name', 'FullName'), ('integer', 'Integer'), ('company', 'Company'), ('job', 'Job'), ('email', 'Email'), ('domain name', 'Domain name'), ('text', 'Text'), ('address', 'Address'), ('date', 'Date'), ('phone number', 'Phone number')], default='full_name', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csv_data_generator.schema')),
            ],
        ),
    ]
