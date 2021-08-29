from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import DevelopmentDiscussionForm, DevelopmentDiscussionAnswerForm
from .models import (
    DevelopmentDiscussion, DevelopmentDiscussionAnswer, DevelopmentIteration, DevelopmentProject
)


def home(request):

    # CHECK AUTH
    if not request.user.is_authenticated:
        return redirect('exarth:login')

    # CHECK PROJECT
    project = DevelopmentProject.objects.first()
    if not project:
        project = DevelopmentProject.objects.create()

    iterations = DevelopmentIteration.objects.all()
    context = {
        'iterations': iterations,
        'project': project
    }
    return render(request=request, template_name='home.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('exarth:login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('exarth:status')

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('exarth:status')
    else:
        form = AuthenticationForm
    return render(request=request, template_name='login.html', context={'form': form})


""" ------------------------------------------------------------------------------------"""


@login_required
def discussions(request):
    context = {
        'discussions_me': DevelopmentDiscussion.objects.filter(started_by=request.user).values('pk', 'description'),
        'discussions_all': DevelopmentDiscussion.objects.exclude(started_by=request.user).values('pk', 'description'),
        'discussions': DevelopmentDiscussion.objects.all()
    }
    return render(request=request, template_name='discussions.html', context=context)


@login_required
def discussion(request, discussion_id):
    try:
        dis = DevelopmentDiscussion.objects.get(pk=discussion_id)
        discussion_answers = DevelopmentDiscussionAnswer.objects.filter(discussion=dis)
        context = {
            'discussion': dis,
            'discussion_answers': discussion_answers,
            'total_answers': discussion_answers.count()
        }
        return render(request=request, template_name='discussion.html', context=context)
    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested discussion {discussion_id} Doesn't Exists")
        redirect('exarth:discussions')


@login_required
def add_discussion(request):
    method = request.method
    if method == 'POST':
        form = DevelopmentDiscussionForm(request.POST)
        if form.is_valid():
            success = form.save(commit=True)
            success.started_by = request.user
            success.save()

            messages.success(
                request=request,
                message=f"Hi Mr {request.user.username}! Your Question submitted Successfully"
            )

            return redirect('exarth:discussion', success.pk)
    else:
        form = DevelopmentDiscussionForm()
    context = {
        'form': form
    }

    return render(request=request, template_name='add_discussion.html', context=context)


@login_required
def update_discussion(request, discussion_id):

    try:
        question = DevelopmentDiscussion.objects.get(pk=discussion_id)

        if question.started_by != request.user:
            messages.error(request, f"You are not allowed to update this discussion")
            return redirect('exarth:discussions')
    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested Question {discussion_id} Doesn't Exists")
        return redirect('exarth:discussions')

    method = request.method
    if method == 'POST':
        form = DevelopmentDiscussionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, f"Requested Question {discussion_id} updated Successfully")
            return redirect('exarth:discussion', discussion_id)
    else:
        form = DevelopmentDiscussionForm(instance=question)

    context = {
        'form': form,
        'id': discussion_id
    }

    return render(request=request, template_name='update_discussion.html', context=context)


@login_required
def delete_discussion(request, discussion_id):
    question = None
    try:
        question = DevelopmentDiscussion.objects.get(pk=discussion_id)

        if question.started_by != request.user:
            messages.error(request, f"You are now allowed to end this discussion")
        else:
            question.delete()
            messages.success(request, f"Your discussion deleted successfully")

    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested Question {discussion_id} Doesn't Exists")

    return redirect('exarth:discussions')


@login_required
def add_answer(request, discussion_id):
    dis = None
    try:
        dis = DevelopmentDiscussion.objects.get(pk=discussion_id)
    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, "Requested discussion doesn't exists")

    method = request.method
    if method == 'POST':
        form = DevelopmentDiscussionAnswerForm(request.POST)
        if form.is_valid():
            success = form.save(commit=True)
            success.answer_by = request.user
            success.discussion = dis

            dis.is_answered = True
            dis.save()

            success.save()

            messages.success(
                request=request,
                message=f"Your Answer to this discussion submitted Successfully"
            )
            return redirect('exarth:discussion', discussion_id)
    else:
        form = DevelopmentDiscussionAnswerForm()
    context = {
        'post': False,
        'form': form
    }

    return render(request=request, template_name='update_discussion_answer.html', context=context)


@login_required
def update_answer(request, answer_id, discussion_id):

    try:
        answer = DevelopmentDiscussionAnswer.objects.get(pk=answer_id)
        question = DevelopmentDiscussionAnswer.objects.get(pk=answer_id)

        if answer.answer_by != request.user:
            messages.error(request, f"You are not allowed to update this answer")
            return redirect('exarth:discussions')

    except DevelopmentDiscussionAnswer.DoesNotExist:
        messages.error(request, f"Requested answer doesn't exists")
        return redirect('exarth:discussions')
    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested discussion doesn't exists")
        return redirect('exarth:discussions')

    method = request.method

    if method == 'POST':
        form = DevelopmentDiscussionAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your answer to this discussion updated Successfully")
            return redirect('exarth:discussion', discussion_id)
    else:
        form = DevelopmentDiscussionAnswerForm(instance=answer)

    context = {
        'post': True,
        'form': form,
        'answer_id': answer_id,
        'discussion_id': discussion_id
    }

    return render(request=request, template_name='update_discussion_answer.html', context=context)


@login_required
def delete_answer(request, answer_id, discussion_id):
    try:
        answer = DevelopmentDiscussionAnswer.objects.get(pk=answer_id)
        question = DevelopmentDiscussion.objects.get(pk=discussion_id)

        if answer.answer_by != request.user:
            messages.error(request, f"You are now allowed to delete this discussion")
        else:
            answer.delete()
            messages.success(request, f"Your answer to this discussion "
                                      f"deleted successfully")

    except DevelopmentDiscussionAnswer.DoesNotExist:
        messages.error(request, f"Requested answer doesn't exists")
    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested discussion doesn't exists")

    return redirect('exarth:discussion', discussion_id)


@login_required
def satisfied_discussion(request, discussion_id):
    try:
        question = DevelopmentDiscussion.objects.get(pk=discussion_id)
        answers = DevelopmentDiscussionAnswer.objects.filter(discussion=question)

        if question.started_by != request.user:
            messages.error(request, f"TFailed to satisfy this is not your discussion")
        else:
            if len(answers) < 1:
                messages.error(
                    request,
                    f"No one answered to this question how can this be satisfied - "
                    f"if you know the answer write it down or you can end this discussion"
                )
            else:
                question.is_satisfied = True
                question.save()
                messages.success(request, f"Your answer to this discussion "
                                      f"satisfied successfully")

    except DevelopmentDiscussion.DoesNotExist:
        messages.error(request, f"Requested discussion doesn't exists")
    return redirect('exarth:discussion', discussion_id)
