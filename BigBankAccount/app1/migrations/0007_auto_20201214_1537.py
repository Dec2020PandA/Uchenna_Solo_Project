# Generated by Django 2.2 on 2020-12-14 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_user_coin_count_clicker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='coin_count_clicker',
            new_name='coin_click_counter',
        ),
    ]