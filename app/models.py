from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    origem = models.TextField()
    imagem = models.ImageField(upload_to='app/static/imagens/', blank=True)
    compostos = models.TextField()
    categoria = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Produtos"
    def __str__(self):
        return f'{self.categoria} {self.nome}'

class Resultado(models.Model):
    nome = models.CharField(max_length=100)
    feito = models.TextField(verbose_name='Do que é composto')
    class Meta:
        verbose_name_plural = "Resultados"
    def __str__(self):
        return f'{self.nome}'
    
    
