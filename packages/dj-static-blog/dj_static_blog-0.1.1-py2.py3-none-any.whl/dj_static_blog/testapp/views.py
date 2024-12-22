from django.views.generic import ListView, DetailView
from dj_static_blog.models import StaticBlogPost

class PostListView(ListView):
    model = StaticBlogPost
    template_name = 'dj_static_blog/post_list.html'
    paginate_by = 2
    
class PostDetailView(DetailView):
    model = StaticBlogPost
    template_name = 'dj_static_blog/post_detail.html'