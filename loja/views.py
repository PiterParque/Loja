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
            if user.tipo_usuario == "Administrador":
                request.session['usuario_id'] = user.id
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
    _usuario=False
    usuario_alterado=False
    mensagem=''
    try:
        usuario_id = request.session.get('usuario_id')
        user=Usuario.objects.filter(id=usuario_id).values()
       
        if user:
            if user[0]['tipo_usuario'] != "Administrador":
                redirect('perfil')
        user=Usuario.objects.filter(id=id).values()
        user=user[0]
        if isinstance(user['data_nascimento'], date):
            print(user['data_nascimento'])
            ano,mes,dia=str(user['data_nascimento'].strftime("%d/%m/%Y")).split("/")
            user['data_nascimento']=dia+"-"+mes+"-"+ano
        usuario_alterado=False
        mensagem="Falha em alterar o usuario"
        if user :
            if user['tipo_usuario'] != "Admisnitrador":
                redirect('perfil')
        if id:
            _usuario=Usuario.objects.filter(id=id).first()
        try:
           if request.method == "POST":
            
                    usuario_obj = Usuario.objects.get(id=id)

                    imagem = request.FILES.get("imagem_usuario")
                    nome = request.POST.get("usuario_nome")
                    cpf = request.POST.get("usuario_cpf")
                    data_nascimento = request.POST.get("usuario_nascimento")
                    telefone = request.POST.get("usuario_telefone")
                    genero = request.POST.get("genero")
                    if genero == "OUTRO":
                        genero = request.POST.get("outro_genero")

                    tipo_usuario = request.POST.get("usuario_tipo")

                    usuario_obj.nome = nome
                    usuario_obj.CPF = cpf
                    usuario_obj.data_nascimento = data_nascimento
                    usuario_obj.telefone = telefone
                    usuario_obj.genero = genero
                    usuario_obj.tipo_usuario = tipo_usuario

                    if imagem:
                        usuario_obj.imagem_usuario = imagem

                    usuario_obj.save()

                    usuario_alterado = True
                    mensagem = "Usuário alterado com sucesso"

        
          
                
        except Exception as e:
                print("Erro:",e)
    except Exception as e :
        print("Erro:",e)
        

    return render(request,"./loja/static/html/administrador/usuario.html",{'usuario':_usuario,'usuario_alterado':usuario_alterado,"mensagem":mensagem})
def criar_usuario(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    usuario_criado=None
 
    try:
           if request.method == "POST":
            
                    usuario_obj = Usuario.objects.create()

                    imagem = request.FILES.get("imagem_usuario")
                    nome = request.POST.get("entrada_nome")
                    senha=request.POST.get("entrada_senha")
                    cpf = request.POST.get("entrada_cpf")
                    data_nascimento = request.POST.get("entrada_nascimento")
                    telefone = request.POST.get("entrada_telefone")
                    genero = request.POST.get("genero")
                    if genero == "OUTRO":
                        genero = request.POST.get("campo_outro_genero")

                    tipo_usuario = request.POST.get("tipo_de_usuario")

                    usuario_obj.nome = nome
                    usuario_obj.senha = senha
                    usuario_obj.CPF = cpf
                    usuario_obj.data_nascimento = data_nascimento
                    usuario_obj.telefone = telefone
                    usuario_obj.genero = genero
                    usuario_obj.tipo_usuario = tipo_usuario

                    if imagem:
                        usuario_obj.imagem_usuario = imagem

                    usuario_obj.save()

                    usuario_alterado = True
                    mensagem = "Usuário alterado com sucesso"

        
    except Exception as e:
                print("Erro:",e)
        

    return render(request,"./loja/static/html/administrador/usuario_criar.html",{'usuario_criado':usuario_criado})
def alterar_senha(request,id):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    senha_alterada=None
    usuario_senha=None
    try:
       usuario_senha=Usuario.objects.filter(id=id).first()
       if request.method == "POST":
           senha= request.POST.get("senha")
           usuario_senha.senha=senha
           usuario_senha.save()
           senha_alterada="Senha Alterada com Sucesso"
    except Exception as e:
        print("Erro:",e)
    return render(request,"./loja/static/html/administrador/alterar_senha.html",{'senha_alterada':senha_alterada,"usuario":usuario_senha})