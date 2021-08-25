# Generated by Django 3.2 on 2021-08-13 12:05

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0003_activitylog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='university',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='university',
            name='phone_no1',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='university',
            name='phone_no2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
    ]
