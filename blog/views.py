from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category, Comment

@login_required(login_url='/login/')
def blog_list(request):
    search = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    posts = Post.objects.filter(status='published').select_related('author', 'category')

    if search:
        posts = posts.filter(title__icontains=search)

    if category_filter:
        posts = posts.filter(category__id=category_filter)

    posts = posts.order_by('-created_at')
    categories = Category.objects.all()

    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'search': search,
        'category_filter': category_filter,
    })

@login_required(login_url='/login/')
def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )
            messages.success(request, 'Comment added!')
            return redirect(f'/blog/{pk}/')

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'comments': comments,
    })

@login_required(login_url='/login/')
def blog_create(request):
    if not request.user.is_staff:  # ← Admin check
        messages.error(request, 'Only admin can create posts!')
        return redirect('/blog/')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST.get('category', '')
        status = request.POST.get('status', 'draft')

        category = None
        if category_id:
            try:
                category = Category.objects.get(pk=int(category_id))
            except (Category.DoesNotExist, ValueError):
                category = None

        Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category,
            status=status,
        )
        messages.success(request, 'Post created!')
        return redirect('/blog/')

    categories = Category.objects.all()
    return render(request, 'blog/blog_create.html', {'categories': categories})

@login_required(login_url='/login/')
def blog_edit(request, pk):
    if not request.user.is_staff:  # ← Admin check
        messages.error(request, 'Only admin can edit posts!')
        return redirect('/blog/')

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        category_id = request.POST.get('category', '')
        post.status = request.POST.get('status', 'draft')

        if category_id:
            try:
                post.category = Category.objects.get(pk=int(category_id))
            except (Category.DoesNotExist, ValueError):
                post.category = None
        else:
            post.category = None

        post.save()
        messages.success(request, 'Post updated!')
        return redirect('/blog/')

    categories = Category.objects.all()
    return render(request, 'blog/blog_edit.html', {
        'post': post,
        'categories': categories,
    })

@login_required(login_url='/login/')
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect('/blog/')

@login_required(login_url='/login/')
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_id = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment deleted!')
    return redirect(f'/blog/{post_id}/')