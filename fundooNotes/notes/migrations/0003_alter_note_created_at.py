# Generated by Django 4.0.1 on 2022-05-02 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
