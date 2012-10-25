from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
#from django.db.models.signals import post_save

# Student Class relates default user model

class UserProfile(models.Model):
    user = models.OneToOneField(User,blank=True,related_name='colleger')
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    
    @property
    def is_student(self):
        try:
            self.student
            return True
        except Student.DoesNotExist:
            return False
    
class Address(models.Model):
    website = models.CharField(max_length=32, null=True, blank=True)
    blog = models.CharField(max_length=32, null=True, blank=True)
    address_line1 = models.CharField(max_length=32, null=True, blank=True)
    address_line2 = models.CharField(max_length=32, null=True, blank=True)
    address_line3 = models.CharField(max_length=32, null=True, blank=True)
    pincode = models.CharField(max_length=6,null=True, blank=True)
    area = models.CharField(max_length=32,null=True, blank=True)
    city = models.CharField(max_length=32,null=True, blank=True)
    state = models.CharField(max_length=32,null=True, blank=True)
    country = models.CharField(max_length=24,null=True, blank=True)
    phone = models.CharField(max_length=16,null=True, blank=True)
    
class College(models.Model):
    AFFILIATION = (
        ('anna_univ', 'Anna University'),
        ('deemed', 'Deemed'),
        ('autonomous', 'Autonomous'),
    )
    TYPE = (
        ('govt', 'Government'),
        ('govt_aid', 'Government-Aided'),
        ('private', 'Private'),
    )
    address = models.ForeignKey(Address,blank=True, null=True)
    name = models.CharField(max_length=64)
    ugc_cgpa = models.CharField(max_length=16, null=True, blank=True)
    ugc_grade = models.CharField(max_length=16, null=True, blank=True)
    established = models.CharField(max_length=16, null=True, blank=True)
    faculties = models.CharField(max_length=4, null=True, blank=True)
    affiliation = models.CharField(max_length=12, choices=AFFILIATION, null=True, blank=True)
    college_type = models.CharField(max_length=12, choices=TYPE, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class Skill(models.Model):
    SKILLS = (
        ('c', 'C'),
        ('cpp', 'C++'),
        ('vb', 'VB'),
        ('java', 'JAVA'),
    )
    TYPES = (
        ('soft', 'Soft-Skills'),
        ('it', 'IT-Skills'),
    )
    skill = models.CharField(max_length=8, choices=SKILLS, null=True, blank=True)
    skill_type = models.CharField(max_length=8, choices=TYPES, null=True, blank=True)

class Student(UserProfile):
    student = models.OneToOneField(UserProfile,related_name='student')
    skills = models.ManyToManyField(Skill, through='SkillSet')
    # todo: better field name
    study = models.ManyToManyField(College, through='Education')
    address = models.ForeignKey(Address,blank=True, null=True)
    passport = models.CharField(max_length=16, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/%Y/%m/%d')
    dob = models.DateField(null=True, blank=True)
    #avatar = models.FileField()
    #profile_photo = models.FileField()
    #tenth_certificate = models.FileField()
    #hsc_certificate = models.FileField()
    tenth_percentage = models.CharField(max_length=5, null=True, blank=True)
    hsc_percentage = models.CharField(max_length=5, null=True, blank=True)
 
class Professor(UserProfile):
    professor = models.OneToOneField(UserProfile,related_name='professor')
    working = models.ManyToManyField(College, through='Teaching', blank=True) 
    address = models.ForeignKey(Address,blank=True, null=True)
    # todo: each model will already have a pk unique id
    # prof_id = models.CharField(max_length=24, null=True, blank=True)

class Education(models.Model):
    YEAR_IN = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    )
    BRANCHES = (
        ('aero', 'Aeronautics'),
        ('auto', 'Automobile'),
        ('cs', 'Computer Science'),
        ('civ', 'Civil'),
        ('eee', 'Electrical and Electronics'),
        ('ece', 'Electronics and Communication'),
        ('it', 'Information Technology'),
        ('mech', 'Mechanical'),
        ('mecht', 'Mechatronics'),
    )
    college = models.ForeignKey(College, null=True, blank=True)
    student = models.ForeignKey(Student, null=True, blank=True)
    roll_no = models.CharField(max_length=24, null=True, blank=True)
    register_no = models.CharField(max_length=24, null=True, blank=True)
    # todo: what are the below 2 fields?
    doj = models.CharField(max_length=4, null=True, blank=True)
    dop = models.CharField(max_length=4, null=True, blank=True)
    year = models.CharField(max_length=2, choices=YEAR_IN, null=True, blank=True)
    branch = models.CharField(max_length=8, choices=BRANCHES, null=True, blank=True)
    
class SkillSet(models.Model):
    RATING = (
        ('beginner', 'Beginner'),
        ('learner', 'Learner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    )
    skill = models.ForeignKey(Skill)
    student = models.ForeignKey(Student)
    # todo: I'm changing this to a rating field
    rating = models.CharField(max_length=8, choices=RATING, null=True, blank=True)
    # todo: why are best_score and last_score charfields?
    best_score = models.CharField(max_length=8, choices=RATING, null=True, blank=True)
    last_score = models.CharField(max_length=8, choices=RATING, null=True, blank=True)
    
class Teaching(models.Model):
    BRANCHES = (
        ('aero', 'Aeronautics'),
        ('auto', 'Automobile'),
        ('cs', 'Computer Science'),
        ('civ', 'Civil'),
        ('eee', 'Electrical and Electronics'),
        ('ece', 'Electronics and Communication'),
        ('it', 'Information Technology'),
        ('mech', 'Mechanical'),
        ('mecht', 'Mechatronics'),
    )
    SUBJECTS = (
        ('maths', 'Maths'),
        ('ed', 'Engineering Drawing'),
        ('atd', 'Applied Thermodynamics'),
        ('pe', 'Power Electronics'),
    )
    college = models.ForeignKey(College)
    professor = models.ForeignKey(Professor)
    date_of_joining = models.DateField(null=True, blank=True)
    date_left = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=2, choices=SUBJECTS, null=True, blank=True)
    branch = models.CharField(max_length=8, choices=BRANCHES, null=True, blank=True)
    
class Company(models.Model):
    address = models.ForeignKey(Address, blank=True, null=True)
    name = models.CharField(max_length=48)
    head_count = models.CharField(max_length=8, blank=True, null=True)
    revenue = models.CharField(max_length=12, blank=True, null=True)
    headquarters = models.CharField(max_length=64)  
    
class Employer(UserProfile):
    employer = models.OneToOneField(UserProfile,related_name='employer') 
    address = models.ForeignKey(Address,blank=True, null=True)
    # todo: each model will already have a pk unique id
    # emp_id = models.CharField(max_length=24, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
