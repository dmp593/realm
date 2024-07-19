# Generated by Django 5.0.7 on 2024-07-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(choices=[('user-short-lived', 'Facebook Short-Lived User Access Token'), ('user-long-lived', 'Facebook Long-Lived User Access Token'), ('app', 'Facebook App Access Token'), ('page', 'Facebook Page Access Token')], max_length=50)),
                ('access_token', models.CharField(max_length=255)),
                ('expiry', models.DateTimeField()),
            ],
            options={
                'ordering': ('-expiry',),
            },
        ),
    ]
