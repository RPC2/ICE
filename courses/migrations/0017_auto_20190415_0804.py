# Generated by Django 2.1.7 on 2019-04-15 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20190411_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='pass_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='enrollmenthistory',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]