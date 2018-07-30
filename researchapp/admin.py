from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Faculty,Department, Student, ResearchScholar, JournalArticle, ConferenceArticle, BookSeries, Project, Document
# Register your models here.
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportActionModelAdmin
#from core.models import 
from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class DepartmentResource(resources.ModelResource):
	class Meta:
		model = Department
		fields = ('deptname','id')

class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = DepartmentResource
	list_display = ('deptname',)
	
class FacultyResource(resources.ModelResource):
    deptname = fields.Field(column_name='deptname', attribute='deptname', widget= ForeignKeyWidget(Department, 'deptname'))
    class Meta:
        model = Faculty
        fields = ('empid','facultyname')
        import_id_fields = ['empid',]

class FacultyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = FacultyResource
	list_display = ('empid','facultyname', 'deptname',)
	list_filter = ('deptname',)
	
class StudentResource(resources.ModelResource):
	deptname = fields.Field(column_name='deptname', attribute='deptname', widget=ForeignKeyWidget(Department, 'deptname'))
	class Meta:
		model = Student
		fields = ('sregno', 'sname', 'sbranch', 'deptname', 'sbatch', 'studentcategory')
		import_id_fields = ['sregno']
		
class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = StudentResource
	list_display = ('sregno','sname','deptname','sbatch','studentcategory',)
	list_filter = ('deptname','sbatch','studentcategory',)
	
class ResearchScholarResource(resources.ModelResource):
	rssupervisor = fields.Field(column_name='rssupervisor', attribute='rssupervisor', widget=ForeignKeyWidget(Faculty, 'facultyname'))
	deptname = fields.Field(column_name='deptname', attribute='deptname', widget=ForeignKeyWidget(Department, 'deptname'))
	class Meta:
		model = ResearchScholar
		fields = ('rsname', 'rsregno', 'rssupervisor', 'deptname')
		import_id_fields = ['rsregno']
		
class ResearchScholarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ResearchScholarResource
	list_display = ('rsregno','rsname','deptname','rssupervisor',)
	list_filter = ('deptname',)

class FacultyManytoManyWidget(widgets.ManyToManyWidget):
	def clean(self, value):
		if not value:
			self.objects.none()
			facultys = value.split(";")
			results = self.model.objects.filter(faculty__site__in=facultys)
			if results.count != len(facultys):
				raise Exception('One or more of the faculty member listed was not found')
			return results
	
	def render(self, value):
		books = [str(obj.faculty) for obj in value.all()]
		return ",".join(facultys)
		
class StudentManytoManyWidget(widgets.ManyToManyWidget):
	def clean(self, value):
		if not value:
			self.objects.none()
			students = value.split(";")
			results = self.model.objects.filter(student__site__in=students)
			if results.count != len(students):
				raise Exception('One or more of the students listed was not found')
			return results

class ResearchScholarManytoManyWidget(widgets.ManyToManyWidget):
	def clean(self, value):
		if not value:
			self.objects.none()
			researchscholars = value.split(";")
			results = self.model.objects.filter(researchscholar__site__in = researchscholars)
			if results.count != len(researchscholars):
				raise Exception('One or more of the research scholars listed was not found')
			return results

class JournalArticleResource(resources.ModelResource):
	facultyauthor = fields.Field(column_name='facultyauthor', widget=FacultyManytoManyWidget(Faculty,'facultyname'))
	studentauthor = fields.Field(column_name='studentauthor', widget=StudentManytoManyWidget(Student,'sname'))
	rsauthor = fields.Field(column_name='rsauthor',widget=ResearchScholarManytoManyWidget(ResearchScholar, 'rsname'))
	
	'''def dehydrate_facultyauthor(self, journalarticle):
		return ', '.join(map(str, journalarticle.facultyauthor.all()))
	
	def dehydrate_studentauthor(self, journalarticle):
		return ', '.join(map(str,journalarticle.studentauthor.all()))
	
	def dehydrate_rsauthor(self, journalarticle):
		return ', '.join(map(str,journalarticle.rsauthor.all()))'''
		
	class Meta:
		model = JournalArticle
		fields = ('id','refformat', 'facultyauthor', 'studentauthor', 'rsauthor', 'jtitle', 'jname', 'jstatus_choice', 'jstatus', 'jpublishedon', 'jvolno', 'jissueno', 'jpageno', 'jtr', 'jsjr', 'jsnip', 'jissn', 'pubfromconf', 'created_at','updated_at','created_by','updated_by')
		import_id_fields=['id']

class JournalArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = JournalArticleResource
	#list_display = ('display_fauthor','display_sauthor','display_rsauthor','refformat','jstatus','jtr','jsjr','jsnip','jissn',)
	list_display = ('refformat',)
	list_filter = ('jtr','jsjr','jsnip','jissn',)
	
