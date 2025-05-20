from django import forms

# Models
from comments.models import Comment
from django.contrib.auth.models import User

class CreateCommentForm(forms.ModelForm):
    """Form for creating comments."""

    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Comentario')

    class Meta:
        """Form settings."""

        model = Comment
        fields = ('comment',)

    def clean_comment(self):
        """Validate the comment field."""
        comment = self.cleaned_data['comment'].strip()
        if not comment:
            raise forms.ValidationError("Este campo es obligatorio.")
        return comment