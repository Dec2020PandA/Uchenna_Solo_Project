# Generated by Django 2.2 on 2020-12-15 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_user_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
