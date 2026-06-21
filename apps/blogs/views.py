from django.views.generic import ListView, DetailView
from django.db.models import Q
from apps.blogs.models import BlogPost, BlogCategory, BlogTag

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogs/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='PUBLISHED')
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        search_query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['tags'] = BlogTag.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('q')
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPost.objects.filter(status='PUBLISHED')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Find related posts in the same category, excluding the current one
        context['related_posts'] = BlogPost.objects.filter(
            category=post.category,
            status='PUBLISHED'
        ).exclude(pk=post.pk)[:3]
        return context
