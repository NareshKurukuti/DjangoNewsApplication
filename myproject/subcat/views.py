from django.shortcuts import render, get_object_or_404, redirect
from .models import SubCat
from cat.models import Cat

# Create your views here.
def subcat_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    
    subcat = SubCat.objects.all()

    return render(request, 'back/subcat_list.html',{'subcat':subcat})


def subcat_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    
    cat_list = Cat.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        catid = request.POST.get('cat')

        if name =="" or catid =="":
            error = "All fields are required"
            return render(request, 'back/error.html', {'error':error})
        else:
            if len(SubCat.objects.filter(name=name)) !=0:
                error = "This SubCategory Already added."
                return render(request, 'back/error.html', {'error':error})
            else:
                category = Cat.objects.get(pk=catid)
                print(category)
                b = SubCat(name=name, category_name=category.name, category_id=catid)
                b.save()

            return redirect('subcat_list')

    return render(request, 'back/subcat_add.html',{'cat_list':cat_list})

def subcat_delete(request,pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    
    try:
        b = SubCat.objects.get(pk=pk)
        b.delete()
    except:
        error = "Something Went Wrong.."
        return render(request, 'back/error.html', {'error':error})

    return redirect('subcat_list')