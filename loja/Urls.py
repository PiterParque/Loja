from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('produto/<slug:slug>',views.produto,name="produto"),
    path('logon/',views.logon_validation,name="tela_logon"),
    path('perfil/',views.perfil,name="perfil"),
    path('perfil/dados_pessoais',views.dados_pessoais,name="dados_pessoais"),
    path('perfil/endereco',views.endereco,name="endereco"),
    path('perfil/pedidos',views.pedidos,name="pedidos"),
    path('perfil/metodos_pagamento',views.metodos_pagamento,name="metodos_pagamento"),
    path('perfil/autenticacao',views.autenticacao,name="autenticacao"),
    path('perfil/notificacao',views.notificacao,name="notificacao"),
    path('administracao/',views.administracao,name='administracao'),
    path('administracao/usuarios',views.usaurios,name="usuarios"),
    path('administracao/usuario/<int:id>',views.usuario,name="usuario"),
    path('administracao/usuario/criar',views.criar_usuario,name="usuario_criar")
]
