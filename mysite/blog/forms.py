from django import forms
from .models import Comment

'''Creating the form to share post using mail'''
class EmailPostForm(forms.Form):  #form created by inheriting forms.Form base class
    name=forms.CharField(max_length=25)
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):#to create the form from the model we use form.ModelForm...we are trying to create the form from models
    class Meta:
        model=Comment #which models to use in form
        fields=('name','email','body') #select the field to display in form....we can also define the exclude field to exclude the fields