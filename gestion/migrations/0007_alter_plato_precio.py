# Generated by Django 5.1.1 on 2024-09-12 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_alter_plato_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plato',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
