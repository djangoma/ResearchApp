# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import mark_safe
from markdown import markdown
import datetime
from django.db import models

class Document(models.Model):
	description = models.CharField(max_length = 255, blank = True)
	document = models.FileField(upload_to = 'documents/')
	uploaded_at = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return self.description
		
class Department(models.Model):
	deptname = models.CharField(verbose_name='Department Name', max_length=50)
	
	def __str__(self):
		return self.deptname
	
		
class Faculty(models.Model):
	empid = models.CharField(primary_key=True, verbose_name="Employee ID",max_length=20)
	deptname=models.ForeignKey('Department', verbose_name="Department Name", on_delete=models.CASCADE, )
	facultyname=models.CharField(verbose_name="Faculty Name",max_length=100)
		
	def __str__(self):
		return self.facultyname
		
	#def display_deptname(self):
	#	return ', '.join([dname.deptname for dname in self.deptname.all() ])
	
	#display_deptname.short_description = 'Department Name'
		
class Student(models.Model):
	sregno = models.CharField(primary_key=True,verbose_name="Registration Number", max_length=20)
	sname = models.CharField(verbose_name="Student Name", max_length=100)
	sbranch = models.CharField(verbose_name="Branch", max_length=50)
	deptname = models.ForeignKey('Department', verbose_name="Department Name",on_delete=models.CASCADE,)
	sbatch = models.CharField(verbose_name="Batch", max_length=20)
	UG ='UG Student'
	PG ='PG Student'
	studentcategory_choice=((UG,'UG Student'),(PG,'PG Student'),)
	studentcategory=models.CharField(verbose_name="Student Category",max_length=20,choices=studentcategory_choice, default=UG)
	def __str__(self):
		return self.sname
		
	#def display_deptname(self):
	#	return ', '.join([dname.deptname for dname in self.deptname.all() ])
	
	#display_deptname.short_description = 'Department Name'
	
class ResearchScholar(models.Model):
	rsname = models.CharField(verbose_name="Student Name", max_length=100)
	rsregno = models.CharField(primary_key=True,verbose_name="Registration Number", max_length=20)
	rssupervisor = models.ForeignKey('Faculty',verbose_name="Supervisor's Name", on_delete=models.CASCADE,)
	deptname = models.ForeignKey('Department', verbose_name="Department Name", on_delete=models.CASCADE,)
	def __str__(self):
		return self.rsname
		
class JournalArticle(models.Model):
	
	refformat=models.TextField(verbose_name="Citation Format",max_length=500,blank=False)
	facultyauthor = models.ManyToManyField('Faculty',verbose_name="Faculty Author",max_length=100)
	studentauthor = models.ManyToManyField('Student',verbose_name="Student Author",max_length=100,blank=True)
	rsauthor = models.ManyToManyField('ResearchScholar',verbose_name="Research Scholar Author",max_length=100,blank=True)
	jtitle = models.CharField(verbose_name="Paper Title",max_length=200,blank=False,default='')
	jname = models.CharField(verbose_name="Journal Name",max_length=200,blank=False,default='')
	Accepted = 'Accepted'
	Submitted = 'Submitted'
	Published = 'Published'
	UnderReview = 'Under Review' 
	jstatus_choice = ((Accepted,'Accepted'),(Submitted,'Submitted'),(Published, 'Published'), (UnderReview,'Under Review'))
	jstatus = models.CharField(verbose_name="Publication Status",max_length=15,choices=jstatus_choice, default=Published)
	jpublishedon = models.DateField(verbose_name="Publication Date", blank = True, null = True)
	jvolno = models.IntegerField(verbose_name="Volume",blank=True, null = True)
	jissueno = models.IntegerField(verbose_name="Issue No",blank=True, null = True)
	jpageno = models.CharField(verbose_name="Page No",max_length=20, blank=True, null = True)
	jtr = models.FloatField(verbose_name="SCI-IF", null=True, blank=True)
	jsjr = models.FloatField(verbose_name="SJR", null=True, blank=True)
	jsnip = models.FloatField(verbose_name="SNIP", null=True, blank=True)
	jissn = models.IntegerField(verbose_name="ISSN NO",null=True, blank=True)
	YES='Yes'
	NO='No'
	pubfromconf_choice=((YES,'Yes'),(NO,'No'),)
	pubfromconf=models.CharField(verbose_name="Through conf.",max_length=5,choices=pubfromconf_choice, default=NO)
	YES='Yes'
	NO='No'
	paynopay_choice=((YES,'Yes'),(NO,'No'),)
	paynopay=models.CharField(verbose_name="Paid Journal",max_length=5,choices=paynopay_choice, default=NO)
	country = models.CharField(verbose_name="Country, published from", max_length=50, null = True)
	created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name="Updated At", null = True)
	created_by = models.ForeignKey(User, related_name = 'journals', on_delete=models.CASCADE,)
	updated_by = models.ForeignKey(User, null = True, related_name = '+', on_delete=models.CASCADE,)
	
	def __str__(self):
		return self.refformat
		
	def get_absolute_url(self):
		return reverse('researchapp:journal_detail',kwargs={'pk': self.pk} )
	
	def get_refformat_as_markdown(self):
		return mark_safe(markdown(self.refformat, safe_mode = 'escape'))
		
	def display_fauthor(self):
		return ', '.join([facultyauthor.facultyname for facultyauthor in self.facultyauthor.all()[:3]])
	
	display_fauthor.short_description = 'Faculty Name'
	
	def display_sauthor(self):
		return ', '.join([studentauthor.sname for studentauthor in self.studentauthor.all()[:3]])
	
	display_sauthor.short_description = 'Student Name'
	
	def display_rsauthor(self):
		return ', '.join([rsauthor.rsname for rsauthor in self.rsauthor.all()[:3]])
	
	display_rsauthor.short_description = 'RS Name'
		
