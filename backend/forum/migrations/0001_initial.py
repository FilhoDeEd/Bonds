# Generated by Django 5.1.3 on 2025-01-17 22:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('D', 'default'), ('U', 'user'), ('E', 'event')], default='U', max_length=5)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('description', models.TextField(max_length=2047)),
                ('subscribers_count', models.IntegerField(default=0)),
                ('popularity', models.FloatField(default=0.0)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('update_date', models.DateTimeField()),
                ('neighborhood', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='user_profile.neighborhood')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user_profile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('forum_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='forum.forum')),
                ('date', models.DateField()),
                ('location', models.TextField(max_length=1023)),
                ('cancelled', models.BooleanField(default=False)),
                ('five_star_mean', models.FloatField(default=0.0)),
            ],
            bases=('forum.forum',),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateField(editable=False)),
                ('is_sub', models.BooleanField(default=False)),
                ('forum', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='forum.forum')),
                ('user_profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='user_profile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('five_star', models.PositiveSmallIntegerField(choices=[(1, '1 - Terrível'), (2, '2 - Ruim'), (3, '3 - Regular'), (4, '4 - Bom'), (5, '5 - Excelente')])),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_profile.userprofile')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.event')),
            ],
        ),
    ]
