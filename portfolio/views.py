from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectTranslation
from django.utils.translation import get_language

def project_list(request):
    language_code = get_language()
    projects = Project.objects.all()

    for project in projects:
        translation = project.translations.filter(language=language_code).first()
        project.translation = translation

    return render(request, 'portfolio/project_list.html', {'projects': projects})

def project_detail(request, slug):
    language_code = get_language()

    translation = ProjectTranslation.objects.filter(
        slug=slug, language=language_code
    ).select_related('project').first()

    if translation:
        project = translation.project
        project.translation = translation
    else:
        project = get_object_or_404(Project, slug=slug)
        project.translation = project.translations.filter(language=language_code).first()

    # Slugs por idioma para el selector
    language_slugs = {'es': project.slug}
    for t in project.translations.all():
        if t.slug:
            language_slugs[t.language.lower()] = t.slug

    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'language_slugs': language_slugs,
    })