from django.shortcuts import redirect, render
from .models import Search

# Create your views here.
def handleAdd(request):
    #s = Search.objects.all()

    if request.method == 'POST':
        new_item = Search(
            query = request.POST['searchBar']
        )
        new_item.save()
        return redirect('/') #homepage

    #return render(request, 'index.html', {'to_add': s})