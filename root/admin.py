from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(faculty)
admin.site.register(Session)
admin.site.register(Semester)
admin.site.register(External)
admin.site.register(SemesterBill)
admin.site.register(Course)
admin.site.register(courseBill)
admin.site.register(ThesisPaper)
admin.site.register(ThesisSupervisor)
