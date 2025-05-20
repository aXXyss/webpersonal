from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from comments.forms import CreateCommentForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from users.models import Profile # Corrección aquí: UserProfile -> Profile
from comments import models
from categories.models import Category

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 5) # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = models.Comment.objects.filter(post=post).order_by('created_at')
    form = CreateCommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


def post_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category, published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category})


def save_comment(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.post = Post.objects.get(id=request.POST.get('post'))
                comment.user = request.user
                # Obtener el perfil del usuario
                try:
                    user_profile = Profile.objects.get(user=request.user)
                    comment.profile = user_profile # Asignar el perfil al comentario
                except Profile.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Perfil no encontrado'}, status=400) # Devolver error si el perfil no existe

                comment.save()

                # Obtener la foto de perfil del usuario
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
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            try:
                reply = form.save(commit=False)
                reply.post = models.Comment.objects.get(id=comment_id).post
                reply.user = request.user
                reply.parent = models.Comment.objects.get(id=comment_id)

                # Obtener el perfil del usuario
                try:
                    user_profile = Profile.objects.get(user=request.user)
                    reply.profile = user_profile # Asignar el perfil a la respuesta
                except Profile.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Perfil no encontrado'}, status=400) # Devolver error si el perfil no existe

                reply.save()

                # Obtener la foto de perfil del usuario
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
                print(f"Error en save_reply: {e}") # Log del error
                return JsonResponse({'success': False, 'error': str(e)}, status=500) # Devuelve el error en JSON
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)