# Generated by Django 3.0.8 on 2020-07-17 20:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.GenericIPAddressField(null=True, validators=[django.core.validators.validate_ipv4_address])),
                ('status', models.BooleanField(default=False)),
                ('env', models.CharField(choices=[('PRODUCTION', 'PRODUCTION'), ('HOMOLOGATION', 'HOMOLOGATION'), ('DEV', 'DEV')], max_length=20)),
                ('version', models.CharField(max_length=5)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('CRITICAL', 'CRITICAL'), ('DEBUG', 'DEBUG'), ('ERROR', 'ERROR'), ('WARNING', 'WARNING'), ('INFO', 'INFO')], max_length=20)),
                ('data', models.TextField(max_length=500)),
                ('shelved', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Agent')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
