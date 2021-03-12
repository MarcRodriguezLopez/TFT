from django.shortcuts import render, HttpResponse
from NBAstatsApp.backend import matchFormat, seasonFormat, standings
from NBAstatsApp.models import BlogPost
from django.views.generic import ListView
# Create your views here.

def matchFull(request, team, day, month, year):
    m = matchFormat.getMatchId(team, day, month, year)
    obj = matchFormat.matchFull(m.id)
    return render(request, 'NBAstatsApp/partido.html', obj)

def positions(request, team):
    obj = standings.rankings(team, [7, 2005], [7, 2006], 'data')
    obj1 = standings.rankings(team, [7, 2006], [7, 2007], 'data')
    obj2 = standings.rankings(team, [7, 2007], [7, 2008], 'data')
    obj3 = standings.rankings(team, [7, 2008], [7, 2009], 'data')
    obj4 = standings.rankings(team, [7, 2009], [7, 2010], 'data')
    obj.update(obj1)
    obj.update(obj2)
    obj.update(obj3)
    obj.update(obj4)
    return render(request, 'NBAstatsApp/historico.html', obj)

def ranking(request, year1, year2):
    obj = standings.getStandings([7, year1], [7, year2], 'data', True)
    return render(request, 'NBAstatsApp/clasificacion.html', obj)

def month(request, team, month, year):
    obj = seasonFormat.getTeamMonthMatches(team, month, year)
    obj['team'] = str(team)
    obj['month'] = str(month)
    obj['year'] = str(year)
    return render(request, 'NBAstatsApp/mes.html', obj)

def year(request, team, year1, year2):
    obj = seasonFormat.getMonthsPerYear(team, year1, year2)
    obj['team'] = str(team)
    obj['year1'] = str(year1)
    obj['year2'] = str(year2)
    return render(request, 'NBAstatsApp/año.html', obj)

def team(request, team):
    obj = {}
    season1 = standings.getTeamStandings(team, [7, 2005], [7, 2006])
    obj['0506_abs'] = season1['dataFavorAbs']
    obj['0506_media'] = season1['dataFavorAvg']
    season2 = standings.getTeamStandings(team, [7, 2006], [7, 2007])
    obj['0607_abs'] = season2['dataFavorAbs']
    obj['0607_media'] = season2['dataFavorAvg']
    season3 = standings.getTeamStandings(team, [7, 2007], [7, 2008])
    obj['0708_abs'] = season3['dataFavorAbs']
    obj['0708_media'] = season3['dataFavorAvg']
    season4 = standings.getTeamStandings(team, [7, 2008], [7, 2009])
    obj['0809_abs'] = season4['dataFavorAbs']
    obj['0809_media'] = season4['dataFavorAvg']
    season5 = standings.getTeamStandings(team, [7, 2009], [7, 2010])
    obj['0910_abs'] = season5['dataFavorAbs']
    obj['0910_media'] = season5['dataFavorAvg']
    obj['team'] = str(team)
    return render(request, 'NBAstatsApp/equipo.html', obj)

def versus(request):
    teams = [0, 1]
    target = 0
    year = 2006
    if request.method == 'POST':
        try:
            teams = [int(numeric_string) for numeric_string in request.POST.getlist('teams')]
            target = int(request.POST['target'])
            year = int(request.POST['season'])
        except:
            teams = [0, 1]
            target = 0
            year = 2006
    obj = standings.getVersusData(teams, target, year)
    labels = ['Puntos', 'TLA', 'TLI', 'TCA', 'TCI', '3PA', 'Asistencias', 'Pérdidas', 'Robos', 'Tapones', 'Rebotes']
    obj['target'] = labels[target]
    seasons = ['2005 - 2006', '2006 - 2007', '2007 - 2008', '2008 - 2009', '2009 - 2010']
    obj['season'] = seasons[year - 2006]
    return render(request, 'NBAstatsApp/grafica.html', obj)

class blog(ListView):
    model = BlogPost

def blogDetail(request, id):
    blog = BlogPost.objects.get(id=id)
    obj = {
        'titulo': blog.title,
        'autor': blog.author,
        'subtitulo': blog.receipt,
        'imagen': blog.image,
        'fecha': blog.date,
        'contenido': blog.content
    }
    return render(request, 'NBAstatsApp/blog.html', obj)