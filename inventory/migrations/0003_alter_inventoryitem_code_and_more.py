# Generated by Django 5.0.7 on 2024-07-29 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_category_options_inventoryitem_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='code',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
