# Generated by Django 5.1 on 2025-02-01 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0005_remove_ticket_cashier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='number',
            new_name='phone_number',
        ),
    ]
