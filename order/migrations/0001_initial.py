# Generated by Django 5.1.7 on 2025-03-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('total_cost', models.IntegerField()),
                ('payment_method', models.CharField(max_length=255)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
    ]
