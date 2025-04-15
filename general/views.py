from django.shortcuts import render

# View for the home page
def index(request):
    context = {}
    return render(request, "general/index.html", context)

# View for the contact page
def contact(request):
    context = {}
    return render(request, "general/contact.html", context)

# View for the about page
def about(request):
    context = {}
    return render(request, "general/about.html", context)
