from django.contrib import admin
from .models import Job, Resume
from interview.models import Candidate
from django.contrib import messages
from django.utils.html import format_html

from datetime import datetime

class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'create_data', 'modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'create_date', 'modified_data')

    def save_model(self, request, obj, form, change):
        if obj.creator is None:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date =  datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + ',' + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人： %s 已成功进入面试环节' % (candidate_names))

enter_interview_process.short_description = '进入面试流程'

class ResumeAdmin(admin.ModelAdmin):
    actions = [enter_interview_process,]

    def image_tag(self, obj):              
        if obj.picture:
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'    

    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major', 'image_tag','created_date')

    readonly_fields = ('username', 'created_date', 'modified_date')

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience","project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)