# Generated by Django 5.0.4 on 2024-05-08 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cgapp', '0004_adminlogin_contact_no_adminlogin_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_pic',
        ),
    ]
