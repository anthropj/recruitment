from django.shortcuts import render
from django.http import Http404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .models import Job, JobTypes, Cities, Resume

# Create your views here.
def joblist(request):
    job_list = Job.objects.all()
    for job in job_list:
        job.job_type = JobTypes[job.job_type][1]
        job.job_city = Cities[job.job_city][1]
    return render(request, 'joblist.html', locals())

def job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.job_type = JobTypes[job.job_type][1]
        job.job_city = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404('Job does not exist')
    return render(request, 'job.html', locals())

class ResumeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'resume_form.html'
    success_url = '/joblist'
    model = Resume
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]

    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'resume_detail.html'