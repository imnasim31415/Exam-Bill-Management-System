from email import message
from xmlrpc.client import FastParser
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string
from .models import *
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User

# Create your views here.

@login_required(login_url='/log')
def home(request):
    return render(request, 'home.html')

def log(request):
    if 'log' in request.POST:
        ia=faculty.objects.filter(email=request.POST.get('email'))
        if not ia:
            messages.error(request,'Account does not exist',extra_tags='log')
        else:
            ib=faculty.objects.get(email=request.POST.get('email'))
            if ib.password==request.POST.get('pass'):
                login(request,authenticate(username=ib.username,email=ib.email,password=ib.password))
                return redirect('/')
            else:
                messages.error(request,'Passwords do not match',extra_tags='log')
    return render(request, 'log.html')


def logOut(request):
    logout(request)
    return redirect('/log')


def committee(request):
    if 'sess' in request.POST:
        print('ok')
        sess = request.POST['session']
        sess = int(sess)
        ob = Session.objects.filter(year=sess)
        if not ob:
            messages.error(request, 'Session Does not Exist !!',
                           extra_tags='session')
        else:
            response = '/viewCom/'+str(request.POST['session'])
            return redirect(response)
    if 'sem' in request.POST:
        sess = request.POST['session']
        sess = int(sess)
        ob = Session.objects.filter(year=sess)
        if not ob:
            messages.error(request, 'Session Does not Exist !!',
                           extra_tags='session')
        else:
            response = '/createSem/'+str(sess)
            return redirect(response)
    return render(request, 'committee.html')


def createCom(request):
    us = User.objects.get(username=request.user.username)
    chairman = User.objects.get(username='chairman')
    cont = None
    if not us == chairman:
        messages.error(request, 'Access Denied !!!', extra_tags='access')
    else:
        ob = faculty.objects.filter()
        oc = External.objects.filter()
        cont = {'ob': ob, 'oc': oc}
        if request.method == 'POST':
            oo = Session.objects.filter(year=int(request.POST['session']))
            if not oo:
                aa = Session(year=int(request.POST['session']))
                aa.save()
            ca = Session.objects.get(year=int(request.POST['session']))
            aa = Semester.objects.filter(
                session=ca, semId=int(request.POST['year']))
            if not aa:
                chairman = faculty.objects.get(email=request.POST['chairman'])
                sob = Semester.objects.filter(session=ca)
                flag = False
                for o in sob:
                    if o.chairman == chairman:
                        flag = True
                if flag:
                    messages.error(
                        request, "Chairman Already Exists in another Committee !", extra_tags='chairman')
                else:
                    tea1 = faculty.objects.get(email=request.POST['tabular1'])
                    tea2 = faculty.objects.get(email=request.POST['tabular2'])
                    tea3 = External.objects.get(email=request.POST['external'])
                    flag = False
                    if tea1 == tea2 or tea2 == chairman or tea1 == chairman:
                        flag = True
                    if flag:
                        messages.error(
                            request, 'Faculty can not be selected more than once !!', extra_tags="twice")
                    else:
                        bb = Semester(semId=int(
                            request.POST['year']), session=ca, chairman=chairman, tabular1=tea1, tabular2=tea2, external=tea3)
                        bb.save()
                        for o in ob:
                            tea = faculty.objects.get(email=o.email)
                            aa = SemesterBill(
                                session=ca, semester=bb, teacher=tea)
                            aa.save()
                        messages.success(
                            request, "Committee Created Successfully", extra_tags="success")
            else:
                messages.error(
                    request, "Semester Already Exists !!", extra_tags="sem")
    return render(request, 'createCom.html', cont)


