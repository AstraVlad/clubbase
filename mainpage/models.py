from django.db import models


# Create your models here.

class Club(models.Model):
    long_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    emblem = models.ImageField()

    def __str__(self):
        return f'{self.short_name}, {self.city}'


class Fighter(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.name}, {str(self.start_date.year)}'


class TournamentParticipation(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    was_a_winner = models.BooleanField()
    got_a_place = models.IntegerField()
