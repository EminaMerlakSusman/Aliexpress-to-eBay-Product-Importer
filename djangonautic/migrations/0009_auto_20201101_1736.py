# Generated by Django 3.1.1 on 2020-11-01 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangonautic', '0008_variationcombination_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationcombination',
            name='price',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
