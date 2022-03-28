from django.contrib import admin

from .models import ZoomAccount, ZoomMeeting
# Register your models here.


class ZoomAccountAdmin(admin.ModelAdmin):
    fields = ['name','description','create_date','available','appkey','secretkey','useremail']
    list_display = ['name', 'available', 'create_date']

class ZoomMeetingAdmin(admin.ModelAdmin):
    fields = ['topic','description','type_meeting','create_dt','start_dt','duration','password','join_url','account','user', 'settings']
    list_display = ['topic', 'start_dt', 'create_dt','duration']

admin.site.register(ZoomAccount, ZoomAccountAdmin)
admin.site.register(ZoomMeeting, ZoomMeetingAdmin)