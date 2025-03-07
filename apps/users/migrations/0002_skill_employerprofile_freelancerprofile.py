# Generated by Django 5.1.3 on 2025-01-11 06:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('posted_projects', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FreelancerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('portfolio', models.URLField(blank=True, null=True)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('rating', models.FloatField(default=0.0)),
                ('completed_projects', models.PositiveIntegerField(default=0)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='freelancer_profiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='freelancer_profile', to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, to='users.skill')),
            ],
        ),
    ]
