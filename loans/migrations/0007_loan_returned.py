# Generated by Django 4.0.7 on 2023-07-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_remove_loan_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
