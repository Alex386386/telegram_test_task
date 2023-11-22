from django.contrib import admin

from .models import Message, BotText, CurrencyRate


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'text')
    list_filter = ('user',)


class BotTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('code', 'rate')


admin.site.register(Message, MessageAdmin)
admin.site.register(BotText, BotTextAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
