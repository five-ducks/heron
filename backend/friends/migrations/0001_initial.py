# Generated by Django 4.2.14 on 2024-08-19 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', '대기상태'), ('accepted', '친구상태')], default='pending', max_length=10)),
                ('user1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends_initiated', to='users.user')),
                ('user2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends_received', to='users.user')),
            ],
        ),
    ]
