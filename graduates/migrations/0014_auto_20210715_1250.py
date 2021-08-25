# Generated by Django 3.2 on 2021-07-15 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0013_auto_20210715_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='certificate',
            name='qr_code',
            field=models.ImageField(null=True, upload_to='qr_codes'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='student',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='graduates.student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='student_id'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(max_length=200),
        ),
    ]