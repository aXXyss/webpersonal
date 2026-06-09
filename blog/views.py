from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from comments.forms import CreateCommentForm
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import get_language
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from users.models import Profile
from comments import models
from categories.models import Category

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    current_lang = get_language()
    
    post = None
    try:
        # Slug correcto para el idioma activo
        post = Post.objects.get(**{f'slug_{current_lang}': slug})
    except Post.DoesNotExist:
        # Buscar en otros idiomas y redirigir a la URL correcta (301)
        for lang in ['es', 'en', 'fr']:
            try:
                post = Post.objects.get(**{f'slug_{lang}': slug})
                # Encontrado en otro idioma — redirigir al slug correcto del idioma activo
                correct_slug = getattr(post, f'slug_{current_lang}')
                correct_url = reverse('blog:post_detail', kwargs={'slug': correct_slug})
                return redirect(correct_url, permanent=True)
            except Post.DoesNotExist:
                continue
        raise Http404("Post no encontrado")
    
    comments = models.Comment.objects.filter(post=post).order_by('created_at')
    form = CreateCommentForm()
    share_url = request.build_absolute_uri()

    translated_slugs = {
        'es': post.slug_es,
        'en': post.slug_en,
        'fr': post.slug_fr,
    }

    return render(request, 'blog/post_detail.html', {
        'post': post, 
        'comments': comments, 
        'form': form, 
        'share_url': share_url,
        'translated_slugs': translated_slugs,
    })


def post_list_by_category(request, slug):
    current_lang = get_language()
    
    category = None
    try:
        category = Category.objects.get(**{f'slug_{current_lang}': slug})
    except Category.DoesNotExist:
        # Buscar en otros idiomas y redirigir a la URL correcta (301)
        for lang in ['es', 'en', 'fr']:
            try:
                category = Category.objects.get(**{f'slug_{lang}': slug})
                # Encontrado en otro idioma — redirigir al slug correcto del idioma activo
                correct_slug = getattr(category, f'slug_{current_lang}')
                correct_url = reverse('blog:post_list_by_category', kwargs={'slug': correct_slug})
                return redirect(correct_url, permanent=True)
            except Category.DoesNotExist:
                continue
        raise Http404("Categoría no encontrada")
    
    posts = Post.objects.filter(categories=category, published_date__lte=timezone.now()).order_by('-published_date')
    
    translated_category_slugs = {
        'es': category.slug_es,
        'en': category.slug_en,
        'fr': category.slug_fr,
    }
    
    return render(request, 'blog/post_list.html', {
        'posts': posts, 
        'category': category,
        'translated_category_slugs': translated_category_slugs,
    })


def save_comment(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.post = Post.objects.get(id=request.POST.get('post'))
                comment.user = request.user
                try:
                    user_profile = Profile.objects.get(user=request.user)
                    comment.profile = user_profile
                except Profile.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Perfil no encontrado'}, status=400)

                comment.save()

                # Enviar email de notificación
                try:
                    post_url = request.build_absolute_uri(comment.post.get_absolute_url())
                    subject = f'Nuevo comentario en: {comment.post.title}'
                    message = f"""
Nuevo comentario en tu blog:

Post: {comment.post.title}
Autor: {comment.user.username} ({comment.user.email})
Fecha: {comment.created_at.strftime("%d/%m/%Y %H:%M")}

Comentario:
{comment.comment}

Ver post: {post_url}
                    """
                    
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                except Exception as email_error:
                    print(f"Error enviando email: {email_error}")

                try:
                    user_profile_photo = user_profile.photo.url if user_profile.photo else '/media/blog/avatars/noavatar.png'
                except Profile.DoesNotExist:
                    user_profile_photo = '/media/blog/avatars/noavatar.png'

                comment_data = {
                    'id': comment.id,
                    'username': comment.user.username,
                    'created_at': comment.created_at.strftime("%d %b %Y %H:%M"),
                    'comment_content': comment.comment,
                    'user_profile_photo_html': f'<img class="d-flex mr-3 rounded-circle" width="50px" height="50px" src="{user_profile_photo}" alt="">'
                }
                return JsonResponse({'success': True, 'comment_data': comment_data})
            except Exception as e:
                print(f"Error en save_comment: {e}")
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def save_reply(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Debes estar conectado para responder'}, status=401)
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            try:
                reply = form.save(commit=False)
                parent_comment = models.Comment.objects.get(id=comment_id)
                reply.post = parent_comment.post
                reply.user = request.user
                reply.parent = parent_comment

                try:
                    user_profile = Profile.objects.get(user=request.user)
                    reply.profile = user_profile
                except Profile.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Perfil no encontrado'}, status=400)

                reply.save()

                # Notificar al autor del comentario padre (si tiene email y no es el mismo usuario)
                if parent_comment.user.email and parent_comment.user != request.user:
                    try:
                        post_url = request.build_absolute_uri(reply.post.get_absolute_url())
                        send_mail(
                            subject=f'Alguien ha respondido a tu comentario en aXXyss',
                            message=f"""Hola {parent_comment.user.username},

                {reply.user.username} ha respondido a tu comentario en el post "{reply.post.title}":

                Tu comentario:
                {parent_comment.comment}

                Respuesta de {reply.user.username}:
                {reply.comment}

                Ver la conversación: {post_url}

                Un saludo,
                aXXyss Soluciones
                https://axxyss.com
                """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[parent_comment.user.email],
                            fail_silently=True,
                        )
                    except Exception as e:
                        print(f"Error enviando notificación al usuario: {e}")

                # Enviar email de notificación
                try:
                    post_url = request.build_absolute_uri(reply.post.get_absolute_url())
                    subject = f'Nueva respuesta en: {reply.post.title}'
                    message = f"""
Nueva respuesta a un comentario en tu blog:

Post: {reply.post.title}
Respondiendo a: {parent_comment.user.username}
Autor de la respuesta: {reply.user.username} ({reply.user.email})
Fecha: {reply.created_at.strftime("%d/%m/%Y %H:%M")}

Comentario original:
{parent_comment.comment}

Respuesta:
{reply.comment}

Ver post: {post_url}
                    """
                    
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                except Exception as email_error:
                    print(f"Error enviando email: {email_error}")

                try:
                    user_profile_photo = user_profile.photo.url if user_profile.photo else '/media/blog/avatars/noavatar.png'
                except Profile.DoesNotExist:
                    user_profile_photo = '/media/blog/avatars/noavatar.png'

                comment_data = {
                    'id': reply.id,
                    'username': reply.user.username,
                    'created_at': reply.created_at.strftime("%d %b %Y %H:%M"),
                    'comment_content': reply.comment,
                    'user_profile_photo_html': f'<img class="d-flex mr-3 rounded-circle" width="50px" height="50px" src="{user_profile_photo}" alt="">',
                    'parent_id': comment_id,
                }

                return JsonResponse({'success': True, 'comment_data': comment_data})
            except Exception as e:
                print(f"Error en save_reply: {e}")
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
