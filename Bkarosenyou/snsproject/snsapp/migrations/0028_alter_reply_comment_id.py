# Generated by Django 3.2 on 2024-02-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snsapp', '0027_auto_20240202_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='comment_id',
            field=models.IntegerField(default=99),
        ),
    ]