def viewCom(request, id):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.filter(session=session).order_by('semId')

    class Class:
        def __init__(self, qd, st):
            self.qd = qd
            self.st = st
            if qd.semId == 1:
                st = "1st Year 1st Semseter"
            if qd.semId == 2:
                st = "1st Year 2nd Semseter"
            if qd.semId == 3:
                st = "2nd Year 1st Semseter"
            if qd.semId == 4:
                st = "2nd Year 2nd Semseter"
            if qd.semId == 5:
                st = "3rd Year 1st Semseter"
            if qd.semId == 6:
                st = "3rd Year 2nd Semseter"
            if qd.semId == 7:
                st = "4th Year 1st Semseter"
            if qd.semId == 8:
                st = "4th Year 2nd Semseter"
            if qd.semId == 9:
                st = "Masters 1st Semseter"
            if qd.semId == 10:
                st = "Masters 2nd Semseter"
            self.st = st
    ar = []
    for o in semester:
        a = Class(qd=o, st=" ")
        ar.append(a)

    cont = {
        'ob': ar,
        'session': id
    }
    return render(request, 'viewCom.html', cont)


def viewSem(request, id, id2):
    ob = faculty.objects.get(email=request.user.email)
    oc = faculty.objects.filter()
    od = External.objects.filter()
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    moderator = SemesterBill.objects.filter(
        session=session, semester=semester, moderator=1)
    typist = SemesterBill.objects.filter(
        session=session, semester=semester, typist=1)
    translator = SemesterBill.objects.filter(
        session=session, semester=semester, translator=1)
    flag = False
    if ob == semester.chairman:
        flag = True
    cont = {
        'sem': semester,
        'flag': flag,
        'ob': oc,
        'oc': od,
        'moderator': moderator,
        'typist': typist,
        'translator': translator
    }

    if 'update' in request.POST:
        tea1 = faculty.objects.get(email=request.POST['tabular1'])
        tea2 = faculty.objects.get(email=request.POST['tabular2'])
        tea3 = External.objects.get(email=request.POST['external'])
        flag = False

        if tea1 == tea2:
            flag = True
        if flag:
            messages.error(
                request, 'Faculty can not be selected more than once !!', extra_tags="twice")
        else:
            semester.tabular1 = faculty.objects.get(
                email=request.POST.get('tabular1'))
            semester.tabular2 = faculty.objects.get(
                email=request.POST.get('tabular2'))
            semester.external = External.objects.get(
                email=request.POST.get('external'))
            semester.save()
            messages.success(
                request, 'Committee Updated Successfully !', extra_tags='update')
    con = None
    if 'add' in request.POST:
        response = '/addRole/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'moderator' in request.POST:
        mod = faculty.objects.get(email=request.POST.get('moderator'))
        oc = SemesterBill.objects.get(
            session=session, semester=semester, teacher=mod)
        oc.moderator = 0
        oc.save()
        response = '/viewSem/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'translator' in request.POST:
        print(request.POST.get('translator'))
        mod = faculty.objects.get(email=request.POST.get('translator'))
        oc = SemesterBill.objects.get(
            session=session, semester=semester, teacher=mod)
        oc.translator = 0
        oc.save()
        response = '/viewSem/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'typist' in request.POST:
        print('ss')
        mod = faculty.objects.get(email=request.POST.get('typist'))
        oc = SemesterBill.objects.get(
            session=session, semester=semester, teacher=mod)
        oc.typist = 0
        oc.save()
        response = '/viewSem/'+str(id)+'/'+str(id2)
        return redirect(response)
    return render(request, 'viewSem.html', cont, con)


