"""research URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
""" From Original 
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from researchapp import views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
from django_filters.views import FilterView
from researchapp.filters import FacultyFilter, StudentFilter, ResearchScholarFilter, JournalArticleFilter, ConferenceArticleFilter, BookSeriesFilter, ProjectFilter
from researchapp.models import Department, Student, ResearchScholar, JournalArticle, ConferenceArticle, Project, Faculty, BookSeries

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/$', accounts_views.signup, name='signup'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	
	url(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
url(r'^reset/done/$',
    auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
    name='password_reset_done'),
url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),
url(r'^reset/complete/$',
    auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    name='password_reset_complete'),
	
	url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
	
	url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
	
	
	
	
	url(r'^journal/(?P<pk>\d+)/$',views.journal_detail, name='journal_detail'),
	url(r'^journal/(?P<pk>\d+)/update/$',views.journal_update, name='journal_update'),
	url(r'^journal/(?P<pk>\d+)/delete/$',views.journal_delete, name='journal_delete'),
	url(r'^journal/new/$', views.journal_new, name='journal_new'),
	url(r'^conference/home/$',views.conference_home, name='conference_home'),
	url(r'^conference/(?P<pk>\d+)/$',views.conference_detail, name='conference_detail'),
	url(r'^conference/(?P<pk>\d+)/update/$',views.conference_update, name='conference_update'),
	url(r'^conference/(?P<pk>\d+)/delete/$',views.conference_delete, name='conference_delete'),
	url(r'^conference/new/$', views.conference_new, name='conference_new'),
	
	url(r'^project/home/$', views.project_home, name='project_home'),
	url(r'^project/(?P<pk>\d+)/$',views.project_detail, name='project_detail'),
	url(r'^project/(?P<pk>\d+)/update/$',views.project_update, name='project_update'),
	url(r'^project/(?P<pk>\d+)/delete/$',views.project_delete, name='project_delete'),
	url(r'^project/new/$', views.project_new, name='project_new'),
	
	url(r'^bookseries/home/$', views.bookseries_home, name='bookseries_home'),
	url(r'^bookseries/(?P<pk>\d+)/$',views.bookseries_detail, name='bookseries_detail'),
	url(r'^bookseries/(?P<pk>\d+)/update/$',views.bookseries_update, name='bookseries_update'),
	url(r'^bookseries/(?P<pk>\d+)/delete/$',views.bookseries_delete, name='bookseries_delete'),
	url(r'^bookseries/new/$', views.bookseries_new, name='bookseries_new'),
	
	
	url(r'^search/$', views.search, name='search'),
	url(r'^searchjournal/$', views.searchjournal, name='searchjournal'),
	
	url(r'^searchconference/$', views.searchconference, name='searchconference'),
	url(r'^searchproject/$', views.searchproject, name='searchproject'),
	url(r'^searchbookseries/$', views.searchbookseries, name='searchbookseries'),
	url(r'^uploadhome/$', views.uploadhome, name='uploadhome'),
	url(r'^fileupload/$', views.fileupload, name='fileupload'),
	
	url(r'admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
