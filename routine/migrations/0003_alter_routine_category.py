# Generated by Django 3.2.13 on 2023-02-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0002_auto_20230212_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='category',
            field=models.CharField(choices=[('기상', '기상'), ('HOMEWORK', 'HOMEWORK')], max_length=50),
        ),
    ]