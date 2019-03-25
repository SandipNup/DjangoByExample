from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.views.generic import ListView
from django.core.mail import send_mail

# Create your views here.

#Creating a post list view 
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag

from django.db.models import Count

'''Cretaing the post list view using function'''
def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,4) #4 posts in eacch page
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        #If page is out of range deliver last page of reasults
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts': posts,'page':page,'tag':tag})



'''creating a class based views for post_list view'''
# class PostListView(ListView):
#     queryset=Post.published.all()  #instead of defining a queryset attribute we could have specified model=Post and djnago would have built the gfeneric Post.objects .all()
#     context_object_name='posts'    #use the context varibale posts for the query reaults.the default variable is object_list if we dont specifiy any context_object_name
#     paginate_by=4                   #paginate the reasult displaying 4 object per page.
#     template_name='blog/post/list.html' #use a custom tempalate to render the page.If we dont set a default template ListView will use blog/post_list.html



# creating a post detail view  
'''create the comment system in post_detail view'''

from .forms import CommentForm

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    #list of active comments for this post
    comments=post.comments.filter(active=True)

    #form for creating the comment 
    if request.method=='POST':
        comment_form=CommentForm(request.POST) #populating for with posted data
        if comment_form.is_valid():
            #create the form object but don't save it to the database
            '''
            We create a new Comment object by calling the form's save() method.We create a new Comment 
            object by calling the form's save() method........Saving with commit=False gets you a model
            object, then you can add your extra data and save it........If you call it with commit=False ,
            you create the model instance, but you don't save it to the database

            '''
            new_comment=comment_form.save(commit=False)

            #Assign the current post to the comment
            new_comment.post=post

            #save the comment to the database
            new_comment.save()
    else:
        comment_form=CommentForm()
    
    #list of similar posts
    post_tags_ids=post.tags.values_list('id',flat=True)  #here .values_list return the  tuple with the value of the id...each post ko tag haru ko id tuple ma rakhxa 
    similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #here all post are filtered through the tag id that are in post tags id...here similar post contains the posts that are tagged with the same id in the post detail id
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4] #here what annotae does is it counts the numbers of tags for each objects in the queryset and returns the object..Annotate generate an independent summary for each object in a QuerySet......Aggregate generate result (summary) values over an entire QuerySet. Aggregate operate over the rowset to get a single value from the rowset.
        #similar post ko number of tags count garxa and set it in the same_tag value and returns same_tag to every post in similar_post
    return render(request,'blog/post/detail.html',{'post': post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_posts})

'''Handling forms in views'''
from .forms import EmailPostForm


def post_share(request,post_id):
    #Retrive post by id
    post=get_object_or_404(Post,id=post_id)
    sent=False
    
    if request.method=='POST':
        #form was submitted
        form=EmailPostForm(request.POST) #populatiing the for with posted data
        if form.is_valid():
            #if form field has passed validation
            
            cd=form.cleaned_data   #if form is valid the value of the form is placed in cleaned_data attribute. we retrive the validated data accessing form.cleaned_data .This attribute is the dictionary of form fields and their values.  
            post_url=request.build_absolute_uri(post.get_absolute_url())  #request.build_absolute_uri() to build a complete URL including HTTP schema and hostname..
            subject='{} ({}) recommends you reading "{}" '.format(cd['name'],cd['email'],post.title) #creating the subject to send through email
            message='Read "{}" at {} \n \n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments']) #crating the message to send through email
            send_mail(subject,message,'sandipneupane65@gmail.com',['sandip_nirvana2011@yahoo.com'],fail_silently=False) #sending mail
            sent=True
        return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent,'cd':cd}) #Note that we have declared the sent variable and set it true when mail is sent and we are going to use that varibale in the template.To display the sucess message when the form is submitted
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})


        



