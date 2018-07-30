from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Department, Student, ResearchScholar, JournalArticle, ConferenceArticle, Project, Faculty, BookSeries
from .forms import JournalNewForm, JournalUpdateForm, ConferenceNewForm, ConferenceUpdateForm, ProjectNewForm, ProjectUpdateForm, BookSeriesNewForm, BookSeriesUpdateForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from researchapp.filters import FacultyFilter, StudentFilter, ResearchScholarFilter, JournalArticleFilter, ConferenceArticleFilter, BookSeriesFilter, ProjectFilter
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm


def uploadhome(request):
    documents = Document.objects.all()
    return render(request, 'uploadhome.html', { 'documents': documents })

def fileupload(request):
	if request.method =='POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('uploadhome')
	else:
		form = DocumentForm()
	return render(request, 'fileupload.html', {'form':form})
	

def search(request):
	'''faculty_list = Faculty.objects.all()
	faculty_filter = FacultyFilter(request.GET, queryset=faculty_list)
	student_list = Student.objects.all()
	student_filter = StudentFilter(request.GET, queryset=student_list)
	rs_list = ResearchScholar.objects.all()
	rs_filter = ResearchScholarFilter(request.GET, queryset=rs_list)'''
	j_list = JournalArticle.objects.all()
	j_filter = JournalArticleFilter(request.GET, queryset=j_list)
	
	#return render(request, 'search/search_FacStuRsJ.html', {'faculty_filter':faculty_filter, 'student_filter':student_filter, 'rs_filter':rs_filter, 'j_filter':j_filter})
	return render(request, 'search/search_FacStuRsJ.html', {'j_filter':j_filter})
	
def searchjournal(request):
	j_list = JournalArticle.objects.all()
	j_filter = JournalArticleFilter(request.GET, queryset=j_list)
	'''print(j_filter.qs)'''
	return render(request, 'search/searchjournal.html',{'j_filter':j_filter} )
	
def searchconference(request):
	c_list = ConferenceArticle.objects.all()
	c_filter = ConferenceArticleFilter(request.GET, queryset=c_list)
	return render(request, 'search/searchconference.html', {'c_filter':c_filter})

def searchproject(request):
	p_list = Project.objects.all()
	p_filter = ProjectFilter(request.GET, queryset=p_list)
	return render(request, 'search/searchproject.html', {'p_filter':p_filter})
	
def searchbookseries(request):
	b_list = BookSeries.objects.all()
	b_filter = BookSeriesFilter(request.GET, queryset=b_list)
	return render(request, 'search/searchbookseries.html', {'b_filter':b_filter})
	
@login_required	
def home(request):
	journals=JournalArticle.objects.all()
	
	page = request.GET.get('page', 1)
	paginator = Paginator(journals, 2)
	
	try:
		j = paginator.page(page)
	except PageNotAnInteger:
		j = paginator.page(1)
	except EmptyPage:
		j = paginator.page(paginator.num_pages)
	
	journalcount = JournalArticle.objects.all().count()
	publishedcount = JournalArticle.objects.filter(jstatus='Published').count()	
	acceptedcount = JournalArticle.objects.filter(jstatus='Accepted').count()	
	submittedcount = JournalArticle.objects.filter(jstatus='Submitted').count()
	year2017 = JournalArticle.objects.all().filter(jpublishedon__year=2017).count()
	'''journal_title = list()
	for journal in journals:
		journal_title.append(journal.jpapertitle)
	response_html='<br>'.join(journal_title)
	return HttpResponse(response_html)'''
	return render(request, 'home.html', {'journals':journals, 'j':j, 'journalcount':journalcount, 'publishedcount':publishedcount, 'acceptedcount':acceptedcount,'submittedcount':submittedcount, 'year2017':year2017 })

@login_required	
def conference_home(request):
	conferences = ConferenceArticle.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(conferences, 10)
	try:
		c = paginator.page(page)
	except PageNotAnInteger:
		c = paginator.page(1)
	except EmptyPage:
		c = paginator.page(paginator.num_pages)
	
	conferencecount = ConferenceArticle.objects.all().count()
	conferenceinternationalcount = ConferenceArticle.objects.filter(conferencecategory='International').count()
	conferencenationalcount = ConferenceArticle.objects.filter(conferencecategory='National').count()
	year2017 = ConferenceArticle.objects.all().filter(cdatefrom__year=2017).count()
	return render(request, 'conference_home.html',{'conferences':conferences,'c':c, 'conferencecount':conferencecount,'conferenceinternationalcount':conferenceinternationalcount, 'conferencenationalcount':conferencenationalcount, 'year2017':year2017 })

