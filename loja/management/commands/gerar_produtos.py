from django.core.management.base import BaseCommand
from faker import Faker
import random
from loja.models import Produto, Categoria, ImagemProduto
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests


class Command(BaseCommand):
    help = 'Gera produtos falsos e múltiplas imagens'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        # Criar categorias iniciais
        categorias = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios']
        for nome in categorias:
            Categoria.objects.get_or_create(nome=nome)

        todas_categorias = list(Categoria.objects.all())

        # Gerador de imagens random (600x600)
        url_imagem_fake = "https://picsum.photos/600"

        for _ in range(10):
            nome = fake.word().capitalize() + ' ' + fake.word().capitalize()
            preco = round(random.uniform(10, 500), 2)
            preco_promocional = preco * random.choice([1, 0.9, 0.8])

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

            # ======== IMAGEM PRINCIPAL ========
            try:
                response = requests.get(url_imagem_fake)
                produto.imagem_principal.save(
                    f"{produto.slug}-principal.jpg",
                    ContentFile(response.content),
                    save=True
                )
            except:
                pass  # Se falhar, apenas deixa sem imagem principal

            # ======== VÁRIAS IMAGENS EXTRAS ========
            qtd_imagens = random.randint(1, 5)  # número aleatório de imagens extras

            for i in range(qtd_imagens):
                try:
                    response = requests.get(url_imagem_fake)
                    image_file = ContentFile(response.content)

                    ImagemProduto.objects.create(
                        produto=produto,
                        imagem=image_file,
                        descricao=f"Imagem {i+1} de {produto.nome}",
                    )
                except:
                    pass

        self.stdout.write(self.style.SUCCESS('Produtos e imagens criados com sucesso!'))
