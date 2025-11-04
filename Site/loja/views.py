from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'./loja/static/html/index.html')
def produto(request):
    return render(request,'./loja/static/html/produto.html')