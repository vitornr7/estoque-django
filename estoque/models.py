from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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
    endereço = models.CharField(max_length=50)

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

    def clean(self):
        if self.baixo_estoque > self.alto_estoque:
            raise ValidationError(
                {'baixo_estoque': ["Baixo estoque maior que alto.", ]})

    def __str__(self):
        return self.empresa.usuario.username + ' - ' + self.produto.nome


class Vendas(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(1000000)])
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produto.nome + ' - ' + str(self.data)


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
    status = models.PositiveSmallIntegerField(choices= STATUS_PEDIDO,validators=[MinValueValidator(0), MaxValueValidator(2)], default=ABERTO)

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
