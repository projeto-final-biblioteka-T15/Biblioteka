# Generated by Django 4.0.7 on 2023-07-05 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_options_book_author_book_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]