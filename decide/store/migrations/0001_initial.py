# Generated by Django 2.0 on 2022-12-12 16:03

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_id', models.PositiveIntegerField()),
                ('voter_id', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('V', 'Voting'), ('BV', 'BinaryVoting')], default='V', max_length=2)),
                ('a', base.models.BigBigField()),
                ('b', base.models.BigBigField()),
                ('voted', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
