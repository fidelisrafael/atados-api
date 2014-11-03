# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atados_core.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'Email')),
                ('name', models.CharField(max_length=200, verbose_name='Name', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='Email verified')),
                ('joined_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('hidden_address', models.BooleanField(default=False, verbose_name='Endereco escondido.')),
                ('site', models.URLField(default=None, null=True, blank=True)),
                ('phone', models.CharField(default=None, max_length=20, null=True, verbose_name='Phone', blank=True)),
                ('legacy_uid', models.PositiveIntegerField(null=True, blank=True)),
                ('token', models.CharField(default=None, max_length=64, unique=True, null=True, verbose_name='token')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zipcode', models.CharField(default=None, max_length=10, null=True, verbose_name='Zip code', blank=True)),
                ('addressline', models.CharField(default=None, max_length=200, null=True, verbose_name='Street', blank=True)),
                ('addressnumber', models.CharField(default=None, max_length=10, null=True, verbose_name='Address number', blank=True)),
                ('addressline2', models.CharField(default=None, max_length=100, null=True, verbose_name='Apt, PO Box, block', blank=True)),
                ('neighborhood', models.CharField(default=None, max_length=50, null=True, verbose_name='Neighborhood', blank=True)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'address',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('canceled', models.BooleanField(default=False, verbose_name='Canceled')),
                ('canceled_date', models.DateTimeField(null=True, verbose_name='Canceled date', blank=True)),
            ],
            options={
                'verbose_name': 'apply',
                'verbose_name_plural': 'applies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
            ],
            options={
                'verbose_name': 'apply status',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.PositiveSmallIntegerField(verbose_name='weekday', choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (0, 'Sunday')])),
                ('period', models.PositiveSmallIntegerField(verbose_name='period', choices=[(0, 'Morning'), (1, 'Afternoon'), (2, 'Evening')])),
            ],
            options={
                'verbose_name': 'availability',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'cause',
                'verbose_name_plural': 'causes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('active', models.BooleanField(default=False, verbose_name='City where Atados is present.')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='Deleted date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('address', models.OneToOneField(null=True, blank=True, to='atados_core.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='End date', blank=True)),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nonprofit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('details', models.TextField(default=None, max_length=2048, null=True, verbose_name='Details', blank=True)),
                ('description', models.TextField(max_length=160, null=True, verbose_name='Short description', blank=True)),
                ('website', models.URLField(default=None, null=True, blank=True)),
                ('facebook_page', models.URLField(default=None, null=True, blank=True)),
                ('google_page', models.URLField(default=None, null=True, blank=True)),
                ('twitter_handle', models.URLField(default=None, null=True, blank=True)),
                ('image', models.ImageField(default=None, upload_to=atados_core.models.nonprofit_image_name, null=True, verbose_name='Logo 200x200', blank=True)),
                ('cover', models.ImageField(default=None, upload_to=atados_core.models.nonprofit_cover_name, null=True, verbose_name='Cover 1450x340', blank=True)),
                ('highlighted', models.BooleanField(default=False, verbose_name='Highlighted')),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('published_date', models.DateTimeField(null=True, verbose_name='Published date', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='Deleted date', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('causes', models.ManyToManyField(to='atados_core.Cause', null=True, blank=True)),
                ('companies', models.ManyToManyField(to='atados_core.Company', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'nonprofit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Project name')),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('details', models.TextField(max_length=2048, verbose_name='Details')),
                ('description', models.TextField(max_length=160, null=True, verbose_name='Short description', blank=True)),
                ('facebook_event', models.URLField(default=None, null=True, blank=True)),
                ('responsible', models.CharField(max_length=50, null=True, verbose_name='Responsible name', blank=True)),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='Phone', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='E-mail', blank=True)),
                ('published', models.BooleanField(default=False, verbose_name='Published')),
                ('published_date', models.DateTimeField(null=True, verbose_name='Published date', blank=True)),
                ('closed', models.BooleanField(default=False, verbose_name='Closed')),
                ('closed_date', models.DateTimeField(null=True, verbose_name='Closed date', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='Deleted date', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('highlighted', models.BooleanField(default=False, verbose_name='Highlighted')),
                ('legacy_nid', models.PositiveIntegerField(null=True, blank=True)),
                ('image', models.ImageField(default=None, upload_to=atados_core.models.project_image_name, null=True, verbose_name='Image 350x260', blank=True)),
                ('address', models.OneToOneField(null=True, blank=True, to='atados_core.Address')),
                ('causes', models.ManyToManyField(to='atados_core.Cause')),
                ('companies', models.ManyToManyField(to='atados_core.Company', null=True, blank=True)),
                ('nonprofit', models.ForeignKey(to='atados_core.Nonprofit')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='Sort', blank=True)),
                ('city', models.ForeignKey(default=None, blank=True, to='atados_core.City', null=True)),
                ('project', models.ForeignKey(to='atados_core.Project')),
            ],
            options={
                'verbose_name': 'recommendation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=50, null=True, verbose_name='Role name', blank=True)),
                ('prerequisites', models.TextField(default=None, max_length=1024, null=True, verbose_name='Prerequisites', blank=True)),
                ('details', models.TextField(default=None, max_length=1024, null=True, verbose_name='Details', blank=True)),
                ('vacancies', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='Vacancies', blank=True)),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'skill',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('code', models.CharField(max_length=2, verbose_name='code')),
            ],
            options={
                'verbose_name': 'state',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facebook_uid', models.CharField(max_length=255, blank=True)),
                ('facebook_access_token', models.CharField(max_length=255, blank=True)),
                ('facebook_access_token_expires', models.PositiveIntegerField(null=True, blank=True)),
                ('birthDate', models.DateField(default=None, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(default=None, null=True, upload_to=atados_core.models.volunteer_image_name, blank=True)),
                ('causes', models.ManyToManyField(to='atados_core.Cause', null=True, blank=True)),
                ('skills', models.ManyToManyField(to='atados_core.Skill', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'volunteer',
                'verbose_name_plural': 'volunteers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekly_hours', models.PositiveSmallIntegerField(null=True, verbose_name='Weekly hours', blank=True)),
                ('can_be_done_remotely', models.BooleanField(default=False, verbose_name='This work can be done remotely.')),
                ('availabilities', models.ManyToManyField(to='atados_core.Availability')),
                ('project', models.OneToOneField(null=True, blank=True, to='atados_core.Project')),
            ],
            options={
                'verbose_name': 'work',
                'verbose_name_plural': 'works',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='state',
            field=models.ForeignKey(default=None, blank=True, to='atados_core.State', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(to='atados_core.Role', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(to='atados_core.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nonprofit',
            name='volunteers',
            field=models.ManyToManyField(to='atados_core.Volunteer', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.OneToOneField(null=True, blank=True, to='atados_core.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(to='atados_core.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='atados_core.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apply',
            name='project',
            field=models.ForeignKey(to='atados_core.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apply',
            name='status',
            field=models.ForeignKey(to='atados_core.ApplyStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apply',
            name='volunteer',
            field=models.ForeignKey(to='atados_core.Volunteer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(default=None, blank=True, to='atados_core.City', null=True, verbose_name='City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.OneToOneField(null=True, blank=True, to='atados_core.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, to='atados_core.Company', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='AddressProject',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('atados_core.project',),
        ),
    ]
