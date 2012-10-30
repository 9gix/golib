from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('catalog:book_list'))
    return render(request, 'index.html', {})
