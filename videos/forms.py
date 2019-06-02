from django import forms

from videos.models import Video


class UserAdvancedSearchVideoForm(forms.Form):
    title = forms.CharField(label="title", required=False)
    user = forms.CharField(label="user", required=False)
    description = forms.CharField(label="description", required=False)
    likes = forms.IntegerField(label="likes", required=False)
    dislikes = forms.IntegerField(label="dislikes", required=False)
    views = forms.IntegerField(label="views", required=False)
    subjects = forms.CharField(label="subject", required=False)

    class Meta:
        model = Video
        fields = [
            'title',
            'user',
            'description',
            'likes',
            'dislikes',
            'views',
            'subjects',
        ]
