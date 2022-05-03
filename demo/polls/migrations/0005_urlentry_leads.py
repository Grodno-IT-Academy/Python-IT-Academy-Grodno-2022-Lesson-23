# Generated by Django 4.0.4 on 2022-05-02 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0004_alter_question_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Urlentry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='date created')),
                ('url_text', models.TextField()),
                ('url_id', models.BigIntegerField()),
                ('url_short', models.CharField(max_length=7)),
                ('snapshot', models.TextField()),
                ('qr_code', models.TextField()),
                ('datetime_available_from', models.DateTimeField(verbose_name='url available from')),
                ('datetime_available_to', models.DateTimeField(verbose_name='url available to')),
                ('partner_ads', models.TextField()),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_date', models.DateTimeField(auto_now=True, verbose_name='date when link was followed')),
                ('follower_info', models.TextField()),
                ('follower_os_info', models.TextField()),
                ('follower_fromwhere', models.TextField()),
                ('urlentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.urlentry')),
            ],
        ),
    ]