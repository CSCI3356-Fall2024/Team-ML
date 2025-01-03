# Generated by Django 5.1.2 on 2024-11-25 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='redeemed_rewards',
            field=models.ManyToManyField(blank=True, related_name='users', to='main.reward'),
        ),
        migrations.CreateModel(
            name='RewardRedeemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redeemed_at', models.DateTimeField(auto_now_add=True)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
            options={
                'unique_together': {('user', 'reward')},
            },
        ),
    ]
