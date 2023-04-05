
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/login/', views.log, name="log"),
    path('log/', views.log, name="log"),
    path('logOut/', views.logOut, name="logOut"),
    path('committee/', views.committee, name="committee"),
    path('createCom/', views.createCom, name="createCom"),
    path('viewCom/<int:id>/', views.viewCom, name="viewCom"),
    path('viewSem/<int:id>/<int:id2>/', views.viewSem, name="viewSem"),
    path('thesis/<int:id>/<int:id2>/<int:id3>/', views.thesis, name="thesis"),
    path('supervising/<int:id>/<int:id2>/<int:id3>/', views.supervising, name="supervising"),     
    path('pdf_view/<int:id>/<int:id2>/<int:id3>/', views.pdf_view, name="pdf_view"),
    path('addRole/<int:id>/<int:id2>/', views.addRole, name="addRole"),
    path('createSem/<int:id>/', views.createSem, name="createSem"),
    path('createCourse/<int:id>/<int:id2>/',
         views.createCourse, name='createCourse'),
    path('viewCourse/<int:id>/<int:id2>/', views.viewCourse, name='viewCourse'),
    path('updateCourse/<int:id>/<int:id2>/<int:id3>/',
         views.updateCourse, name='updateCourse'),
    path('deleteCourse/<int:id>/<int:id2>/<int:id3>/',
         views.deleteCourse, name='deleteCourse'),
    path('addInvigilator/<int:id>/<int:id2>/<int:id3>/',
         views.addInvigilator, name='addInvigilator'),
    path('indCourse/<int:id>/<int:id2>/<int:id3>/',
         views.indCourse, name='indCourse'),
    path('examBill/', views.examBill, name='examBill'),
    path('indBill/<int:id>/<int:id2>/<int:id3>/', views.indBill, name='indBill'),
    path('examBill2/', views.examBill2, name='examBill'),
    path('semBill/<int:id>/<int:id2>/', views.semBill, name='semBill'),
    path('indBill2/<int:id>/<int:id2>/<int:id3>/',
         views.indBill2, name='indBill2'),







]
