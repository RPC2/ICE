# Generated by Django 2.1.7 on 2019-03-20 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_component_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='slug',
        ),
    ]
