from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Ref, get_ref_from_doi
from .utils import canonicalize_doi
from .forms import RefForm

def edit(request, pk=None):
    c = {'pk': pk if pk else ''}
    if request.method == 'POST':
        ref = None
        if pk:
            ref = Ref.objects.get(pk=pk)
        form = RefForm(request.POST, instance=ref)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/refs/')
    else:
        try:
            ref = Ref.objects.get(pk=pk)
        except Ref.DoesNotExist:
            ref = None
        form = RefForm(instance=ref)

    c['form'] = form
    return render(request, 'refs/edit.html', c)

def resolve(request, pk=None):
    # Look up DOI and pre-populate form, render to refs/add.html
    if request.method == 'GET':
        doi = request.GET.get('doi')
        doi = canonicalize_doi(doi)
        if not pk:
            try:
                # We're trying to add a reference but one with the same DOI
                # is in the database already.
                ref = Ref.objects.get(doi=doi)
                return HttpResponseRedirect(f'/refs/edit/{ref.pk}')
            except Ref.DoesNotExist:
                ref = None
        else:
            ref = get_object_or_404(Ref, pk=pk)
        ref = get_ref_from_doi(doi, ref)
        form = RefForm(instance=ref)
        c = {'form': form, 'pk': pk if pk else ''}
       # return edit(request, pk=pk)
       # url = reverse('ref:edit', kwargs={'pk': pk})
        return render(request, 'refs/edit.html', c)
    raise Http404

def ref_list(request):
    refs = Ref.objects.all()
    c = {'refs': refs}
    return render(request, 'refs/refs-list.html', c)

def delete(request, pk):
    ref = get_object_or_404(Ref, pk=pk)
    ref.delete()
    return HttpResponseRedirect('/refs/')
