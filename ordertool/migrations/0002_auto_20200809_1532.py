# Generated by Django 3.1 on 2020-08-09 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordertool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userjob',
            name='idxml',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
