from .models import Comment, Post
from django import forms
from django.utils import timezone


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'cols': 10, 'rows': 4})
        }


class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "text",
            "pub_date",
            "location",
            "category",
            "is_published",
        )
