# Generated by Django 2.0.5 on 2020-03-26 20:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('level', models.CharField(choices=[('KG_1', 'Kindergarten 1'), ('KG_2', 'Kindergarten 2'), ('B_1', 'Basic 1'), ('B_2', 'Basic 2'), ('B_3', 'Basic 3'), ('B_4', 'Basic 4'), ('B_5', 'Basic 5'), ('B_6', 'Basic 6'), ('B_7', 'Basic 7'), ('B_8', 'Basic 8'), ('B_9', 'Basic 9'), ('B_10', 'Basic 10'), ('B_11', 'Basic 12'), ('B_12', 'Basic 12')], max_length=15)),
                ('strand', models.IntegerField(validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)])),
                ('sub_strand', models.IntegerField()),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ('-level', 'strand', 'sub_strand'),
            },
        ),
    ]
