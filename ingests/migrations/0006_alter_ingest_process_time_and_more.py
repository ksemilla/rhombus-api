# Generated by Django 5.0.3 on 2024-03-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingests', '0005_ingest_process_time_ingest_processed_row_nums_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingest',
            name='process_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ingest',
            name='processed_row_nums',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ingest',
            name='row_nums',
            field=models.BigIntegerField(default=0),
        ),
    ]
