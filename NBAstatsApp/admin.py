from django.contrib import admin
from .models import Team, Assist, Match, Point, Steal, Substitution, Rebound, Turnover, Block, Foul, Type, Standing, BlogPost
# Register your models here.
admin.site.register(Team)
admin.site.register(Assist)
admin.site.register(Foul)
admin.site.register(Match)
admin.site.register(Point)
admin.site.register(Steal)
admin.site.register(Substitution)
admin.site.register(Rebound)
admin.site.register(Turnover)
admin.site.register(Block)
admin.site.register(Type)
admin.site.register(Standing)
admin.site.register(BlogPost)