# Generated by Django 5.1 on 2024-09-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0002_rename_author_book_author_name_and_more'),
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerorder',
            old_name='user',
            new_name='user_email',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='book',
            new_name='book_name',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order',
            new_name='order_index',
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='order_index',
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetail',
            unique_together={('order_index', 'book_name')},
        ),
    ]
