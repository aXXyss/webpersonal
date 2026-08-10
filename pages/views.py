from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from django.utils.translation import get_language

# Create your views here.

def page(request, page_id, page_slug):
    #page= get_object_or_404(Page, id=page_id, link=page_slug)
    page = get_object_or_404(Page, id=page_id)
    language_code = get_language()
    translation = page.translations.filter(language=language_code).first()

    # Determina el slug correcto según el idioma
    expected_slug = page.link if language_code == 'es' else translation.link if translation else page.link

    # Si el slug de la URL no coincide, redirige al correcto
    if page_slug != expected_slug:
        return redirect('page', page_id=page.id, page_slug=expected_slug, permanent=True)

    
    context = {
        'page': page,
        'translation': translation,
    }
    return render(request, 'pages/page_detail.html', context)
