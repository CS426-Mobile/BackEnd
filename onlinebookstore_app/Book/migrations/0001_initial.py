# Generated by Django 5.1 on 2024-09-04 02:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Author', '0001_initial'),
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('num_1_star', models.IntegerField()),
                ('num_2_star', models.IntegerField()),
                ('num_3_star', models.IntegerField()),
                ('num_4_star', models.IntegerField()),
                ('num_5_star', models.IntegerField()),
                ('description', models.TextField(max_length=1000)),
                ('public_date', models.DateField()),
                ('language', models.CharField(max_length=50)),
                ('weight', models.DecimalField(decimal_places=1, max_digits=4)),
                ('page_count', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Author.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Category.category')),
            ],
        ),
    ]