def addRole(request, id, id2):
    ob = faculty.objects.filter()
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    tea = faculty.objects.get(email=request.user.email)
    chairman = semester.chairman
    flag = False
    if chairman == tea:
        flag = True
    cont = {'ob': ob,
            'flag': flag
            }
    if request.method == 'POST':
        session = Session.objects.get(year=int(id))
        semester = Semester.objects.get(session=session, semId=int(id2))
        oo = SemesterBill.objects.filter(session=session, semester=semester)
        tea = faculty.objects.get(email=request.POST['teacher'])
        oa = SemesterBill.objects.filter(
            session=session, semester=semester, teacher=tea)
        if not oa:
            no = SemesterBill(session=session, semester=semester, teacher=tea)
            no.save()
        ca = SemesterBill.objects.get(
            session=session, semester=semester, teacher=tea)
        val = request.POST['role']
        if val == "1":
            ca.moderator = 1
        elif val == "2":
            ca.translator = 1
        elif val == "3":
            ca.typist = 1
        ca.save()
        response = '/viewSem/'+str(id)+'/'+str(id2)
        return redirect(response)
    return render(request, 'addRole.html', cont)


def createSem(request, id):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.filter(session=session)

    class Class:
        def __init__(self, qd, st):
            self.qd = qd
            self.st = st
            if qd.semId == 1:
                st = "1st Year 1st Semseter"
            if qd.semId == 2:
                st = "1st Year 2nd Semseter"
            if qd.semId == 3:
                st = "2nd Year 1st Semseter"
            if qd.semId == 4:
                st = "2nd Year 2nd Semseter"
            if qd.semId == 5:
                st = "3rd Year 1st Semseter"
            if qd.semId == 6:
                st = "3rd Year 2nd Semseter"
            if qd.semId == 7:
                st = "4th Year 1st Semseter"
            if qd.semId == 8:
                st = "4th Year 2nd Semseter"
            if qd.semId == 9:
                st = "Masters 1st Semseter"
            if qd.semId == 10:
                st = "Masters 2nd Semseter"
            self.st = st
    ar = []
    for o in semester:
        a = Class(qd=o, st=" ")
        ar.append(a)

    cont = {
        'ob': ar,
        'session': id
    }
    return render(request, 'createSem.html', cont)


def createCourse(request, id, id2):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    ob = faculty.objects.filter()
    cont = {'ob': ob,
            'session':session.year,
            'semester':semester.semId
            }
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        code = int(code)
        credit = request.POST['credit']
        credit = int(code)
        type = request.POST['type']
        type = int(type)
        if type == 1 or type == 2:
            internal = faculty.objects.get(email=request.POST['internal'])
            external = faculty.objects.get(email=request.POST['external'])
        course = Course.objects.filter(
            session=session, semester=semester, courseCode=int(code))
        if not course:
            if type == 1 or type == 2:
                oa = Course(session=session, semester=semester, courseName=name, courseCode=code, credit=credit,
                            type=type, internal=internal, external=external)
                oa.save()
            else:
                oa = Course(session=session, semester=semester,
                            courseName=name, courseCode=code, credit=credit, type=type)
                oa.save()
            messages.success(
                request, 'Course Created Successfully !!', extra_tags='success')
        else:
            messages.error(request, 'Course Already Exists',
                           extra_tags='error')
    return render(request, 'createCourse.html', cont)


def viewCourse(request, id, id2):
    tea = faculty.objects.get(email=request.user.email)
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    course = Course.objects.filter(session=session, semester=semester)
    flag = False
    if tea == semester.chairman:
        flag = True
    cont = {"ob": course,
            'flag': flag,
            'session': id,
            'semester': id2
            }
    if 'add' in request.POST:
        response = '/createCourse/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'update' in request.POST:
        response = '/updateCourse/' + \
            str(id)+'/'+str(id2)+'/'+str(request.POST['update'])
        return redirect(response)
    if 'delete' in request.POST:
        print('ok')
        co = Course.objects.get(
            session=session, semester=semester, courseCode=int(request.POST['delete']))
        co.delete()
        response = '/viewCourse/' + \
            str(id)+'/'+str(id2)
        return redirect(response)
    return render(request, 'viewCourse.html', cont)


