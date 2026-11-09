import datetime as dt

from django.shortcuts import get_object_or_404, render


from blog.models import Post, Category


# Create your views here.
def index(request):
    template_name = 'blog/index.html'
    post_list = (
        Post.objects.select_related('location', 'category', 'author')
        .filter(
            is_published=True,
            pub_date__lte=dt.date.today(),
            category__is_published=True,
        )
        .order_by('pub_date', 'title')[0:5]
    )
    return render(request, template_name, {'post_list': post_list})


def post_detail(request, id):
    template_name = 'blog/detail.html'
    querySet = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(pk=id)
    post = get_object_or_404(
        querySet,
        pub_date__lte=dt.date.today(),
        is_published=True,
        category__is_published=True,
    )
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        category__slug=category_slug,
        category__is_published=True,
        is_published=True,
        pub_date__lte=dt.date.today(),
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, template_name, context)
