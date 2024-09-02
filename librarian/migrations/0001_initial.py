# Generated by Django 5.0.8 on 2024-09-02 08:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('employee_id', models.IntegerField(unique=True)),
                ('address', models.TextField(blank=True)),
                ('mobile_no', models.IntegerField(max_length=10, unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('password', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