def updateCourse(request, id, id2, id3):

    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    ob = faculty.objects.filter()
    theory = False
    lab = False
    viva = False
    course = Course.objects.get(
        session=session, semester=semester, courseCode=int(id3))
    extra = courseBill.objects.filter(
        session=session, semester=semester, course=course)

    if course.type == 1:
        theory = True
    elif course.type == 2:
        lab = True
    elif course.type == 3:
        viva = True
    ex = External.objects.filter()
    cont = {
        'session':id,
        'semester':id2,
        'id3':id3,
        'ob': ob,
        'theory': theory,
        'lab': lab,
        'viva': viva,
        'course': course,
        'extra': extra,
        'ex': ex
    }
    if 'theory' in request.POST:
        internal = faculty.objects.get(email=request.POST.get('internal'))
        external = faculty.objects.get(email=request.POST.get('external'))
        third = faculty.objects.get(email=request.POST.get('third'))
        paperNo = request.POST['paperNo']
        tPaperNo = request.POST['tpaperNo']
        course.internal = internal
        course.external = external
        course.thirdExaminer = third
        course.paperNo = paperNo
        course.tPaperNo = tPaperNo
        course.save()
        response = '/viewCourse/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'lab' in request.POST:
        internal = faculty.objects.get(email=request.POST.get('internal'))
        external = faculty.objects.get(email=request.POST.get('external'))
        duration = request.POST['duration']
        course.internal = internal
        course.external = external
        course.duration = duration
        course.save()
        response = '/viewCourse/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'viva' in request.POST:
        external = External.objects.get(email=request.POST.get('external'))
        duration = request.POST['duration']
        course.vivaExternal = external
        course.duration = duration
        course.save()
        response = '/viewCourse/'+str(id)+'/'+str(id2)
        return redirect(response)
    if 'invigilator' in request.POST:
        response = '/addInvigilator/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(response)

    return render(request, 'updateCourse.html', cont)


def addInvigilator(request, id, id2, id3):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    course = Course.objects.get(
        session=session, semester=semester, courseCode=int(id3))
    ob = faculty.objects.filter()
    ex = External.objects.filter()
    cont = {'ob': ob, }
    if 'add' in request.POST:
        tea = faculty.objects.get(email=request.POST['invigilator'])
        oo = courseBill(session=session, semester=semester,
                        course=course, extra=tea)
        oo.save()
        response = '/updateCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(response)
    return render(request, 'addInvigilator.html', cont)


def indCourse(request, id, id2, id3):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    course = Course.objects.get(
        session=session, semester=semester, courseCode=int(id3))
    theory = False
    viva = False
    lab = False
    if course.type == 1:
        theory = True
    if course.type == 2:
        lab = True
    if course.type == 3:
        viva = True
    extra = courseBill.objects.filter(
        session=session, semester=semester, course=course)

    cont = {
        'course': course,
        'theory': theory,
        'viva': viva,
        'lab': lab,
        'extra': extra
    }
    return render(request, 'indCourse.html', cont)
def deleteCourse(request, id, id2, id3):
    return render(request, 'deleteCourse.html')


def examBill(request):
    if request.method == 'POST':
        session = Session.objects.filter(year=int(request.POST['session']))
        flag = False
        if not session:
            flag = True
        else:
            session = Session.objects.get(year=int(request.POST['session']))
            semester = Semester.objects.filter(
                session=session, semId=int(request.POST['semester']))
            if not semester:
                flag = True
        if flag:
            messages.error(
                request, 'Session Or Semester Does not Exist !!', extra_tags='nn')
        else:
            response = '/indBill/' + \
                request.POST['session']+'/' + \
                request.POST['semester']+'/'+str(request.user.id)
            return redirect(response)
    return render(request, 'examBill.html')


