# Generated by Django 3.1 on 2020-08-17 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0008_auto_20200817_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Divisions',
            fields=[
                ('division_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('division_name', models.CharField(max_length=100)),
                ('deprecated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Fighters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Мужской'), ('Female', 'Женский')], max_length=20)),
                ('current_club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainpage.clubs')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentNominations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Мужчины'), ('Female', 'Женщины'), ('Mixed Male Female', 'Смешанная')], max_length=20)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainpage.divisions')),
            ],
        ),
        migrations.CreateModel(
            name='Tournaments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(default=models.DateField())),
                ('description', models.TextField(blank=True, null=True)),
                ('rules_text', models.TextField(blank=True, null=True)),
                ('rules_file', models.FileField(blank=True, null=True, upload_to='docs')),
                ('rules_json', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weapons',
            fields=[
                ('weapons_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('weapons_name', models.CharField(max_length=100)),
                ('deprecated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('got_a_place', models.IntegerField(default=0)),
                ('was_disqualified', models.BooleanField(default=False)),
                ('fighter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.fighters')),
                ('nomination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournamentnominations')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournaments')),
            ],
        ),
        migrations.AddField(
            model_name='tournamentnominations',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournaments'),
        ),
        migrations.AddField(
            model_name='tournamentnominations',
            name='weapon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainpage.weapons'),
        ),
        migrations.CreateModel(
            name='TournamentFights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_stage', models.CharField(max_length=100)),
                ('tournament_stage_round', models.IntegerField(default=0)),
                ('ring_no', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('fighter_1_result', models.IntegerField()),
                ('fighter_2_result', models.IntegerField()),
                ('result', models.IntegerField(choices=[(0, 'Ничья'), (1, 'Победил боец номер 1'), (2, 'Победил боец номер 2')])),
                ('fighter_1', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fighter_1', to='mainpage.fighters')),
                ('fighter_2', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fighter_2', to='mainpage.fighters')),
                ('nomination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournamentnominations')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournaments')),
            ],
        ),
        migrations.CreateModel(
            name='FightLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('fighter_1_score_change', models.IntegerField()),
                ('fighter_2_score_change', models.IntegerField()),
                ('fighter_1_other_effect', models.CharField(max_length=30)),
                ('fighter_2_other_effect', models.CharField(max_length=30)),
                ('the_fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.tournamentfights')),
            ],
        ),
    ]
