# Generated by Django 4.0.5 on 2022-06-22 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_time', '0003_rename_scadual_schedule_alter_employee_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]