def indBill(request, id, id2, id3):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    fac = faculty.objects.get(email=request.user.email)
    course = Course.objects.filter(session=session, semester=semester)
    semBill = SemesterBill.objects.filter(session=session, semester=semester)
    thesPaper=ThesisPaper.objects.filter(session=session,semester=semester)
    thesSupervisor=ThesisSupervisor.objects.filter(session=session,semester=semester)
    class bill:
        def __init__(self, role, courseCode, courseName,  paperNo, duration,bill,st):
            self.role = role
            self.courseCode = courseCode
            self.courseName = courseName
            self.paperNo = paperNo
            self.duration = duration
            self.bill=bill
            self.st=st
    ar = []
    if semester.chairman == fac:
        p = bill(role="Chairman", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0,bill=2700,st=0)
        ar.append(p)
    if semester.tabular1 == fac or semester.tabular2 == fac:
        tk=0
        if semester.semId>=1 and semester.semId<=3:
            tk=2500
        else:
            tk=3125
        p = bill(role="Tabulation", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0,bill=tk,st=0)
        ar.append(p)
    for o in thesPaper:
        if o.faculty==fac:
            if o.paperNo>0:
                p=bill(role='Thesis Paper Evaluation',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.paperNo,duration=0,bill=o.paperNo*1250,
                       st=0
                       )
                ar.append(p)
    for o in thesSupervisor:
        if o.faculty==fac:
            if o.studentNo>0:
                p=bill(role='Thesis Supervisor',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.studentNo,duration=0,
                       bill=o.studentNo*3100,st=0
                       )
                ar.append(p)
    
    for o in semBill:
        if o.teacher == fac:
            if o.moderator == 1:
                p = bill(role="Moderation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=2150,st=len(course)-1)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.translator == 1:
                p = bill(role="Translation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=400,st=len(course-1))
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.typist == 1:
                p = bill(role="Stencil-Cutter", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=375,st=o.paperNo)
                ar.append(p)

    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0,bill=2150,st=1)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0,bill=2150,st=1)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.thirdExaminer == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.tPaperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=o.duration,bill=15000,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Viva", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*200,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Lab Invigilator", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*400,st=0)
                    ar.append(p)
    for o in course:
        if o.type == 3:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Viva-Voce", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*200,st=0)
                    ar.append(p)
    aa = int(id2)
    ca = int((aa+1)/2)
    ss = ""
    if ca == 1:
        ss += "1st Year "
    elif ca == 2:
        ss += "2nd Year "
    elif ca == 3:
        ss += "3rd Year "
    elif ca == 4:
        ss += "4th Year "
    if aa == 1:
        ss += "1st Semester"
    elif aa == 2:
        ss += "2nd Semester"
    total=0
    for o in ar:
        total+=o.bill
    cont = {
        'ob': ar,
        'name': fac,
        'session': id,
        'ss': ss,
        'total':total
    }
    if 'pdf' in request.POST:
        res='/pdf_view/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(res)
    return render(request, 'indBill.html', cont)
