from django.contrib import admin
from .models import CardDump, Country, CardCvv, CardMarket, Checkpoint, CrawlerAccess, FilePath, Crawler_Breaker, Email_passwords

# Register your models here.

class Email_passwordsAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'password', 'source']

admin.site.register(CardDump)
admin.site.register(CardCvv)
admin.site.register(Country)
admin.site.register(CardMarket)
admin.site.register(Checkpoint)
admin.site.register(Email_passwords, Email_passwordsAdmin)
admin.site.register(CrawlerAccess)
admin.site.register(FilePath)
admin.site.register(Crawler_Breaker)



