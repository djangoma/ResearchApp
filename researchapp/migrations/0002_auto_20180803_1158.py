# Generated by Django 2.0.1 on 2018-08-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookseries',
            name='refformat',
            field=models.TextField(max_length=300, verbose_name='Citation Format'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='cname',
            field=models.CharField(default='', max_length=50, verbose_name='Conference Name'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='ctitle',
            field=models.CharField(default='', max_length=50, verbose_name='Paper Title'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='facultyauthor',
            field=models.ManyToManyField(max_length=30, to='researchapp.Faculty', verbose_name='Faculty Author'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='refformat',
            field=models.TextField(max_length=300, verbose_name='Citation Format'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='rsauthor',
            field=models.ManyToManyField(blank=True, max_length=30, to='researchapp.ResearchScholar', verbose_name='Research Scholar Author'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='studentauthor',
            field=models.ManyToManyField(blank=True, max_length=30, to='researchapp.Student', verbose_name='Student Author'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='venue',
            field=models.CharField(max_length=50, verbose_name='Venue'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='facultyauthor',
            field=models.ManyToManyField(max_length=30, to='researchapp.Faculty', verbose_name='Faculty Author'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='jname',
            field=models.CharField(default='', max_length=50, verbose_name='Journal Name'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='jtitle',
            field=models.CharField(default='', max_length=50, verbose_name='Paper Title'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='refformat',
            field=models.TextField(max_length=300, verbose_name='Citation Format'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='rsauthor',
            field=models.ManyToManyField(blank=True, max_length=30, to='researchapp.ResearchScholar', verbose_name='Research Scholar Author'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='studentauthor',
            field=models.ManyToManyField(blank=True, max_length=30, to='researchapp.Student', verbose_name='Student Author'),
        ),
        migrations.AlterField(
            model_name='project',
            name='fundingagency',
            field=models.CharField(max_length=100, verbose_name='Funding Agency'),
        ),
        migrations.AlterField(
            model_name='project',
            name='outcome',
            field=models.TextField(blank=True, max_length=300, verbose_name='Outcome'),
        ),
        migrations.AlterField(
            model_name='project',
            name='projectcategory',
            field=models.CharField(choices=[('External', 'External'), ('Internal Faculty', 'Internal Faculty'), ('Internal Student', 'Internal Student')], default='External', max_length=20, verbose_name='Project Category'),
        ),
        migrations.AlterField(
            model_name='project',
            name='projectstatus',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Results Pending', 'Results Pending'), ('Rejected', 'Rejected')], default='Ongoing', max_length=20, verbose_name='Project Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='projecttitle',
            field=models.CharField(max_length=100, verbose_name='Project Title'),
        ),
    ]
