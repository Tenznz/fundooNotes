# Generated by Django 4.0.1 on 2022-03-17 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginData',
        ),
    ]