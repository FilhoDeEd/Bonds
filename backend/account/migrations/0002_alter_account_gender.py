# Generated by Django 5.1.3 on 2024-11-29 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro')], max_length=5, null=True),
        ),
    ]