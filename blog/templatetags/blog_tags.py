from django import template
from ..models import Post

# Identify this module as one containing template tags.
register = template.Library()

# Get the total number of posts in the blog.
@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/recent_posts.html')
def show_recent_posts(count=5):
    recent_posts = Post.objects.order_by('-date_posted')[:count]
    return {'recent_posts': recent_posts}
