# Generated by Django 3.1.3 on 2021-01-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_auto_20210121_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='dr_cr',
            field=models.CharField(default='nil', editable=False, max_length=2, verbose_name='Dr/Cr'),
        ),
    ]
