# Generated by Django 5.1.1 on 2024-10-06 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('network_name', models.CharField(max_length=50)),
                ('template_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('position', models.IntegerField()),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='templatess.template')),
            ],
        ),
    ]