class ConferenceArticleResource(resources.ModelResource):
	facultyauthor = fields.Field(column_name='facultyauthor', widget=FacultyManytoManyWidget(Faculty,'facultyname'))
	studentauthor = fields.Field(column_name='studentauthor', widget=StudentManytoManyWidget(Student,'sname'))
	rsauthor = fields.Field(column_name='rsauthor',widget=ResearchScholarManytoManyWidget(ResearchScholar, 'rsname'))
		
	'''def dehydrate_facultyauthor(self, conferencearticle):
		return ', '.join(map(str, conferencearticle.facultyauthor.all()))
	
	def dehydrate_studentauthor(self, conferencearticle):
		return ', '.join(map(str,conferencearticle.studentauthor.all()))
	
	def dehydrate_rsauthor(self, conferencearticle):
		return ', '.join(map(str,conferencearticle.rsauthor.all()))'''
	class Meta:
		model = ConferenceArticle
		fields = ('id','refformat','facultyauthor','studentauthor', 'rsauthor', 'ctitle','cname','presentedby', 'conferencecategory', 'cdatefrom','cdateto', 'venue', 'country', 'csjr','csnip', 'cisbn', 'pubtojournalorbook', 'created_at', 'updated_at', 'created_by', 'updated_by')
		import_id_fields = ['id']

class ConferenceArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ConferenceArticleResource
	list_display = ('display_fauthor','display_sauthor','display_rsauthor','refformat','pubtojournalorbook')
	list_filter = ('conferencecategory','country','cdatefrom','cdateto','pubtojournalorbook',)

	


class BookSeriesResource(resources.ModelResource):
	facultyauthor = fields.Field(column_name='facultyauthor', widget=FacultyManytoManyWidget(Faculty,'facultyname'))
	studentauthor = fields.Field(column_name='studentauthor', widget=StudentManytoManyWidget(Student,'sname'))
	rsauthor = fields.Field(column_name='rsauthor',widget=ResearchScholarManytoManyWidget(ResearchScholar, 'rsname'))
	#facultyauthor = fields.Field(column_name='facultyauthor', attribute='facultyauthor.set()', widget=ManyToManyWidget(Faculty,))
	#fa = display_fauthor()
	#facultynames = fields.Field()
	
	'''def dehydrate_facultyauthor(self, book):
		return ', '.join(map(str, book.facultyauthor.all()))
	
	def dehydrate_studentauthor(self, book):
		return ', '.join(map(str,book.studentauthor.all()))
	
	def dehydrate_rsauthor(self, book):
		return ', '.join(map(str,book.rsauthor.all()))'''
	
#return ', '.join(map(str,book.facultyauthor.all().values('facultyname')))

	class Meta:
		model = BookSeries
		use_transactions = True
		fields = ('id','refformat', 'facultyauthor', 'studentauthor','rsauthor','booktitle', 'bookname', 'pubfromconf', 'bsjr', 'bsnip', 'bisbn', 'created_at', 'updated_at', 'created_by', 'updated_by')
		import_id_fields = ['id']
		
	

#return ', '.join([facultyauthor.facultyname for facultyauthor in self.facultyauthor.all()[:3]])


class BookSeriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ('display_fauthor', 'refformat')
	resource_class = BookSeriesResource
	list_filter = ('pubfromconf','bpublishedon',)
	

class ProjectResource(resources.ModelResource):
	facultypi = fields.Field(column_name='facultypi', widget=FacultyManytoManyWidget(Faculty,'facultyname'))
	facultycopi = fields.Field(column_name='facultycopi', widget=FacultyManytoManyWidget(Faculty,'facultyname'))
	student = fields.Field(column_name='student', widget=StudentManytoManyWidget(Student,'sname'))
	rs = fields.Field(column_name='rs',widget=ResearchScholarManytoManyWidget(ResearchScholar, 'rsname'))
	#facultyauthor = fields.Field(column_name='facultyauthor', attribute='facultyauthor.set()', widget=ManyToManyWidget(Faculty,))
	#fa = display_fauthor()
	#facultynames = fields.Field()
	
	'''def dehydrate_facultypi(self, project):
		return ', '.join(map(str, project.facultypi.all()))
	
	def dehydrate_facultycopi(self, project):
		return ', '.join(map(str, project.facultycopi.all()))
	
	def dehydrate_student(self, project):
		return ', '.join(map(str,project.student.all()))
	
	def dehydrate_rs(self, project):
		return ', '.join(map(str,project.rs.all()))'''
	class Meta:
		model = Project
		fields = ('id','facultypi', 'facultycopi', 'student', 'rs', 'projecttitle', 'fundingagency', 'projectcategory', 'projectstatus', 'duration','sanctioneddate', 'sanctionedamount', 'fundreleasedon', 'amountreceived', 'completiondate', 'outcome', 'created_at', 'updated_at', 'created_by', 'updated_by')
		import_id_fields = ['id']
		
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ProjectResource
	list_display = ('display_fpiauthor','display_fcopiauthor','display_sauthor', 'display_rsauthor', 'projectcategory', 'projectstatus', 'projecttitle', 'fundingagency','sanctionedamount',)
	list_filter = ('projectcategory', 'projectstatus','fundingagency','sanctioneddate',)
	fieldsets = (
        (None, {
            'fields': ('facultypi', 'facultycopi', 'student', 'rs',)
        }),
        ('Project Details', {
            'fields': ('projectcategory', 'projectstatus','projecttitle', 'fundingagency','duration','sanctioneddate','sanctionedamount','fundreleasedon','amountreceived','completiondate','outcome','created_by','updated_by',)
        }),
    )
	
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ResearchScholar, ResearchScholarAdmin)
admin.site.register(JournalArticle, JournalArticleAdmin)
admin.site.register(ConferenceArticle, ConferenceArticleAdmin)
admin.site.register(BookSeries, BookSeriesAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Document)