from django.shortcuts import render
from  .models import Topic, Entry
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TopicForm, EntryForm


# Create your views here.


def index(request):
    return render(request, 'learnin_logs/index.html')

def topics(request):
    topics = Topic.objects.order_by('date_aded')
    context = {'topics': topics}
    return render(request, 'learnin_logs/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_aded')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learnin_logs/topic.html', context)

def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('topics'))

    context = {'form' : form}
    return render(request, 'learnin_logs/new_topic.html', context)

def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
    if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()
        return HttpResponseRedirect(reverse('index'))
    context = {'topic':topic, 'form':form}
    return render(request, 'learnin_logs/new_entry.html', context)

def edit_entry(request, id_entry):
    entry = Entry.objects.get(id=id_entry)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'learnin_logs/edit_entry.html', context)

