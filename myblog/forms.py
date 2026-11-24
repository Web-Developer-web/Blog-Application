from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "category",
            "featured_image",
            "short_description",
            "content",
            "tags",
            "status",
            "is_featured",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter a compelling post title...",
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "auto-generated-if-left-blank",
            }),
            "category": forms.Select(attrs={"class": "form-select"}),
            "featured_image": forms.ClearableFileInput(attrs={"class": "form-file"}),
            "short_description": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 3,
                "placeholder": "Brief summary shown on cards and previews...",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-textarea form-textarea--lg",
                "rows": 10,
                "placeholder": "Write your full post content here...",
            }),
            "tags": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "django, python, webdev",
            }),
            "status": forms.Select(attrs={"class": "form-select"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }