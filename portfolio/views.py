from django.shortcuts import render, get_object_or_404
from .models import Project
from django.utils.translation import get_language

def project_list(request):
    language_code = get_language()
    projects = Project.objects.all()

    # Inyecta la traducción actual en cada proyecto
    for project in projects:
        translation = project.translations.filter(language=language_code).first()
        project.translation = translation

    return render(request, 'portfolio/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    language_code = get_language()
    translation = project.translations.filter(language=language_code).first()
    project.translation = translation  # Inyecta la traducción para el detalle

    return render(request, 'portfolio/project_detail.html', {'project': project})