from django.core.management.base import BaseCommand
from faker import Faker
import random
from loja.models import Produto, Categoria, ImagemProduto
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests


class Command(BaseCommand):
    help = 'Gera produtos falsos com pelo menos uma imagem cada'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        # Criar categorias padrão caso não existam
        categorias = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios']
        for nome in categorias:
            Categoria.objects.get_or_create(nome=nome)

        todas_categorias = list(Categoria.objects.all())

        url_imagem_fake = "https://picsum.photos/600"

        for _ in range(10):
            nome = fake.word().capitalize() + ' ' + fake.word().capitalize()
            preco = round(random.uniform(10, 500), 2)
            preco_promocional = round(preco * random.choice([1, 0.9, 0.8]), 2)

            # Criar produto
            produto = Produto.objects.create(
                nome=nome,
                descricao=fake.text(200),
                marca=fake.company(),
                categoria=random.choice(todas_categorias),
                preco=preco,
                preco_promocional=preco_promocional,
                estoque=random.randint(0, 100),
                sku=fake.unique.ean(length=8),
                slug=slugify(nome),
                ativo=True,
                ml=f"{random.randint(50, 1000)}ml",
            )

            # ===== GARANTIR PELO MENOS UMA IMAGEM =====
            qtd_imagens = random.randint(1, 5)  # 1 a 5 imagens

            for i in range(qtd_imagens):
                try:
                    response = requests.get(url_imagem_fake)
                    image_file = ContentFile(response.content, name=f"{produto.slug}-{i}.jpg")

                    ImagemProduto.objects.create(
                        produto=produto,
                        imagem=image_file
                    )
                except Exception as e:
                    print(f"Erro ao baixar imagem do produto {produto.nome}: {e}")

        self.stdout.write(self.style.SUCCESS("Produtos e imagens criados com sucesso!"))
