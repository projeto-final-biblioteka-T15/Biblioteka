# Generated by Django 4.0.7 on 2023-07-05 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copies', '0003_alter_copies_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copies',
            name='available',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='copies',
            name='total',
            field=models.PositiveIntegerField(default=1),
        ),
    ]