from django.shortcuts import render, render_to_response
from events.models import Event, Attendance
from django.template import RequestContext
from events.forms import EventForm
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def tonight(request):
	events = Event.objects.today().filter(latest=True)
	attending = []
	for event in events:
		try:
			Attendance.objects.get(event=event, user=request.user)
			attending.append(True)
		except Attendance.DoseNotExist:
			attending.append(False)

	context = {
		'events': zip(events, attending),
	}
	return render_to_response(
		'events/tonight.html',
		context,
		context_instance = RequestContext(request),
	)
@login_required
def create(request):
	form = EventForm(request.POST or None)
	if form.is_valid():
		event = form.save(commit=False)
		event.creator = request.user
		guessed_date = None
		for word in event.description.split():
			try:
				guessed_date = parse(word)
				break
			except ValueError:
				pass
		event.start_date = guessed_date
		event.save()
		
		messages.success(request, 'Your event was posted')
		if 'next' in request.POST:
			next = request.POST['next']
		else:
			next = reverse('ev_tonight')
		return HttpResponseRedirect(next)
	return render_to_response(
		'events/create.html',
		{'form':form},
		context_instance = RequestContext(request)
	)
create = login_required(create)
