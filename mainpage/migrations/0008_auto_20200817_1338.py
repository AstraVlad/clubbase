# Generated by Django 3.1 on 2020-08-17 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0007_tournaments_rules_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fighters',
            name='current_club',
        ),
        migrations.RemoveField(
            model_name='fightlog',
            name='the_fight',
        ),
        migrations.RemoveField(
            model_name='tournamentfights',
            name='fighter_1',
        ),
        migrations.RemoveField(
            model_name='tournamentfights',
            name='fighter_2',
        ),
        migrations.RemoveField(
            model_name='tournamentfights',
            name='nomination',
        ),
        migrations.RemoveField(
            model_name='tournamentfights',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='tournamentnominations',
            name='division',
        ),
        migrations.RemoveField(
            model_name='tournamentnominations',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='tournamentnominations',
            name='weapon',
        ),
        migrations.RemoveField(
            model_name='tournamentparticipation',
            name='fighter',
        ),
        migrations.RemoveField(
            model_name='tournamentparticipation',
            name='nomination',
        ),
        migrations.RemoveField(
            model_name='tournamentparticipation',
            name='tournament',
        ),
        migrations.DeleteModel(
            name='Divisions',
        ),
        migrations.DeleteModel(
            name='Fighters',
        ),
        migrations.DeleteModel(
            name='FightLog',
        ),
        migrations.DeleteModel(
            name='TournamentFights',
        ),
        migrations.DeleteModel(
            name='TournamentNominations',
        ),
        migrations.DeleteModel(
            name='TournamentParticipation',
        ),
        migrations.DeleteModel(
            name='Tournaments',
        ),
        migrations.DeleteModel(
            name='Weapons',
        ),
    ]
