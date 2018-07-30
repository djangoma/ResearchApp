from import_export import resources
from .models import Faculty

class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty