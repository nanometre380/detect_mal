# Generated by Django 2.2.7 on 2019-12-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0003_black'),
    ]

    operations = [
        migrations.CreateModel(
            name='White',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
            ],
        ),
    ]
