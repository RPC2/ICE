# Generated by Django 2.2b1 on 2019-04-07 10:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0003_delete_quizresult'),
        ('courses', '0010_quizresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrollmentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=True)),
                ('date_completed', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learner')),
            ],
        ),
    ]
