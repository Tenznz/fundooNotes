# Generated by Django 4.0.1 on 2022-05-16 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0018_alter_collaborator_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notes.note'),
        ),
    ]