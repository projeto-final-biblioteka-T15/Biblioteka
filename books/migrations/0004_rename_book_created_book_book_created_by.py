# Generated by Django 4.0.7 on 2023-07-04 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_bookowner_remove_book_users_book_book_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_created',
            new_name='book_created_by',
        ),
    ]
