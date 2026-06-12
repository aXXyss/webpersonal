from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
        # Buscar si el slug pertenece a OTRO idioma o al slug base
        other_translation = ProjectTranslation.objects.filter(
            slug=slug
        ).select_related('project').first()

        if other_translation:
            project = other_translation.project
        else:
            project = get_object_or_404(Project, slug=slug)

        # Buscar el slug correcto para el idioma activo
        correct_translation = project.translations.filter(language=language_code).first()
        if correct_translation and correct_translation.slug:
            correct_url = reverse('portfolio:project_detail', kwargs={'slug': correct_translation.slug})
            return redirect(correct_url, permanent=True)
        
        # Si no hay traducción para este idioma, usar el slug base
        project.translation = None

    # Slugs por idioma para el selector
    language_slugs = {'es': project.slug}
    for t in project.translations.all():
        if t.slug:
            language_slugs[t.language.lower()] = t.slug

    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'language_slugs': language_slugs,
    })