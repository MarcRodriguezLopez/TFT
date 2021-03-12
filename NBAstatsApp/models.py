from django.db import models

# Create your models here.
class Team(models.Model):
    team = models.CharField(max_length=5)
    id = models.IntegerField(primary_key=True)

    class Meta:
        ordering = ('team',)

    def __str__(self):
        return self.team

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    ot = models.IntegerField()
    data = models.JSONField(default={})
    #dict = 'Points', 'FTM', 'FTA', 'FGM','FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds'

    def __str__(self):
        return "Match " + str(self.id)


class Assist(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team
    #dict = points generated

    def __str__(self):
        return str(self.code) + " assists"


class Foul(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team
    #dict = foul type

    def __str__(self):
        return str(self.code) + " fouls"


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team
    #dict = shot type
    #dict = value, si es 0 vemos que ha fallado el tiro por lo que eliminamos el campo miss or made

    def __str__(self):
        return str(self.code) + " points"


class Steal(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team

    def __str__(self):
        return str(self.code) + " steals"



class Block(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team

    def __str__(self):
        return str(self.code) + " blocks"



class Rebound(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team

    def __str__(self):
        return str(self.code) + " rebounds"



class Substitution(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team
    #dict = number

    def __str__(self):
        return str(self.code) + " substitutions"



class Turnover(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(Match, on_delete= models.CASCADE)
    data = models.JSONField(default={})
    #dict = time
    #dict = team
    #dict = turnover type

    def __str__(self):
        return str(self.code) + " turnovers"


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=200)
    code = models.IntegerField()
    clase = models.CharField(max_length=200)

    def __str__(self):
        return str(self.code) + " " + str(self.clase)

class Standing(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    part = models.CharField(max_length=200)
    num_matches = models.IntegerField()
    data = models.JSONField(default={})

    def __str__(self):
        return 'Standings ' + str(self.team) + ' ' + str(self.part) + ': ' + str(self.month) + '/' + str(self.year)

class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    receipt = models.TextField()
    author = models.CharField(max_length=50)
    content = models.TextField()
    image = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title