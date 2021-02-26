from django.urls import path, re_path
from .views import joblist, job, ResumeCreateView, ResumeDetailView

urlpatterns = [
    path('', joblist),
    path('joblist', joblist, name = 'job_list'),
    # re_path(r'^P<job_id>/\d+', job)
    path('job/<int:job_id>', job, name = 'job_detail'),

    path('resume/add/', ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>', ResumeDetailView.as_view(), name='resume-detail'),
]