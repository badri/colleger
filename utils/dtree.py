'''
possible outcomes and explanations
improve score => re-take the same quiz and improve score
same course => take the course associated with this quiz
block quiz => impose time constraint on the particular quiz for the student, i.e. quiz can't be re-taken for 1 month.
challenge friends => share score with friends and challenge them to beat your score.
next course => unlock next course
next quiz => unlock next quiz
show jobs => show jobs associated with this quiz

Usage:
>>> decisions['fail']['2']
['same course']
>>> decisions['pass']['2']
['next course', 'challenge friends', 'block quiz']
'''

dtree = '''
fail	1	improve score
fail	2	same course
fail	3	same course,block quiz
pass	1	next course,challenge friends,improve score
pass	2	next course,challenge friends,block quiz
high	1	next course,challenge friends,next quiz,improve score
high	2	next course,challenge friends,block quiz
full	1	next course,challenge friends,next quiz,show jobs
'''

decisions = {}
for i in dtree.strip().split('\n'):    
    result, attempt, outcome = i.split('\t')
    try:
        decisions[result][attempt] =outcome.split(',')
    except:
        decisions[result] = {}
        decisions[result][attempt] =outcome.split(',')