@login_required	
def project_home(request):
	projects = Project.objects.all()
	
	page = request.GET.get('page', 1)
	paginator = Paginator(projects, 10)
	
	try:
		p = paginator.page(page)
	except PageNotAnInteger:
		p = paginator.page(1)
	except EmptyPage:
		p = paginator.page(paginator.num_pages)
		
	projextongoingcount = Project.objects.filter(projectcategory='External').filter(projectstatus='Ongoing').count()
	projintongoingfacultycount = Project.objects.filter(projectcategory='Internal Faculty').filter(projectstatus='Ongoing').count()
	projintongoingstudentcount = Project.objects.filter(projectcategory='Internal Student').filter(projectstatus='Ongoing').count()
	projextcomplettedcount = Project.objects.filter(projectcategory='External').filter(projectstatus='Completed').count()
	projintcompletedfacultycount = Project.objects.filter(projectcategory='Internal Faculty').filter(projectstatus='Completed').count()
	projintcompletedstudentcount = Project.objects.filter(projectcategory='Internal Student').filter(projectstatus='Completed').count()
	
	return render(request, 'project_home.html', {'projects':projects, 'p':p, 'projextongoingcount':projextongoingcount, 'projintongoingfacultycount':projintongoingfacultycount, 'projintongoingstudentcount':projintongoingstudentcount, 'projextcomplettedcount':projextcomplettedcount, 'projintcompletedfacultycount':projintcompletedfacultycount, 'projintcompletedstudentcount':projintcompletedstudentcount})

def bookseries_home(request):
	bookseries = BookSeries.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(bookseries, 10)
	try:
		bs = paginator.page(page)
	except PageNotAnInteger:
		bs = paginator.page(1)
	except EmptyPage:
		bs = paginator.page(paginator.num_pages)
		
	bookseriescount = BookSeries.objects.all().count()
	
	return render(request, 'bookseries_home.html', {'bookseries':bookseries, 'bs':bs,'bookseriescount':bookseriescount})
	
@login_required	
def journal_detail(request,pk):
	'''try:
		journal=Journal.objects.get(pk=pk)
	except Journal.DoesNotExist:
		raise Http404'''
	journal=get_object_or_404(JournalArticle, pk=pk)
	falist=journal.facultyauthor.all()
	salist=journal.studentauthor.all()
	rslist=journal.rsauthor.all()
	return render(request, 'journal.html', {'journal':journal, 'falist':falist, 'salist':salist, 'rslist':rslist})
	
'''def new_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'new_journal.html', {'journal': journal})'''

@login_required	
def journal_new(request):
	'''return HttpResponse("Hello World !!")'''
	journal=JournalArticle.objects.all()
	user = User.objects.first()  # TODO: get the currently logged in user
	if request.method == 'POST':
		form = JournalNewForm(request.POST)
		if form.is_valid():
			journal = form.save(commit=False)
			journal.save()
			return redirect('home')  # TODO: redirect to the created topic page
	else:
		form = JournalNewForm()
	return render(request,'journal_new.html',{'journal':journal,'form': form})

@login_required	
def journal_update(request, pk):
	journal=get_object_or_404(JournalArticle, pk=pk)
	if request.method=='POST':
		form = JournalUpdateForm(request.POST, instance=journal)
		if form.is_valid():
			journal = form.save(commit=False)
			journal.save()
			return redirect('home')
	else:
		form=JournalUpdateForm(instance=journal)
	return render(request, 'journal_update.html', {'journal':journal, 'form':form})

@login_required	
def journal_delete(request,pk):
	journal=get_object_or_404(JournalArticle, pk=pk)
	return render(request, 'journal_delete.html', {'journal':journal})
	

def conference_detail(request,pk):
	'''try:
		journal=Journal.objects.get(pk=pk)
	except Journal.DoesNotExist:
		raise Http404'''
	conference=get_object_or_404(ConferenceArticle, pk=pk)
	falist=conference.facultyauthor.all()
	salist=conference.studentauthor.all()
	rslist=conference.rsauthor.all()
	return render(request, 'conference.html', {'conference':conference, 'falist':falist, 'salist':salist, 'rslist':rslist})
	
'''def new_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'new_journal.html', {'journal': journal})'''

