from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime, timedelta


class DevelopmentProject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, default='Unknown')
    tag_line = models.CharField(max_length=255, null=False, blank=False, default='_tag_line_not_defined_until_now_')
    version = models.CharField(max_length=100, null=False, blank=False, default='v0.0.1 - alpha')
    start_date = models.DateTimeField(default=datetime.now())
    last_date = models.DateTimeField(default=datetime.now()+timedelta(weeks=+4))
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='dev/images/project/', null=True, blank=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class DevelopmentFeedback(models.Model):
    STATUS = (
        ('1', 'Pending'),
        ('2', 'Reviewed'),
        ('3', 'Completed'),
    )

    name = models.CharField(max_length=100, help_text='')
    description = RichTextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    status = models.CharField(max_length=1, default='1', null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client Feedback'
        verbose_name_plural = 'Client Feedback'

    def __str__(self):
        return self.name


class DevelopmentIteration(models.Model):
    sequence = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='dev/images/iterations/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Development Iteration'
        verbose_name_plural = 'Development Iterations'

    def __str__(self):
        return self.name


class DevelopmentDiscussion(models.Model):

    QUESTION_TYPE = (
        ('1', 'Application Idea and Research'),
        ('2', 'Application Design UI/UX'),
        ('3', 'Business Logic'),
        ('4', 'Bugs Issues Errors and Other problems'),
        ('5', 'Missing requirements and fixes'),
        ('6', 'Security Vulnerabilities'),
        ('0', 'Undefined'),
    )

    topic = models.CharField(
        max_length=1, choices=QUESTION_TYPE,
        help_text="Select Your discussion category if you didn't find select undefined"
    )
    description = models.TextField(
        help_text='Have something in mind? lets start to write'
    )
    started_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='QUESTION_BY')

    is_answered = models.BooleanField(default=False)
    is_satisfied = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussion Board'

    def __str__(self):
        return self.question


class DevelopmentDiscussionAnswer(models.Model):

    discussion = models.ForeignKey(DevelopmentDiscussion, on_delete=models.CASCADE, null=True,
                                   blank=True)
    answer = RichTextField(null=False, blank=False)
    answer_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ANSWERED_BY')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Discussion Answer'
        verbose_name_plural = 'Discussion Answers'

    def __str__(self):
        return self.discussion.question
