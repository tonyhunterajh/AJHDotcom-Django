from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='site-home'),
	path('about/', views.about, name='site-about'),
	path('preacherBio/', views.preacherBio, name='site-preacherBio'),
	path('preacherBooks/', views.preacherBooks, name='site-preacherBooks'),
	path('professionalProfile/', views.professionalProfile, name='site-professionalProfile'),
	path('pitmasterBio/', views.pitmasterBio, name='site-pitmasterBio'),
]