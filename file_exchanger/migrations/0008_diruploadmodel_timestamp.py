# Generated by Django 4.2.2 on 2023-08-07 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_exchanger', '0007_alter_diruploadmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diruploadmodel',
            name='timestamp',
            field=models.IntegerField(default=123456),
            preserve_default=False,
        ),
    ]
