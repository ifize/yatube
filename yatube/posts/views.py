from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User

POST_NUMBER = 10


def page_maker(request, posts):
    paginator = Paginator(posts, POST_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    context = {
        'page_obj': page_maker(request, posts),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().filter(group=group).order_by('-pub_date')
    context = {
        'group': group,
        'page_obj': page_maker(request, posts),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.all().filter(author=user).order_by('-pub_date')
    if request.user != user:
        self_profile = False
        if request.user.is_authenticated:
            auth = User.objects.filter(following__user=request.user)
            if user in auth:
                following = True
            else:
                following = False
        else:
            following = False
    else:
        self_profile = True
        following = None
    context = {
        'posts': posts,
        'username': user,
        'page_obj': page_maker(request, posts),
        'following': following,
        'self_profile': self_profile
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post.objects.select_related('author'), pk=post_id)
    posts_author = post.author.posts.all()
    posts_counter = posts_author.count()
    comments = Comment.objects.all().order_by('-created')
    context = {
        'post': post,
        'posts_counter': posts_counter,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = user
            post = Post.objects.create(
                text=text,
                group=group,
                author=author,
            )
            post.save()
            return redirect('posts:profile', user.username)

        return render(request, template, {'form': form, 'is_edit': False})

    form = PostForm()
    return render(request, template, {'form': form, 'is_edit': False})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    context = {
        'page_obj': page_maker(request, posts),
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)
    if (
        request.user != user
    ) & (
            Follow.objects.filter(user=request.user, author=user).count() < 1
    ):
        Follow.objects.create(
            user=request.user,
            author=user
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=user).delete()
    return redirect('posts:profile', username=username)
