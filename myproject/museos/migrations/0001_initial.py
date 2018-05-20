# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ident', models.CharField(max_length=32)),
                ('Nombre', models.TextField()),
                ('Nombre_via', models.CharField(max_length=32)),
                ('Clase_vial', models.CharField(max_length=32)),
                ('Numero', models.CharField(max_length=32)),
                ('Localidad', models.CharField(max_length=32)),
                ('Provincia', models.CharField(max_length=32)),
                ('Cod_Postal', models.CharField(max_length=32)),
                ('Barrio', models.CharField(max_length=32)),
                ('Distrito', models.CharField(max_length=32)),
                ('Coord_X', models.CharField(max_length=32)),
                ('Coord_Y', models.CharField(max_length=32)),
                ('Enlace', models.CharField(max_length=256)),
                ('Descripcion', models.TextField()),
                ('Accesibilidad', models.CharField(max_length=32)),
                ('Telefono', models.CharField(max_length=15)),
                ('Email', models.CharField(max_length=20)),
                ('Num_Comentario', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Titulo_pagina', models.CharField(max_length=32)),
                ('Tamano', models.FloatField(default=1)),
                ('Color', models.CharField(max_length=32)),
                ('Nombre', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fecha',
            name='Museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='fecha',
            name='Usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='Museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