def pdf_view(request,id,id2,id3):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    fac = faculty.objects.get(email=request.user.email)
    course = Course.objects.filter(session=session, semester=semester)
    semBill = SemesterBill.objects.filter(session=session, semester=semester)
    thesPaper=ThesisPaper.objects.filter(session=session,semester=semester)
    thesSupervisor=ThesisSupervisor.objects.filter(session=session,semester=semester)
    class bill:
        def __init__(self, role, courseCode, courseName,  paperNo, duration,bill,st):
            self.role = role
            self.courseCode = courseCode
            self.courseName = courseName
            self.paperNo = paperNo
            self.duration = duration
            self.bill=bill
            self.st=st
    ar = []
    if semester.chairman == fac:
        p = bill(role="Chairman", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0,bill=2700,st=0)
        ar.append(p)
    if semester.tabular1 == fac or semester.tabular2 == fac:
        tk=0
        if semester.semId>=1 and semester.semId<=3:
            tk=2500
        else:
            tk=3125
        p = bill(role="Tabulation", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0,bill=tk,st=0)
        ar.append(p)
    for o in thesPaper:
        if o.faculty==fac:
            if o.paperNo>0:
                p=bill(role='Thesis Paper Evaluation',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.paperNo,duration=0,bill=o.paperNo*1250,
                       st=0
                       )
                ar.append(p)
    for o in thesSupervisor:
        if o.faculty==fac:
            if o.studentNo>0:
                p=bill(role='Thesis Supervisor',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.studentNo,duration=0,
                       bill=o.studentNo*3100,st=0
                       )
                ar.append(p)
    
    for o in semBill:
        if o.teacher == fac:
            if o.moderator == 1:
                p = bill(role="Moderation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=2150,st=o.paperNo)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.translator == 1:
                p = bill(role="Translation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=400,st=o.paperNo)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.typist == 1:
                p = bill(role="Stencil-Cutter", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0,bill=375,st=o.paperNo)
                ar.append(p)

    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0,bill=2150,st=1)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0,bill=2150,st=1)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.thirdExaminer == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.tPaperNo, duration=0,bill=o.paperNo*115,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=o.duration,bill=15000,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Viva", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*200,st=0)
            ar.append(p)
    for o in course:
        if o.type == 2:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Lab Invigilator", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*400,st=0)
                    ar.append(p)
    for o in course:
        if o.type == 3:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Viva-Voce", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration,bill=o.duration*200,st=0)
                    ar.append(p)
    aa = int(id2)
    ca = int((aa+1)/2)
    ss = ""
    if ca == 1:
        ss += "1st Year "
    elif ca == 2:
        ss += "2nd Year "
    elif ca == 3:
        ss += "3rd Year "
    elif ca == 4:
        ss += "4th Year "
    if aa == 1:
        ss += "1st Semester"
    elif aa == 2:
        ss += "2nd Semester"
    elif aa==3:
        ss+='3rd Semester'
    else:
        ss+=str(id2)+"th Semester" 
    total=0
    for o in ar:
        total+=o.bill
    cont = {
        'ob': ar,
        'name': fac,
        'session': id,
        'ss': ss,
        'total':total
    }
    template_path='pdf_view.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="bill.pdf"'
    template = get_template(template_path)
    html = template.render(cont)    
    pisa_status = pisa.CreatePDF(
       html, dest=response )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def examBill2(request):
    if request.method == 'POST':
        session = Session.objects.filter(year=int(request.POST['session']))
        flag = False
        if not session:
            flag = True
        else:
            session = Session.objects.get(year=int(request.POST['session']))
            semester = Semester.objects.filter(
                session=session, semId=int(request.POST['semester']))
            if not semester:
                flag = True
        if flag:
            messages.error(
                request, 'Session Or Semester Does not Exist !!', extra_tags='nn')
        else:
            ca = faculty.objects.get(email=request.user.email)
            da = faculty.objects.get(email="chairman@gmail.com")
            semester = Semester.objects.get(
                session=session, semId=int(request.POST['semester']))
            if not (ca == semester.chairman or da == ca):
                flag = True
            if flag:
                messages.error(request, 'Access Denied !!', extra_tags='chair')
            else:
                response = '/semBill/' + \
                    request.POST['session']+'/' + \
                    request.POST['semester']+'/'
                return redirect(response)
    return render(request, 'examBill2.html')


class bill:
    def __init__(self, teacher,  role, courseCode, courseName,  paperNo, duration):
        self.role = role
        self.courseCode = courseCode
        self.courseName = courseName
        self.paperNo = paperNo
        self.duration = duration
        self.teacher = teacher


