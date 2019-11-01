from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    codigo = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])

    def get_absolute_url(self):
        return reverse("estoque:detalhes_produto", args=[str(self.id)])

    def __str__(self):
        return self.nome


class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # true = filial | false = central
    filial = models.BooleanField(default=True)
    endereco = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username


class Estoque(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    baixo_estoque = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    alto_estoque = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'produto'], name='empresa_produto'),
        ]

    def get_absolute_url(self):
        return reverse("estoque:detalhes_produto", args=[str(self.id)])

    def clean(self):
        if self.baixo_estoque > self.alto_estoque:
            raise ValidationError(
                {'baixo_estoque': ["Baixo estoque maior que alto.", ]})

    def __str__(self):
        return self.empresa.usuario.username + ' - ' + self.produto.nome


class VendasFilial(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])
    # data = models.DateTimeField(auto_now_add=True)
    data = models.DateTimeField()

    def __str__(self):
        return self.produto.nome + ' - ' + str(self.data)


class Carrinho(models.Model):
    ABERTO = False
    FECHADO = True

    status = models.BooleanField(default=ABERTO)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)], default=0)

    data = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['empresa'], condition=Q(status=False), name='carrinho_aberto'),
        ]

    def __str__(self):
        return str(self.id) + ' - ' + str(self.empresa) + ' - ' + str(self.status)


class CarrinhoProdutos(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['carrinho', 'produto'], name='carrinho_produto'),
        ]

    def __str__(self):
        return str(self.carrinho) + ' - ' + str(self.produto)


class PedidosFilial(models.Model):
    ABERTO = 0
    APROVADO = 1
    REPROVADO = 2

    STATUS_PEDIDO = [
        (ABERTO, 'Aberto'),
        (APROVADO, 'Aprovado'),
        (REPROVADO, 'Reprovado'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_PEDIDO, validators=[
                                              MinValueValidator(0), MaxValueValidator(2)], default=ABERTO)

    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produto.nome + ' - ' + str(self.data)


class ComprasCentral(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produto.nome + ' - ' + str(self.data)
