# Generated by Django 5.1.7 on 2025-03-26 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='ticket_name',
        ),
    ]
