# Generated by Django 4.0.7 on 2023-07-05 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_remove_loan_copy'),
        ('books', '0006_alter_book_published_date'),
        ('copies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('available', models.PositiveIntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='books.book')),
            ],
        ),
        migrations.DeleteModel(
            name='Copy',
        ),
    ]
