# Generated by Django 2.2 on 2023-02-13 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Projekti', '0003_remove_variation_variation_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitem',
            name='variation',
        ),
    ]
