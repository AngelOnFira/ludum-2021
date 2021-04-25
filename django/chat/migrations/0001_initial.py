# Generated by Django 3.2 on 2021-04-25 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.IntegerField(choices=[(0, 'red'), (1, 'green'), (2, 'blue')], default=0)),
                ('right', models.IntegerField(choices=[(0, 'red'), (1, 'green'), (2, 'blue')], default=0)),
                ('up', models.IntegerField(choices=[(0, 'red'), (1, 'green'), (2, 'blue')], default=0)),
                ('down', models.IntegerField(choices=[(0, 'red'), (1, 'green'), (2, 'blue')], default=0)),
                ('main', models.IntegerField(choices=[(0, 'red'), (1, 'green'), (2, 'blue')], default=0)),
                ('slot', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.player')),
            ],
        ),
    ]
