# Generated by Django 5.1 on 2024-09-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerCartBook', '0003_customercartbook_num_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercartbook',
            name='num_books',
            field=models.IntegerField(default=1),
        ),
    ]
