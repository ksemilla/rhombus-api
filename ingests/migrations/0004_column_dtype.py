# Generated by Django 5.0.3 on 2024-03-27 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingests', '0003_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='dtype',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
