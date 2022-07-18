from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'content', 'category')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows': 4
    }))

    class Meta:
        model = Comment
        fields = ('content',)