def cal(id, id2, f):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    fac = faculty.objects.get(email=f.email)
    course = Course.objects.filter(session=session, semester=semester)
    semBill = SemesterBill.objects.filter(session=session, semester=semester)

    ar = []
    if semester.chairman == fac:
        p = bill(teacher=fac.email, role="Chairman", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0)
        ar.append(p)
    if semester.tabular1 == fac or semester.tabular2 == fac:
        p = bill(teacher=fac.email, role="Tabulation", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0)
        ar.append(p)

    for o in semBill:
        if o.teacher == fac:
            if o.moderator == 1:
                p = bill(teacher=fac.email, role="Moderation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.translator == 1:
                p = bill(teacher=fac.email, role="Translation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.typist == 1:
                p = bill(teacher=fac.email, role="Stencil-Cutter", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)

    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(teacher=fac.email, role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(teacher=fac.email, role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(teacher=fac.email, role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(teacher=fac.email, role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.thirdExaminer == fac:
            p = bill(teacher=fac.email, role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.tPaperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(teacher=fac.email, role="Lab Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=o.duration)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(teacher=fac.email, role="Lab Viva", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=o.duration)
            ar.append(p)
    for o in course:
        if o.type == 2:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(teacher=fac.email, role="Lab Invigilator", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration)
                    ar.append(p)
    for o in course:
        if o.type == 3:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(teacher=fac.email, role="Viva-Voce", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration)
                    ar.append(p)
    return ar

def semBill(request, id, id2):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    ex = faculty.objects.filter()
    a = []
    ob = []
    for o in ex:
        b = cal(id, id2, o)
        if len(b) > 0:
            a.append(b[0].teacher)
    for o in a:
        oo = faculty.objects.get(email=o)
        ob.append(oo)
    aa=int(id2)
    ss=""
    if aa == 1:
        ss += "1st Semester"
    elif aa == 2:
        ss += "2nd Semester"
    elif aa==3:
        ss+='3rd Semester'
    else:
        ss+=str(id2)+"th Semester" 
    cont = {
        'ob': ob,
        'semester':ss
    }

    if request.method == 'POST':
        aa = request.POST.get('teacher')
        bb = -111
        oo = faculty.objects.get(email=aa)
        response = '/indBill2/'+str(id)+'/'+str(id2)+'/'+str(oo.id)
        return redirect(response)

    return render(request, 'semBill.html', cont)


def indBill2(request, id, id2, id3):
    session = Session.objects.get(year=int(id))
    semester = Semester.objects.get(session=session, semId=int(id2))
    fac = faculty.objects.get(id=int(id3))
    course = Course.objects.filter(session=session, semester=semester)
    semBill = SemesterBill.objects.filter(session=session, semester=semester)
    thesPaper=ThesisPaper.objects.filter(session=session,semester=semester)
    thesSupervisor=ThesisSupervisor.objects.filter(session=session,semester=semester)
    class bill:
        def __init__(self, role, courseCode, courseName,  paperNo, duration):
            self.role = role
            self.courseCode = courseCode
            self.courseName = courseName
            self.paperNo = paperNo
            self.duration = duration
    ar = []
    if semester.chairman == fac:
        p = bill(role="Chairman", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0)
        ar.append(p)
    if semester.tabular1 == fac or semester.tabular2 == fac:
        p = bill(role="Tabulation", courseCode=0,
                 courseName="CSE", paperNo=0, duration=0)
        ar.append(p)
    for o in thesPaper:
        if o.faculty==fac:
            if o.paperNo>0:
                p=bill(role='Thesis Paper Evaluation',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.paperNo,duration=0
                       )
                ar.append(p)
    for o in thesSupervisor:
        if o.faculty==fac:
            if o.studentNo>0:
                p=bill(role='Thesis Supervisor',courseCode=o.course.courseCode,
                       courseName='CSE',paperNo=o.studentNo,duration=0
                       )
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.moderator == 1:
                p = bill(role="Moderation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.translator == 1:
                p = bill(role="Translation", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)
    for o in semBill:
        if o.teacher == fac:
            if o.typist == 1:
                p = bill(role="Stencil-Cutter", courseCode=0,
                         courseName="CSE", paperNo=len(course)-1, duration=0)
                ar.append(p)

    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Question-Paper Formulation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.internal == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.external == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 1 and o.thirdExaminer == fac:
            p = bill(role="Paper Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.tPaperNo, duration=0)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Evaluation", courseCode=o.courseCode,
                     courseName="CSE", paperNo=o.paperNo, duration=o.duration)
            ar.append(p)
    for o in course:
        if o.type == 2 and (o.internal == fac or o.external == fac):
            p = bill(role="Lab Viva", courseCode=o.courseCode,
                     courseName="CSE", paperNo=0, duration=o.duration)
            ar.append(p)
    for o in course:
        if o.type == 2:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Lab Invigilator", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration)
                    ar.append(p)
    for o in course:
        if o.type == 3:
            ex = courseBill.objects.filter(
                session=session, semester=semester, course=o)
            for i in ex:
                if ex.extra == fac:
                    p = bill(role="Viva-Voce", courseCode=o.courseCode,
                             courseName="CSE", paperNo=0, duration=o.duration)
                    ar.append(p)
    aa = int(id2)
    ca = int((aa+1)/2)
    ss = ""
    if ca == 1:
        ss += "1st Year "
    elif ca == 2:
        ss += "2nd Year "
    elif ca == 3:
        ss += "3rd Year "
    elif ca == 4:
        ss += "4th Year "
    if aa == 1:
        ss += "1st Semester"
    elif aa == 2:
        ss += "2nd Semester"
    cont = {
        'ob': ar,
        'name': fac,
        'session': id,
        'ss': ss
    }
    return render(request, 'indBill.html', cont)
def thesis(request,id,id2,id3):
    session=Session.objects.get(year=int(id))
    semester=Semester.objects.get(session=session,semId=int(id2))
    course=Course.objects.get(session=session,semester=semester,courseCode=int(id3))
    tec=faculty.objects.filter().order_by('name')
    tea=ThesisPaper.objects.filter(session=session,semester=semester,course=course)
    if not tea:
        for o in tec:
            cc=ThesisPaper(
                session=session,semester=semester,course=course,
                faculty=faculty.objects.get(email=o.email)
            )
            cc.save()
    ff=ThesisPaper.objects.filter(session=session,semester=semester,course=course)
    if 'save' in request.POST:
        for o,i in zip(request.POST.getlist('paper'),ff):
            dd=ThesisPaper.objects.get(
                session=session,semester=semester,course=course,
                faculty=faculty.objects.get(email=i.faculty.email)
            )
            dd.paperNo=int(o)
            dd.save()
        res='/updateCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(res)
    if 'cancel' in request.POST:
        res='/updateCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(res)

    cont={

        'session':session.year,
        'semester':semester.semId,
        'tea':ff
    }
    return render(request,'thesis.html',cont)
def supervising(request,id,id2,id3):
    session=Session.objects.get(year=int(id))
    semester=Semester.objects.get(session=session,semId=int(id2))
    course=Course.objects.get(session=session,semester=semester,courseCode=int(id3))
    tec=faculty.objects.filter().order_by('name')
    tea=ThesisSupervisor.objects.filter(session=session,semester=semester,course=course)
    if not tea:
        for o in tec:
            cc=ThesisSupervisor(
                session=session,semester=semester,course=course,
                faculty=faculty.objects.get(email=o.email)
            )
            cc.save()
    ff=ThesisSupervisor.objects.filter(session=session,semester=semester,course=course)
    if 'save' in request.POST:
        for o,i in zip(request.POST.getlist('student'),ff):
            dd=ThesisSupervisor.objects.get(
                session=session,semester=semester,course=course,
                faculty=faculty.objects.get(email=i.faculty.email)
            )
            dd.studentNo=int(o)
            dd.save()
        res='/updateCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(res)
    if 'cancel' in request.POST:
        res='/updateCourse/'+str(id)+'/'+str(id2)+'/'+str(id3)
        return redirect(res)

    cont={

        'session':session.year,
        'semester':semester.semId,
        'tea':ff
    }
    return render(request,'supervising.html',cont)