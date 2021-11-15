from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from .models import Post
from .models import Category
from .models import Comment


class IndexListView(ListView):
    queryset = Post.objects.filter(
        status='published').order_by('?')
    template_name = 'index.html'


def about_me(request):
    return render(request, 'categories/about_me.html')

class CategoryList(ListView):
    template_name = 'blog/category_list.html'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
        category=self.category, status='published').order_by('-publication_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_title"] = self.category.title
        context['category_post_list'] = self.get_queryset()
        context["category_description"] = self.category.description
        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)

    # get 5 latest post
    recent_post = Post.objects.filter(category = post.category).order_by('-publication_date')[:5]
    latest = []

    for r_post in recent_post:
        if r_post.slug == post.slug:
            continue
        
        latest.append(
            {
                "title": r_post.title,
                'slug': r_post.slug
            }
        )

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    comment_form = CommentForm()
    context = {'post': post, 'comments': comments,
               "comment_form": comment_form, "latest": latest}

    return render(request, 'article.html', context)


def error_404(request, exception):
    return render(request, "404.html")
