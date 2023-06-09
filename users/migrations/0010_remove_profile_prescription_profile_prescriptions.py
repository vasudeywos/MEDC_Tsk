# Generated by Django 4.1.7 on 2023-06-07 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Med', '0008_appointment_pay_amount'),
        ('users', '0009_alter_profile_prescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='prescription',
        ),
        migrations.AddField(
            model_name='profile',
            name='prescriptions',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='Med.prescription'),
        ),
    ]