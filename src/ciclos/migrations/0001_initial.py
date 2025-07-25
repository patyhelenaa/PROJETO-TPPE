# Generated by Django 5.2.1 on 2025-07-17 04:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('data', models.DateField()),
                ('dia_menstruada', models.BooleanField()),
                ('duracao_ciclo', models.PositiveIntegerField()),
                ('duracao_menstruacao', models.PositiveIntegerField()),
                ('fluxo_menstrual', models.CharField(
                    choices=[
                        ('LEVE', 'Leve'),
                        ('MODERADO', 'Moderado'),
                        ('INTENSO', 'Intenso'),
                        ('MUITO_INTENSO', 'Muito Intenso')
                    ],
                    max_length=20
                )),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ciclos',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'db_table': 'ciclo',
            },
        ),
    ]
