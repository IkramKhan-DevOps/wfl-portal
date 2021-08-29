from django.forms import ModelForm, Textarea
from .models import DevelopmentDiscussion, DevelopmentDiscussionAnswer


class DevelopmentDiscussionForm(ModelForm):
    class Meta:
        model = DevelopmentDiscussion
        fields = (
            'topic', 'description'
        )
        widgets = {
            'question': Textarea(attrs={'cols': 80, 'rows': 10})
        }


class DevelopmentDiscussionAnswerForm(ModelForm):
    class Meta:
        model = DevelopmentDiscussionAnswer
        fields = (
            'answer',
        )
        widgets = {
            'answer': Textarea(attrs={'cols': 80, 'rows': 10})
        }
