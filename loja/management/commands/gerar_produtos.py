from django.core.management.base import BaseCommand
from faker import Faker
import random
from loja.models import Produto, Categoria
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Gera produtos falsos para teste usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        categorias = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios']
        for nome in categorias:
            Categoria.objects.get_or_create(nome=nome)

        todas_categorias = list(Categoria.objects.all())

        for _ in range(10):
            nome = fake.word().capitalize() + ' ' + fake.word().capitalize()
            marca = fake.company()
            categoria = random.choice(todas_categorias)
            preco = round(random.uniform(10, 500), 2)
            preco_promocional = preco * random.choice([0.8, 0.9, 1])
            estoque = random.randint(0, 100)
            sku = fake.unique.ean(length=8)
            slug = slugify(nome)

            Produto.objects.create(
                nome=nome,
                descricao=fake.text(200),
                marca=marca,
                categoria=categoria,
                preco=preco,
                preco_promocional=preco_promocional,
                estoque=estoque,
                sku=sku,
                slug=slug,
                ativo=True,
                ml=f"{random.randint(50, 1000)}ml",
            )

        self.stdout.write(self.style.SUCCESS(' Produtos criados com sucesso!'))
