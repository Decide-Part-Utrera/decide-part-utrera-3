# Generated by Django 2.0 on 2022-12-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20221212_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='tipo',
            field=models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('DHONT', 'DHONT'), ('IMPERIALI', 'IMPERIALI')], default='IMPERIALI', max_length=20, verbose_name='Count method'),
        ),
    ]
