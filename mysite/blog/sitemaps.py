from django.contrib.sitemaps import Sitemap #we create the custome sitemap by inheriting the Sitemap class from the sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq='weekly'
    priority=0.9

    def items(self):
        return Post.published.all()

    def lastmod(self,obj): #this function takes each object of the item function 
        return obj.publish