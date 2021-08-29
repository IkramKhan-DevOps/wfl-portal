from django.contrib import admin
from .models import (
    DevelopmentIteration, DevelopmentFeedback,
    DevelopmentDiscussion, DevelopmentDiscussionAnswer,
    DevelopmentProject
)


admin.site.register(DevelopmentProject)
admin.site.register(DevelopmentIteration)
admin.site.register(DevelopmentDiscussion)
admin.site.register(DevelopmentDiscussionAnswer)
admin.site.register(DevelopmentFeedback)

'''_______________________________________________________________________________________________________________'''

admin.site.site_header = 'EXARTH - DEV - Root Access'
admin.site.site_title = ' Root Access'
admin.site.index_title = 'System Apps'
