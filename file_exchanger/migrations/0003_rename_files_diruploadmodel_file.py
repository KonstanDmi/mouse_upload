# Generated by Django 4.2.2 on 2023-07-19 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_exchanger', '0002_alter_diruploadmodel_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diruploadmodel',
            old_name='files',
            new_name='file',
        ),
    ]
