# Generated by Django 3.2.4 on 2021-06-23 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210623_1341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post_pk',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]