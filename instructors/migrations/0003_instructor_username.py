# Generated by Django 2.1.7 on 2019-04-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0002_auto_20190405_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]