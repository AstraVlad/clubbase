from django.db import models

GENDERS = ('Male', 'Female', 'Mixed Male Female')

# Create your models here.


class Clubs(models.Model):
    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'

    long_name = models.CharField(max_length=200, blank=False, null=False,)
    short_name = models.CharField(max_length=50, blank=False, null=False,)
    city = models.CharField(max_length=30, blank=False, null=False,)
    emblem = models.ImageField(upload_to='images')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}, {self.city}'


class Fighters(models.Model):
    class Meta:
        verbose_name = 'Боец'
        verbose_name_plural = 'Бойцы'
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Фамилия')
    # TODO: Добавить историю клубов
    city = models.CharField(max_length=30, blank=False, null=False)
    current_club = models.ForeignKey(Clubs, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Клуб')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    GENDER_CHOICES = [
        (GENDERS[0], 'Мужской'),
        (GENDERS[1], 'Женский'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Tournaments(models.Model):
    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
    name = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=30, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False, default=start_date)
    description = models.TextField(blank=True, null=True)
    rules_text = models.TextField(blank=True, null=True)
    rules_file = models.FileField(blank=True, null=True, upload_to='docs')
    rules_json = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}, {str(self.start_date.year)}'


class Weapons(models.Model):
    class Meta:
        verbose_name = 'Класс оружия'
        verbose_name_plural = 'Классы оружия'
    weapons_id = models.CharField(max_length=20, primary_key=True, unique=True)
    weapons_name = models.CharField(max_length=100, blank=False, null=False)
    deprecated = models.BooleanField(default=False, blank=False, null=False)


class Divisions(models.Model):
    class Meta:
        verbose_name = 'Эшелон'
        verbose_name_plural = 'Эшелоны'
    division_id = models.CharField(max_length=20, primary_key=True, unique=True)
    division_name = models.CharField(max_length=100, blank=False, null=False)
    deprecated = models.BooleanField(default=False, blank=False, null=False)


class TournamentNominations(models.Model):
    class Meta:
        verbose_name = 'Турнирная номинация'
        verbose_name_plural = 'Турнирные номинации'
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    division = models.ForeignKey(Divisions, on_delete=models.RESTRICT)
    weapon = models.ForeignKey(Weapons, on_delete=models.RESTRICT)
    GENDER_CHOICES = [
        (GENDERS[0], 'Мужчины'),
        (GENDERS[1], 'Женщины'),
        (GENDERS[2], 'Смешанная'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)


class TournamentParticipation(models.Model):
    fighter = models.ForeignKey(Fighters, on_delete=models.CASCADE, blank=False, null=False)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, blank=False, null=False)
    nomination = models.ForeignKey(TournamentNominations, on_delete=models.CASCADE, blank=False, null=False)
    got_a_place = models.IntegerField(default=0, blank=False, null=False)
    was_disqualified = models.BooleanField(default=False, null=False, blank=False)

    def was_a_winner(self):
        if self.got_a_place == 1:
            return True
        else:
            return False


class TournamentFights(models.Model):
    class Meta:
        verbose_name = 'Бой'
        verbose_name_plural = 'Бои'
    tournament = models.ForeignKey(Tournaments, blank=False, null=False, on_delete=models.CASCADE)
    nomination = models.ForeignKey(TournamentNominations, blank=False, null=False, on_delete=models.CASCADE)
    tournament_stage = models.CharField(max_length=100)
    tournament_stage_round = models.IntegerField(default=0)
    ring_no = models.IntegerField(default=0)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    fighter_1 = models.ForeignKey(Fighters, blank=False, null=False,
                                  on_delete=models.RESTRICT, related_name='fighter_1')
    fighter_2 = models.ForeignKey(Fighters, blank=False, null=False,
                                  on_delete=models.RESTRICT, related_name='fighter_2')
    fighter_1_result = models.IntegerField()
    fighter_2_result = models.IntegerField()
    RESULTS_CHOICES = [
        (0, 'Ничья'),
        (1, 'Победил боец номер 1'),
        (2, 'Победил боец номер 2'),
    ]
    result = models.IntegerField(null=False, blank=False, choices=RESULTS_CHOICES)


class FightLog(models.Model):
    the_fight = models.ForeignKey(TournamentFights, blank=False, null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=False, null=False)
    fighter_1_score_change = models.IntegerField()
    fighter_2_score_change = models.IntegerField()
    fighter_1_other_effect = models.CharField(max_length=30)
    fighter_2_other_effect = models.CharField(max_length=30)

