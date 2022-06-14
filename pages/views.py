from zoneinfo import available_timezones
from django.shortcuts import render


from watch.models import Watch

def shortenString(product):
    if len(product.description) > 40:
        return product.description[:40] + '...'
    else:
        return product.description

# Create your views here.
def home_view(request, *args, **kwargs):

    if request.method == 'POST':
        q = request.POST['q']
        products = Watch.objects.filter(title__icontains=q)
    else:
        products = Watch.objects.all()
        
    productsList = list(products)
    for product in productsList:
        if product.availableItems < 1:
            productsList.remove(product)

    shortDescriptions = map(shortenString, productsList)


    shortDescriptionsList = list(shortDescriptions)

    for i in range(len(productsList)):
        productsList[i].description = shortDescriptionsList[i]

    print(productsList)

    context = {'products': productsList,
               'descriptions': list(shortDescriptions)} 
    return render(request, "pages/home.html", context)

def about_view(request, *args, **kwargs): 
    return render(request, "pages/about.html", {})

def contact_view(request, *args, **kwargs): 
    return render(request, "pages/contact.html", {})