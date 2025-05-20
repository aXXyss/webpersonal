from .models import Link

# Creación de un procesador de contexto para enlazar las redes sociales en cada página

def ctx_dict(request):
    ctx = {}
    links = Link.objects.all()
    for link in links:
        ctx[link.key]=link.url
    return ctx