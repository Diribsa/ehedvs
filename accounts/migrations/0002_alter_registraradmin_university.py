# Generated by Django 3.2 on 2021-08-13 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin', '0006_alter_university_fax_no'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registraradmin',
            name='university',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='super_admin.university'),
        ),
    ]
