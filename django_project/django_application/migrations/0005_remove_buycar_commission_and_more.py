# Generated by Django 4.1.1 on 2022-09-27 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_application', '0004_alter_buycar_commission_alter_buycar_net_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buycar',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='buycar',
            name='commission_currency',
        ),
    ]