class ConferenceArticle(models.Model):
	refformat=models.TextField(verbose_name="Citation Format",max_length=500,blank=False)
	facultyauthor = models.ManyToManyField('Faculty',verbose_name="Faculty Author",max_length=100)
	studentauthor = models.ManyToManyField('Student',verbose_name="Student Author",max_length=100,blank=True)
	rsauthor = models.ManyToManyField('ResearchScholar',verbose_name="Research Scholar Author",max_length=100,blank=True)
	ctitle = models.CharField(verbose_name="Paper Title",max_length=200,blank=False,default='')
	cname = models.CharField(verbose_name="Conference Name",max_length=200,blank=False,default='')
	presentedby=models.CharField(verbose_name="Presented By",max_length=50)
	NATIONAL='National'
	INTERNATIONAL='International'
	conferencecategory_choice=((NATIONAL,'National'),(INTERNATIONAL,'International'),)
	conferencecategory=models.CharField(verbose_name="Conference Category",max_length=50,choices=conferencecategory_choice, default=INTERNATIONAL)
	cdatefrom=models.DateField(verbose_name="Conference Date From: ")
	cdateto=models.DateField(verbose_name="Conference Date To: ")
	venue=models.CharField(verbose_name="Venue",max_length=100)
	country = models.CharField(verbose_name="Country", max_length=50)
	csjr = models.FloatField(verbose_name="SJR", null=True, blank=True)
	csnip = models.FloatField(verbose_name="SNIP", null=True, blank=True)
	cisbn = models.FloatField(verbose_name="ISBN", null=True, blank=True)
	
	NO='No'
	JOURNAL = 'Journal'
	BOOKSERIES = 'Book Series'
	pubtojournalorbook_choice=((NO,'No'),(JOURNAL,'Journal'),(BOOKSERIES,'Book Series'))
	pubtojournalorbook=models.CharField(verbose_name="To be Published as Journal/ Book",max_length=50,choices=pubtojournalorbook_choice, default=NO)
	created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name="Updated At", null = True)
	created_by = models.ForeignKey(User, related_name = 'conferences', on_delete=models.CASCADE,)
	updated_by = models.ForeignKey(User, null = True, related_name = '+', on_delete=models.CASCADE,)
		
	def __str__(self):
		return self.refformat
	
	def get_absolute_url(self):
		return reverse('researchapp:conference_detail',kwargs={'pk': self.pk} )
		
	def display_fauthor(self):
		return ', '.join([facultyauthor.facultyname for facultyauthor in self.facultyauthor.all()[:3]])
	
	display_fauthor.short_description = 'Faculty Name'
	
	def display_sauthor(self):
		return ', '.join([studentauthor.sname for studentauthor in self.studentauthor.all()[:3]])
	
	display_sauthor.short_description = 'Student Name'
	
	def display_rsauthor(self):
		return ', '.join([rsauthor.rsname for rsauthor in self.rsauthor.all()[:3]])
	
	display_rsauthor.short_description = 'RS Name'

