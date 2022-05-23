from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from django.views.generic import ListView

from .forms import CommentForm
from .models import Category, Comment, Post

method_decorator(gzip_page)


class IndexListView(ListView):
    queryset = Post.objects.filter(status="published").order_by("?")
    template_name = "index.html"


def about_me(request):
    return render(request, "categories/about_me.html")


class CategoryList(ListView):
    template_name = "blog/category_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(category=self.category, status="published").order_by(
            "-publication_date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_title"] = self.category.title
        context["category_post_list"] = self.get_queryset()
        context["category_description"] = self.category.description
        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)

    tags = post.tags.values("title", "slug")

    # filter used to select latest posts
    filters = Q(category=post.category) & Q(status="published") & ~Q(slug=post.slug)

    # get 5 latest post
    recent_posts = Post.objects.filter(filters).order_by("-publication_date")

    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comments_count": comments.count(),
        "comment_form": comment_form,
        "latest": recent_posts,
        "tags": tags,
    }

    return render(request, "article.html", context)


def error_404(request, exception):
    return render(request, "404.html")
