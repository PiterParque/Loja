from django.shortcuts import render,redirect
from .models import Produto,Categoria,Usuario
from datetime import datetime,date

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
    _usuarios=Usuario.objects.all()
    _usuarios=_usuarios.values()
    for i,_usuario in enumerate(_usuarios):
        if isinstance(_usuario['data_nascimento'], date):
            ano,mes,dia=str(_usuarios[i]['data_nascimento']).split('-')
            _usuarios[i]['data_nascimento']=dia+"/"+mes+"/"+ano
      


    
    return render(request,"./loja/static/html/administrador/usuarios.html",{'usuarios':_usuarios})
def usuario(request,id):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).values()
    user=user[0]
    if isinstance(user['data_nascimento'], date):
     print(user['data_nascimento'])
     ano,mes,dia=str(user['data_nascimento']).split('')
     user['data_nascimento']=dia+"-"+mes+"-"+ano
    usuario_alterado=False
    mensagem="Falha em alterar o usuario"
    if user :
        if user['tipo_usuario'] != "Admisnitrador":
            redirect('perfil')
    if id:
        _usuario=Usuario.objects.filter(id=id).first()
    if request.method == "POST":
        nome=request.POST.get("usuario_nome")
        cpf=request.POST.get("usuario_cpf")
        data_nascimento=request.POST.get("usuario_nascimento")
        telefone=request.POST.get("usuario_telefone")
        genero = request.POST.get("genero")
        if genero == "OUTRO":
            genero = request.POST.get("outro_genero")
        tipo_usuario=request.POST.get("usuario_tipo")
        if isinstance(data_nascimento, date):
                ano,mes,dia=str(data_nascimento).split('-')
                data_nascimento=ano+"-"+mes+"-"+dia

        try:
            x=Usuario.objects.filter(id=id).update(
                nome=nome,
                CPF=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone,
                genero=genero,
                tipo_usuario=tipo_usuario
            )
            
            usuario_alterado=True
            mensagem="Usuario Alterado com Sucesso"
        except Exception as e:
            print("Erro:",e)

        

    return render(request,"./loja/static/html/administrador/usuario.html",{'usuario':_usuario,'usuario_alterado':usuario_alterado,"mensagem":mensagem})
def criar_usuario(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    usuario_criado=None
    if request.method == "POST":
        nome=request.POST.get("entrada_nome")
        cpf=request.POST.get("entrada_cpf")
        data_nascimento=request.POST.get("entrada_nascimento")
        senha=request.POST.get("entrada_senha")
        telefone=request.POST.get("entrada_telefone")
        genero = request.POST.get("genero")
        if genero == "OUTRO":
            genero = request.POST.get("entrada_outro_genero")
        tipo_usuario=request.POST.get("tipo_de_usuario")
        try:
  
            usuario_novo=Usuario.objects.create(
                nome=nome,
                senha=senha,
                CPF=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone,
                genero=genero,
                tipo_usuario=tipo_usuario
            )
            usuario_novo.save()
            usuario_criado="Usuario criado com sucesso"
        except Exception as e:
            print("Erro ao criar usuário:", e)
            usuario_criado="Erro ao criar o usuario"
        

    return render(request,"./loja/static/html/administrador/usuario_criar.html",{'usuario_criado':usuario_criado})
