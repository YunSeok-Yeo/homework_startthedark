from django.shortcuts import render, render_to_response, get_object_or_404
from events.models import Event, Attendance
from django.template import RequestContext
from events.forms import EventForm
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def tonight(request):
	events = Event.objects.today().filter(latest=True)
	context = {
		'events': events,
	}
	return render_to_response(
                'events/tonight.html',
                RequestContext(request, context),
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
		RequestContext(request, {'form':form})
	)
create = login_required(create)

@login_required
def toggle_attendance(request):
	try:
		event_id = int(request.POST['event_id'])
	except (KeyError, ValueError):
		raise Http404
	event = get_object_or_404(Event, id=event_id);
	attendance, created = Attendance.objects.get_or_create(user=request.user, event=event)
	if created:
		messages.success(request, "you are now attending '%s'", event)
		#request.user.message_set.create(message="you are now attending '%s'", event)
	else:
		attendance.delete()
		messages.success(request, "you are no longer attending '%s'", event)
		#request.user.message_set.create(message="you are no longer attending '%s'", event)

	if 'next' in request.POST:
		next = request.POST['next']
	else:
		next = reverse('ev_tonight')
	return HttpResponseRedirect(next)


toggle_attendance = login_required(toggle_attendance)


def archive(request):
        events = Event.objects.filter(latest=True)
        context = {
                'events': events,
        }
        return render_to_response(
                'events/archive.html',
                RequestContext(request, context),
        )
