from django.contrib import admin
from .tasks import strategy_1
from .models import Stock,Strategy
# Register your models here.
admin.site.register(Stock)


def run_my_task(modeladmin, request, queryset):
    print(queryset,"ASDFGHJGFDFGHJHFVGHJHGHJKN")
    for obj in queryset:
        eval(obj.name).delay()
    modeladmin.message_user(request, "Task successfully queued.")

run_my_task.short_description = "Run my Strategy"

@admin.register(Strategy)
class MyModelAdmin(admin.ModelAdmin):
    actions = [run_my_task]