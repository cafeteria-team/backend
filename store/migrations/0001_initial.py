# Generated by Django 3.2.9 on 2022-05-31 00:11

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=24, verbose_name='편의시설 이름')),
                ('category', models.CharField(choices=[('CAFE', '카페'), ('COFFEE', '커피'), ('CONVEIENCE', '편의점'), ('NOODEL', '면'), ('BREAD', '빵'), ('BEVERAGE', '음료')], default='', max_length=15, verbose_name='편의시설 카테고리')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'facility',
                'db_table': 'facility',
            },
        ),
        migrations.CreateModel(
            name='JoinFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'join_facility',
                'db_table': 'join_facility',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('addr', models.CharField(max_length=128)),
                ('zip_code', models.CharField(max_length=6)),
                ('detail_addr', models.CharField(blank=True, max_length=128)),
                ('busi_num', models.CharField(max_length=10)),
                ('busi_num_img', models.CharField(blank=True, max_length=256)),
                ('price', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict), blank=True, null=True, size=None)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'store',
                'db_table': 'store',
            },
        ),
    ]
