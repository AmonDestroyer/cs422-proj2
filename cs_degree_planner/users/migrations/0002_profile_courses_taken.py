# Generated by Django 4.2 on 2023-05-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='courses_taken',
            field=models.ManyToManyField(to='forecast.course'),
        ),
    ]
