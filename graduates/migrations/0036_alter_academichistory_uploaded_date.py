# Generated by Django 3.2 on 2021-08-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0035_auto_20210820_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academichistory',
            name='uploaded_date',
            field=models.DateField(auto_now=True),
        ),
    ]
