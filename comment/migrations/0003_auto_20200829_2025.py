# Generated by Django 3.0.3 on 2020-08-29 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20200829_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_to',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='root',
        ),
    ]
