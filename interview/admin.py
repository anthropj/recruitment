from django.contrib import admin
from django.http import HttpResponse
from django.forms import modelform_factory
from django.db.models import Q
from django.utils.safestring import mark_safe

from .models import Candidate
from . import candidate_fields as cf
# from .dingtalk import send
from jobs.models import Resume
from .tasks import send_dingtalk_message

import csv
from datetime import datetime
import codecs
import logging

logger = logging.getLogger(__name__)

exported_list = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
                     'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')

def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""

    for obj in queryset:
        candidates = obj.username + ';' + candidates
        interviewers = obj.first_interviewer_user.username + ';' + interviewers
    send_dingtalk_message.delay("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )

def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type = 'text/csv')
    field_list = exported_list
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )
    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    # print(queryset.all())
    for obj in queryset:
        csv_line_list = []
        for field in field_list:
            field_obj = queryset.model._meta.get_field(field)
            field_value = field_obj.value_from_object(obj)
            csv_line_list.append(field_value)
        writer.writerow(csv_line_list)
    
    logger.info("%s has exported %s candidate records" % (request.user.username, len(queryset)))
    return response

notify_interviewer.short_description = '通知一面面试官'

export_model_as_csv.short_description = '导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)

# Register your models here.
class InterviewAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv, notify_interviewer]

    list_display = ('username', 'city', 'bachelor_school', 'get_resume', 'first_score', 'first_result',
                    'first_interviewer_user', 'second_result', 'second_interviewer_user',
                    'hr_score', 'hr_result', 'last_editor')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')
    
    # 筛选字段
    list_filter = ('city','first_result','second_result','hr_result','first_interviewer_user','second_interviewer_user','hr_interviewer_user')

    # 排序字段
    ordering = ('hr_result','second_result','first_result')

    def get_group_name(self, user):
        group_names = [g.name for g in user.groups.all()]            
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_name(request.user)

        if 'interviewer' in group_names:
            logger.info('interviewer is in user\'s group for %s' % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    # def get_changelist_formset(self, request, **kwargs):
    #     if request.user.is_superuser or 'hr' in self.get_group_name(request.user):
    #         kwargs['formset'] = modelform_factory(Candidate, fields=['first_interviewer_user', 'second_interviewer_user'])
    #     kwargs['formset'] = modelform_factory(Candidate, fields=[])
    #     return super().get_changelist_formset(request, **kwargs)

    def get_list_editable(self, request):
        group_names = self.get_group_name(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(InterviewAdmin, self).get_changelist_instance(request)

    def get_fieldsets(self, request, obj):
        group_names = self.get_group_name(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        group_names = self.get_group_name(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return qs.filter(first_interviewer_user = request.user) | qs.filter(second_interviewer_user = request.user)

    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' %(opts.app_label, 'export'))

    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe('<a href="/resume/%s" target="_blank">%s</a>' % (resumes[0].id, '查看简历'))
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True


admin.site.register(Candidate, InterviewAdmin)