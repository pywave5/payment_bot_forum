# Generated by Django 5.1.7 on 2025-04-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_referral'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='blogger_name',
        ),
        migrations.AddField(
            model_name='referral',
            name='user_id',
            field=models.BigIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='referral',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
