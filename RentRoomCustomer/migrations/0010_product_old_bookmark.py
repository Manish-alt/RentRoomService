# Generated by Django 5.1.1 on 2024-10-06 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentRoomCustomer', '0009_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_bookmark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
