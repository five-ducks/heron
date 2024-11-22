# Generated by Django 5.0.7 on 2024-11-22 07:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_username1', models.CharField(help_text='Reference to the first user participating in the match.', max_length=150, null=True)),
                ('match_username2', models.CharField(help_text='Reference to the second user participating in the match.', max_length=150, null=True)),
                ('match_result', models.CharField(blank=True, choices=[('user1_win', '유저1 승리'), ('user2_win', '유저2 승리'), ('pending_result', '결과 대기중')], default='pending_result', help_text='Result of the match.', max_length=40)),
                ('match_start_time', models.DateTimeField(auto_now_add=True, help_text='Start time of the match.')),
                ('match_end_time', models.DateTimeField(default=django.utils.timezone.now, help_text='End time of the match.')),
                ('username1_grade', models.IntegerField(blank=True, default=0, help_text='Grade of the first user in the match.')),
                ('username2_grade', models.IntegerField(blank=True, default=0, help_text='Grade of the second user in the match.')),
                ('match_type', models.CharField(choices=[('tournament', '토너먼트 경기'), ('onetoone', '1대1경기')], default='onetoone', help_text='Type of match, either tournament or onetoone.', max_length=10)),
            ],
        ),
    ]
