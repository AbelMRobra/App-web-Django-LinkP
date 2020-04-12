from django.db import models

# Create your models here.

class Proyectos(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Titulo")
    description = models.CharField(max_length=200, verbose_name = "Descripción")
    finish_date = models.DateTimeField(verbose_name = "Fecha de entrega")
    created = models.DateTimeField(auto_now=True, verbose_name = "Fecha de actualización")
    img = models.ImageField(verbose_name = "Imagen", upload_to="proyects")
    presup = models.FileField(null=True, verbose_name = "Presupuesto", upload_to="proyects/presupuestos")
    exp = models.FileField(null=True, verbose_name = "Explosión de insumos", upload_to="proyects/exp")
    curva = models.FileField(null=True, verbose_name = "Curva de inversión", upload_to="proyects/curva")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.title

class Contratos(models.Model):
    np = models.CharField(max_length=200, verbose_name="Nota de pedido")
    titulo = models.CharField(max_length=200, verbose_name="Nombre del contrato")
    provee = models.CharField(max_length=200, verbose_name="Nombre del contratista")

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
    
    def __str__(self):
        return self.titulo

class Certificados(models.Model):
    obra = models.ForeignKey(Proyectos, null=False, blank=True, on_delete=models.CASCADE, verbose_name = "Obra")
    nombre = models.ForeignKey(Contratos, null=False, blank=True, on_delete=models.CASCADE, verbose_name= "Nombre del Contrato")
    num_cer =  models.IntegerField(verbose_name="Numero de certificado")
    descrip = models.CharField(max_length=200, verbose_name="Descripción")
    adj = models.FileField(null=True, verbose_name = "Adjunto", upload_to="projects/cert")

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return self.descrip
    
