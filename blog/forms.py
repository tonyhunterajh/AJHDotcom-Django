from .models import Post, Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class EmailPostForm(forms.Form):
    sender = forms.CharField(max_length=25)
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
