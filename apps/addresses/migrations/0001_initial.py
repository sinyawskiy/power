# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='\u0428\u0438\u0440\u043e\u0442\u0430')),
                ('address', models.CharField(blank=True, help_text='\u0437\u0430\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438', max_length=255, null=True, verbose_name='\u0430\u0434\u0440\u0435\u0441')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0430\u0434\u0440\u0435\u0441',
                'verbose_name_plural': '\u0430\u0434\u0440\u0435\u0441\u0430 \u043e\u0431\u044a\u0435\u043a\u0442\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='CityArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0439\u043e\u043d\u0430')),
            ],
            options={
                'verbose_name': '\u0440\u0430\u0439\u043e\u043d',
                'verbose_name_plural': '\u0440\u0430\u0439\u043e\u043d\u044b',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='city_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.CityArea', verbose_name='\u0440\u0430\u0439\u043e\u043d'),
        ),
    ]