class BookSeries(models.Model):
	refformat=models.TextField(verbose_name="Citation Format",max_length=500,blank=False)
	facultyauthor = models.ManyToManyField('Faculty',verbose_name="Faculty Author")
	studentauthor = models.ManyToManyField('Student',verbose_name="Student Author",blank=True)
	rsauthor = models.ManyToManyField('ResearchScholar',verbose_name="Research Scholar Author",blank=True)
	booktitle = models.CharField(verbose_name="Paper Title",max_length=200,blank=False,default='')
	bookname = models.CharField(verbose_name="Book Title",max_length=200,blank=False,default='')
	bpublishedon = models.DateField(verbose_name="Publication on:",default=datetime.date.today )
	YES='Yes'
	NO='No'
	pubfromconf_choice=((YES,'Yes'),(NO,'No'),)
	pubfromconf=models.CharField(verbose_name="Through conf.",max_length=50,choices=pubfromconf_choice, default=NO)
	bsjr = models.FloatField(verbose_name="SJR", null=True, blank=True)
	bsnip = models.FloatField(verbose_name="SNIP", null=True, blank=True)
	bisbn = models.FloatField(verbose_name="ISBN", null=True, blank=True)
	created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
	updated_at = models.DateField(verbose_name="Updated At", null = True)
	created_by = models.ForeignKey(User, related_name = 'books', on_delete=models.CASCADE,)
	updated_by = models.ForeignKey(User, null = True, related_name = '+', on_delete=models.CASCADE,)
	
	def __unicode__(self):
		return self.refformat
	
	def __str__(self):
		return self.refformat
		
	def display_fauthor(self):
		return ', '.join([facultyauthor.facultyname for facultyauthor in self.facultyauthor.all()[:3]])
	
	display_fauthor.short_description = 'Faculty Name'
	
	def display_sauthor(self):
		return ', '.join([studentauthor.sname for studentauthor in self.studentauthor.all()[:3]])
	
	display_sauthor.short_description = 'Student Name'
	
	def display_rsauthor(self):
		return ', '.join([rsauthor.rsname for rsauthor in self.rsauthor.all()[:3]])
	
	display_rsauthor.short_description = 'RS Name'
		
class Project(models.Model):
	facultypi = models.ManyToManyField('Faculty',verbose_name="Principal Investigator", related_name = 'projectpis', blank=True)
	facultycopi = models.ManyToManyField('Faculty', verbose_name="Co-Principal Investigator", related_name = 'projectcopis', blank = True)
	student = models.ManyToManyField('Student',verbose_name="Student",blank=True)
	rs = models.ManyToManyField('ResearchScholar',verbose_name="Research Scholar",blank=True)
	projecttitle = models.CharField(verbose_name="Project Title",max_length=200)
	fundingagency=models.CharField(verbose_name="Funding Agency",max_length=200)
	EXTERNAL='External'
	INTERNALFACULTY='Internal Faculty'
	INTERNALSTUDENT='Internal Student'
	projectcategory_choice=((EXTERNAL,'External'),(INTERNALFACULTY,'Internal Faculty'),(INTERNALSTUDENT,'Internal Student'),)
	projectcategory=models.CharField(verbose_name="Project Category",max_length=50,choices=projectcategory_choice, default=EXTERNAL)
	
	SUBMITTED='Submitted'
	ONGOING='Ongoing'
	COMPLETED='Completed'
	RESULTSPENDING = 'Results Pending'
	REJECTED = 'Rejected'
	projectstatus_choice=((SUBMITTED,'Submitted'),(ONGOING,'Ongoing'),(COMPLETED,'Completed'),(RESULTSPENDING,'Results Pending'),(REJECTED,'Rejected'),)
	projectstatus=models.CharField(verbose_name="Project Status",max_length=50,choices=projectstatus_choice, default=ONGOING)
	duration=models.CharField(verbose_name="Duration",max_length=50)
	sanctioneddate=models.DateField(verbose_name="Sanctioned Date")
	sanctionedamount=models.FloatField(verbose_name="Sanctioned Amount",blank = True, null = True)
	fundreleasedon=models.CharField(verbose_name="Fund Released On",max_length=20, blank=True, null = True)
	amountreceived=models.CharField(verbose_name="Amount Received",max_length=200, blank=True, null = True)
	completiondate=models.DateField(verbose_name="Completion Date", blank = True, null = True)
	outcome=models.TextField(verbose_name="Outcome",max_length=500, blank=True)
	created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name="Updated At", null = True)
	created_by = models.ForeignKey(User, related_name = 'projects', on_delete=models.CASCADE,)
	updated_by = models.ForeignKey(User, null = True, related_name = '+', on_delete=models.CASCADE,)
	
	def __str__(self):
		return self.projecttitle
		
	def get_absolute_url(self):
		return reverse('researchapp:project_detail',kwargs={'pk': self.pk} )
		
	def display_fpiauthor(self):
		return ', '.join([facultypi.facultyname for facultypi in self.facultypi.all()[:3]])
	
	display_fpiauthor.short_description = 'PI Name'
	
	def display_fcopiauthor(self):
		return ', '.join([facultycopi.facultyname for facultycopi in self.facultycopi.all()[:3]])
	
	display_fcopiauthor.short_description = 'PI Name'
	
	def display_sauthor(self):
		return ', '.join([studentauthor.sname for studentauthor in self.student.all()[:3]])
	
	display_sauthor.short_description = 'Student Name'
	
	def display_rsauthor(self):
		return ', '.join([rsauthor.rsname for rsauthor in self.rs.all()[:3]])
	
	display_rsauthor.short_description = 'RS Name'