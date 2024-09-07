# Generated by Django 5.1 on 2024-09-07 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCartBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Book.book')),
            ],
        ),
    ]
