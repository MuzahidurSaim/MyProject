from django.shortcuts import render

# Create your views here.

# grader/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        num_mcqs = request.POST.get('num_mcqs')
        if num_mcqs and num_mcqs.isdigit() and int(num_mcqs) > 0:
            request.session['num_mcqs'] = int(num_mcqs)
            return redirect('enter_correct_answers')
        else:
            messages.error(request, "Please enter a valid positive integer.")
    return render(request, 'index.html')


def enter_correct_answers(request):
    num_mcqs = request.session.get('num_mcqs')
    if num_mcqs is None:
        return redirect('index')

    if request.method == 'POST':
        correct_answers = []
        for i in range(1, num_mcqs + 1):
            answer = request.POST.get(f'answer_{i}').strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                correct_answers.append(answer)
            else:
                messages.error(request, f"Invalid input for Question {i}. Use A, B, C, or D.")
                return render(request, 'enter_correct_answers.html', {'num_mcqs': range(1, num_mcqs + 1)})
        request.session['correct_answers'] = correct_answers
        return redirect('enter_num_students')

    return render(request, 'enter_correct_answers.html', {'num_mcqs': range(1, num_mcqs + 1)})


def enter_num_students(request):
    if 'correct_answers' not in request.session:
        return redirect('index')

    if request.method == 'POST':
        num_students = request.POST.get('num_students')
        if num_students and num_students.isdigit() and int(num_students) > 0:
            request.session['num_students'] = int(num_students)
            request.session['current_student'] = 1
            request.session['students'] = []
            return redirect('enter_student_answers')
        else:
            messages.error(request, "Please enter a valid positive integer.")
    return render(request, 'enter_num_students.html')


def enter_student_answers(request):
    num_mcqs = request.session.get('num_mcqs')
    num_students = request.session.get('num_students')
    current_student = request.session.get('current_student')

    if None in (num_mcqs, num_students, current_student):
        return redirect('index')

    if request.method == 'POST':
        roll_no = request.POST.get('roll_no').strip()
        answers = []
        for i in range(1, num_mcqs + 1):
            answer = request.POST.get(f'answer_{i}').strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                answers.append(answer)
            else:
                messages.error(request, f"Invalid input for Question {i}. Use A, B, C, or D.")
                context = {
                    'student_number': current_student,
                    'num_mcqs': range(1, num_mcqs + 1),
                }
                return render(request, 'enter_student_answers.html', context)

        students = request.session.get('students', [])
        students.append({'roll_no': roll_no, 'answers': answers})
        request.session['students'] = students
        request.session['current_student'] = current_student + 1

        if current_student < num_students:
            return redirect('enter_student_answers')
        else:
            return redirect('show_results')

    context = {
        'student_number': current_student,
        'num_mcqs': range(1, num_mcqs + 1),
    }
    return render(request, 'enter_student_answers.html', context)


def show_results(request):
    if 'students' not in request.session or 'correct_answers' not in request.session:
        return redirect('index')

    correct_answers = request.session['correct_answers']
    students = request.session['students']
    results = []

    for student in students:
        score = sum(
            1 for ca, sa in zip(correct_answers, student['answers']) if ca == sa
        )
        results.append({'roll_no': student['roll_no'], 'score': score})

    context = {'results': results}
    # Clear session data after displaying results
    for key in ['num_mcqs', 'correct_answers', 'num_students', 'current_student', 'students']:
        request.session.pop(key, None)

    return render(request, 'show_results.html', context)
