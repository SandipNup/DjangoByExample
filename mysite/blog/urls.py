from django.urls import path,re_path
from . import views
from .feeds import LatestPostFeed





app_name='blog'
urlpatterns = [
    #urls for the template pages
    #post views
    path('', views.post_list, name='post_list'), #url for post_list view
    # path('',views.PostListView.as_view(),name='post_list'), #urls for PostListView class based view
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),#url for post list view without slug
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),#to call the post list view with tag
    re_path(r'^(?P<post_id>\d+)/share/$',views.post_share,name='post_share'),
    path('feed',LatestPostFeed(),name='post_feed'),
    
]