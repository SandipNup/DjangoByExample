from django import template
from django.db.models import Count

register=template.Library() #each template tags need to contain the variable called register to be a valid tag library

from ..models import Post

"""we are defining a tag called
total_posts with a Python function and using @register.simple_tag to define
the function as a simple tag and register it."""
@register.simple_tag
def total_posts():   #django will use the function name as the tag name if you want to use the seprate tagname you can use @register.simple_tag(name="my_tags")
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_post.html') #registered template tag with inclusion tag and we specify the template where the values has to be rendered
def show_latest_posts(count=5): #inclusion tags returns the dictionary of the value
    latest_post=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_post}


"""Now we will create an assignment tag to display the most commented post"""

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]



"""Custome djnago filters"""
from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

    
