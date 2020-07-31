from django.shortcuts import render

def home(request):
	return render(request, 'ajhsite/home.html')

def about(request):
	return render(request, 'ajhsite/about.html')

def preacherBio(request):
	return render(request, 'ajhsite/preacherBio.html')

def preacherBooks(request):
	return render(request, 'ajhsite/preacherBooks.html')

def professionalProfile(request):
	return render(request, 'ajhsite/professionalProfile.html')

def pitmasterBio(request):
	return render(request, 'ajhsite/pitmasterBio.html')
