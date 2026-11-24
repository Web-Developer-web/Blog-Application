# myblog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Category, Post


def post_list(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    status_filter = request.GET.get("status", "").strip()

    if request.user.is_authenticated:
        posts = Post.objects.select_related("author", "category")
        if status_filter in (Post.Status.DRAFT, Post.Status.PUBLISHED):
            posts = posts.filter(status=status_filter)
    else:
        posts = Post.objects.select_related("author", "category").filter(
            status=Post.Status.PUBLISHED
        )

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__icontains=query)
        )

    featured_posts = (
        Post.objects.select_related("author", "category")
        .filter(status=Post.Status.PUBLISHED, is_featured=True)[:3]
    )
    categories = Category.objects.all()

    context = {
        "posts": posts,
        "featured_posts": featured_posts,
        "categories": categories,
        "query": query,
        "active_category": category_slug,
        "active_status": status_filter,
    }
    return render(request, "myblog/post_list.html", context)


def post_detail(request, slug):
    queryset = Post.objects.select_related("author", "category")
    if not request.user.is_authenticated:
        queryset = queryset.filter(status=Post.Status.PUBLISHED)

    post = get_object_or_404(queryset, slug=slug)

    # Increment views safely without race conditions
    Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
    post.refresh_from_db(fields=["views_count"])

    tag_list = [t.strip() for t in post.tags.split(",") if t.strip()] if post.tags else []

    return render(request, "myblog/post_detail.html", {
        "post": post,
        "tag_list": tag_list,
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Post "{post.title}" created successfully.')
            return redirect("myblog:post_detail", slug=post.slug)
    else:
        form = PostForm()

    return render(request, "myblog/post_form.html", {
        "form": form,
        "page_title": "Create New Post",
        "submit_label": "Publish / Save Post",
    })


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect("myblog:post_detail", slug=post.slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save()
            messages.success(request, f'Post "{updated_post.title}" updated.')
            return redirect("myblog:post_detail", slug=updated_post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "myblog/post_form.html", {
        "form": form,
        "post": post,
        "page_title": f"Edit: {post.title}",
        "submit_label": "Save Changes",
    })


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect("myblog:post_detail", slug=post.slug)

    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f'Post "{title}" deleted.')
        return redirect("myblog:post_list")

    return render(request, "myblog/post_confirm_delete.html", {"post": post})