# Generated by Django 5.1.1 on 2024-10-04 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentRoomCustomer', '0008_product_amenities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]