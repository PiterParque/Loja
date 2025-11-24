from django.shortcuts import render,redirect
from .models import Produto,Categoria,Usuario


# Create your views here.
def index(request):
    produtos=Produto.objects.filter(ativo=True).order_by('-data_cadastro')
    return render(request,'./loja/static/html/index.html',{'produtos':produtos})
def produto(request,slug):
    produto_principal=Produto.objects.filter(slug=slug)
    id_categoria=produto_principal.values()[0]['categoria_id']
    produtos=Produto.objects.filter(categoria=id_categoria).order_by('-data_cadastro')
    return render(request,'./loja/static/html/produto.html',{'produtos':produtos,'produto_princiapl':produto_principal})

#------Perfil-------
def tela_logon(request):
    return render(request,'./loja/static/html/perfil/tela_logon.html')
def logon_validation(request):
    error=None
    if request.method == "POST":
        username = request.POST.get("username")
        password=request.POST.get("password")
        user= Usuario.objects.filter(nome=username, senha=password).first()
        if user :
            if user.tipo_usuario == "Admisnitrador":
                return redirect('administracao')
            request.session['usuario_id'] = user.id
            return redirect('perfil')
        else:
            error="Usuário ou senha incorretos."
    return render(request,'./loja/static/html/perfil/tela_logon.html',{'error':error})
def perfil(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/perfil.html')
def dados_pessoais(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/dados_pessoais.html')
def endereco(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/endereco.html')
def metodos_pagamento(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/metodos_pagamento.html')
def notificacao(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/notificacao.html')
def pedidos(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/pedidos.html')
def autenticacao(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect("tela_logon")
    user = Usuario.objects.get(id=usuario_id)
    return render(request,'./loja/static/html/perfil/autenticação.html')
#------------------
def administracao(request):
    return render(request,"./loja/static/html/administrador/administracao.html")
def usaurios(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    _usuarios=Usuario.objects.all().values()
    return render(request,"./loja/static/html/administrador/usuarios.html",{'usuarios':_usuarios})
def usuario(request,id):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    if id:
        _usuario=Usuario.objects.filter(id=id).first()
        

    return render(request,"./loja/static/html/administrador/usuario.html",{'usuario':_usuario})
def criar_usuario(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    return render(request,"./loja/static/html/administrador/usuario_criar.html")