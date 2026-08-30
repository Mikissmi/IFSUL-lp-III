# Adicione esta classe ao seu models.py (mesmo app de Usuario/PerfilDermatologico)

from django.db import models


class Produto(models.Model):
    CATEGORIA_CHOICES = [(c, c) for c in [
        'Limpeza', 'Água Micelar', 'Tônico', 'Sérum', 'Hidratante',
        'Protetor Solar', 'Esfoliante', 'Máscara Facial', 'Óleo Facial',
        'Contorno de Olhos',
    ]]
    MODO_USO_CHOICES = [(v, v) for v in ['Manhã', 'Noite', 'Manhã e Noite']]

    marca = models.CharField(max_length=100)
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)

    # multivalorados, guardados como no CSV: "Oleosa;Mista", "Acne;Oleosidade"
    tipo_pele = models.CharField(max_length=100)
    preocupacao = models.CharField(max_length=255)

    modo_uso = models.CharField(max_length=20, choices=MODO_USO_CHOICES)
    ingrediente_principal = models.CharField(max_length=100)
    fps = models.PositiveSmallIntegerField(blank=True, null=True)
    tamanho_ml = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1)
    num_avaliacoes = models.PositiveIntegerField(default=0)
    descricao = models.TextField(blank=True)
    imagem_url = models.URLField(max_length=300, blank=True)
    link_produto = models.URLField(max_length=300, blank=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return f'{self.marca} - {self.nome}'

    def tipos_pele(self):
        return [t.strip() for t in self.tipo_pele.split(';') if t.strip()]

    def preocupacoes(self):
        return [p.strip() for p in self.preocupacao.split(';') if p.strip()]