@login_required	
def conference_new(request):
	'''return HttpResponse("Hello World !!")'''
	conference=ConferenceArticle.objects.all()
	user = User.objects.first()  # TODO: get the currently logged in user
	if request.method == 'POST':
		form = ConferenceNewForm(request.POST)
		if form.is_valid():
			conference = form.save(commit=False)
			conference.save()
			return redirect('conference_home')  # TODO: redirect to the created topic page
	else:
		form = ConferenceNewForm()
	return render(request,'conference_new.html',{'conference':conference,'form': form})

@login_required	
def conference_update(request, pk):
	conference=get_object_or_404(ConferenceArticle, pk=pk)
	if request.method=='POST':
		form = ConferenceUpdateForm(request.POST, instance=conference)
		if form.is_valid():
			conference = form.save(commit=False)
			conference.save()
			return redirect('conference_home')
	else:
		form=ConferenceUpdateForm(instance=conference)
	return render(request, 'conference_update.html', {'conference':conference, 'form':form})

@login_required	
def conference_delete(request,pk):
	conference=get_object_or_404(ConferenceArticle, pk=pk)
	return render(request, 'conference_delete.html', {'conference':conference})

@login_required		
def project_detail(request,pk):
	'''try:
		journal=Journal.objects.get(pk=pk)
	except Journal.DoesNotExist:
		raise Http404'''
	project=get_object_or_404(Project, pk=pk)
	fapilist=project.facultypi.all()
	facopilist=project.facultycopi.all()
	salist = project.student.all()
	rslist = project.rs.all()
	
	return render(request, 'project.html', {'project':project, 'fapilist':fapilist, 'facopilist':facopilist, 'salist':salist, 'rslist':rslist})
	
'''def new_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'new_journal.html', {'journal': journal})'''

@login_required	
def project_new(request):
	'''return HttpResponse("Hello World !!")'''
	project=Project.objects.all()
	user = User.objects.first()  # TODO: get the currently logged in user
	if request.method == 'POST':
		form = ProjectNewForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.save()
			return redirect('project_home')  # TODO: redirect to the created topic page
	else:
		form = ProjectNewForm()
	return render(request,'project_new.html',{'project':project,'form': form})

@login_required		
def project_update(request, pk):
	project=get_object_or_404(Project, pk=pk)
	if request.method=='POST':
		form = ProjectUpdateForm(request.POST, instance=project)
		if form.is_valid():
			project = form.save(commit=False)
			project.save()
			return redirect('project_home')
	else:
		form=ProjectUpdateForm(instance=project)
	return render(request, 'project_update.html', {'project':project, 'form':form})

@login_required	
def project_delete(request,pk):
	project=get_object_or_404(Project, pk=pk)
	return render(request, 'project_delete.html', {'project':project})

def bookseries_detail(request,pk):
	'''try:
		journal=Journal.objects.get(pk=pk)
	except Journal.DoesNotExist:
		raise Http404'''
	bookseries=get_object_or_404(BookSeries, pk=pk)
	falist=bookseries.facultyauthor.all()
	salist=bookseries.studentauthor.all()
	rslist=bookseries.rsauthor.all()
	return render(request, 'bookseries.html', {'bookseries':bookseries, 'falist':falist, 'salist':salist, 'rslist':rslist})

def bookseries_new(request):
	'''return HttpResponse("Hello World !!")'''
	bookseries=BookSeries.objects.all()
	user = User.objects.first()  # TODO: get the currently logged in user
	if request.method == 'POST':
		form = BookSeriesNewForm(request.POST)
		if form.is_valid():
			bookseries = form.save(commit=False)
			bookseries.save()
			return redirect('bookseries_home')  # TODO: redirect to the created topic page
	else:
		form = BookSeriesNewForm()
	return render(request,'bookseries_new.html',{'bookseries':bookseries,'form': form})
	
def bookseries_update(request, pk):
	bookseries=get_object_or_404(BookSeries, pk=pk)
	if request.method=='POST':
		form = BookSeriesUpdateForm(request.POST, instance=bookseries)
		if form.is_valid():
			bookseries = form.save(commit=False)
			bookseries.save()
			return redirect('bookseries_home')
	else:
		form=BookSeriesUpdateForm(instance=bookseries)
	return render(request, 'bookseries_update.html', {'bookseries':bookseries, 'form':form})
	
def bookseries_delete(request,pk):
	bookseries=get_object_or_404(BookSeries, pk=pk)
	return render(request, 'bookseries_delete.html', {'bookseries':bookseries})