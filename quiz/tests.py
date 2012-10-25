from models import *
q=Quiz.objects.get(pk=1)
qi=QuizInstance.objects.get(pk=1)
print q.get_instances_last_month
