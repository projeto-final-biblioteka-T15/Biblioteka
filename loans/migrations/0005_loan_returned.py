# Generated by Django 4.0.7 on 2023-07-05 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_alter_loan_copy_alter_loan_loan_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='returned',
            field=models.BooleanField(default=True),
        ),
    ]
