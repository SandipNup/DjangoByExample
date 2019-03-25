from django.db import models  #each model subclasses django.db.models.Model
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

from taggit.managers import TaggableManager



#creating the manager object fro the post model
'''Post.objects.all().here objects is the default manager of every models that retrive objects in the database.However 
    we can also define custome object manager
'''
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()

   



# Create your models here.

class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date='publish')  #This is a field intended to be used in URLs. We have added the unique_for_date parameter to this field so that we can build URLs for posts using their publish date and slug. Django will prevent multiple posts from having the same slug for a given date.
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts') #It defines a many-to-one relationship. We are telling Django that each post is written by a user, and a user can write any number of posts. The on_delete parameter specifies the behavior to adopt when the referenced object is deleted.We specify the name of the reverse relationship, from User to Post, with the related_name attribute.
    body = models.TextField()
    publish=models.DateTimeField(default=timezone.now)#This datetime indicates when the post was published. We use Django's timezone now method as the default value.
    created=models.DateTimeField(auto_now_add=True)#suto_now_add=True will save date automatically while creating the object
    updated=models.DateTimeField(auto_now=True)#This datetime indicates the last time the post was updated. Since we are using auto_now here, the date will be updated automatically when saving an object.
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')# We use a choices parameter, so the value of this field can only be set to one of the given choices.
    objects=models.Manager()#the default manager
    published=PublishedManager()#our custome manager
    tags=TaggableManager() #taggable manager for creating tags for the post

    class Meta:
        ordering=('-publish',) #reverse odering of object on publish date
    
    def __str__(self): #human readable presentation of the object.
        return self.title

    #We will use the get_absolute_url() method in our templates to link to specific posts.
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


'''Creating the model for comment in the Post'''
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE) #ForeginKey to associate the comment with the single Post
    name=models.CharField(max_length=50) #
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)  #we use the active boolean field that we will use to manually deactivate inapproriate comments

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)



   



