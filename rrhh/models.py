from django.db import models
from proyectos.models import Proyectos

# Create your models here.

class NotaDePedido(models.Model):

    class SioNo(models.TextChoices):
        SI = "SI"
        NO = "NO"

    class Tipo(models.TextChoices):
        NP = "NP"
        OS = "OS"

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    numero = models.IntegerField(verbose_name="Nota de pedido numero")
    titulo = models.CharField(max_length=200, verbose_name="Titulo de la nota de pedido")
    creador = models.CharField(max_length=200, verbose_name="Creador")
    destinatario = models.CharField(max_length=200, verbose_name="Destinatario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualiacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    fecha_requerida = models.CharField(max_length=200, verbose_name="Fecha requerida")
    copia = models.CharField(max_length=200, verbose_name="Quien recibe en copia")
    adjuntos = models.FileField(verbose_name="Adjuntos", blank=True, null=True)
    envio_documentacion = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Es para enviar documentación")
    cambio_proyecto = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Genera cambios al proyecto")
    comunicacion_general = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Es comunicación general")
    descripcion = models.TextField(verbose_name="Descripción de la causa")
    tipo = models.CharField(choices=Tipo.choices, max_length=20, verbose_name="Tipo de correspondencia", blank=True, null=True)
    numero = models.IntegerField(verbose_name="Nota de pedido numero", blank=True, null=True)
    visto = models.CharField(max_length=200, verbose_name="Visto", blank=True, null=True)

    class Meta:
        verbose_name="Correspondencia"
        verbose_name_plural="Correspondencias"

    def __str__(self):
        return self.titulo

class datosusuario(models.Model):

    class estados(models.TextChoices):

        ACTIVO = "ACTIVO"
        NO_ACTIVO = "NO ACTIVO"


    identificacion = models.CharField(max_length=200, verbose_name="Identificacion")
    imagen = models.CharField(max_length=200, verbose_name="Imagen", blank=True, null=True, editable=False)
    imagenlogo = models.ImageField(verbose_name="Imagen", blank=True, null=True)
    area = models.CharField(max_length=200, verbose_name="Area", blank=True, null=True)
    cargo = models.CharField(max_length=200, verbose_name="Cargo", blank=True, null=True)
    email = models.CharField(max_length=200, verbose_name="Email", blank=True, null=True)
    estado = models.CharField(choices=estados.choices, default=estados.ACTIVO, max_length=20, verbose_name="Estado")

    class Meta:
        verbose_name="Dato de usuario"
        verbose_name_plural="Datos de los usuarios"

    def __str__(self):
        return self.identificacion

class ComentariosCorrespondencia(models.Model):
    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name = "Usuario")
    correspondencia = models.ForeignKey(NotaDePedido, on_delete=models.CASCADE, verbose_name = "Usuario")
    comentario = models.CharField(max_length=200, verbose_name="Creador")
    fecha = models.DateTimeField(verbose_name="Fecha")

    class Meta:
        verbose_name="Comentario"
        verbose_name_plural="Comentarios"

class Vacaciones(models.Model):
    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_final = models.DateField(verbose_name="Fecha final")

    class Meta:
        verbose_name="Vacaciones"
        verbose_name_plural="Vacaciones"

class mensajesgenerales(models.Model):

    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha", blank=True, null=True)
    mensaje = models.CharField(verbose_name="Mensaje", blank=True, null=True, max_length=200)


    class Meta:
        verbose_name="Mensaje general"
        verbose_name_plural="Mensajes generales"

    def __str__(self):
        return self.mensaje

class MonedaLink(models.Model):

    nombre = models.CharField(verbose_name="Nombre de la moneda", blank=True, null=True, max_length=200)
    usuario_portador = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario Portador")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    tipo = models.CharField(verbose_name="Tipo de moneda", blank=True, null=True, max_length=200)

    class Meta:
        verbose_name="Moneda link"
        verbose_name_plural="Monedas link"

    def __str__(self):
        return self.nombre

class EntregaMoneda(models.Model):
    moneda = models.ForeignKey(MonedaLink, on_delete=models.CASCADE, verbose_name="Usuario Portador")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la entrega")
    usuario_recibe = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario Recibe")
    mensaje = models.CharField(verbose_name="Mensaje de la entrega", blank=True, null=True, max_length=300)

    class Meta:
        verbose_name="Entrega de moneda"
        verbose_name_plural="Entregas de monedas"

    def __str__(self):
        return self.mensaje

class Anuncios(models.Model):

    class categoria(models.TextChoices):

            LINKP = "LINKP"
            COMUNIDAD = "COMUNIDAD"
            PROYECTOS = "PROYECTOS"

    class activo(models.TextChoices):

            SI = "SI"
            NO = "NO"

    titulo = models.CharField(max_length=300, verbose_name="Nombre del anuncio")
    descrip = models.CharField(max_length=300, verbose_name="Descripción corta")
    imagen = models.ImageField(verbose_name="Imagen")
    categoria = models.CharField(choices=categoria.choices, max_length=20, verbose_name="Categoria")
    activo = models.CharField(choices=activo.choices, max_length=20, verbose_name="Activo")

    class Meta:
        verbose_name="Anuncio"
        verbose_name_plural="Anuncios"

    def __str__(self):
        return self.titulo

class Seguimiento(models.Model):

    class estados(models.TextChoices):

        ESPERA = "ESPERA"
        TRABAJANDO = "TRABAJANDO"
        PROBLEMAS = "PROBLEMAS"
        LISTO = "LISTO"

    class areas(models.TextChoices):

        PRESUPUESTO = "PRESUPUESTOS"
        COMPRAS_CONTRATACIONES = "COMPRAS Y CONTRATACIONES"
        EQUIPO_TECNICO = "EQUIPO TECNICO"
        ADMINISTRACION_FINANZAS = "ADMINISTRACIÓN Y FINANZAS"
        COMERCIALIZACION_MARKETING = "COMERCIALIZACIÓN Y MARKETING"
        RR_HH = "RECURSOS HUMANOS"
        DIRECCION = "DIRECCIÓN"
        OBRA = "OBRA"

    orden = models.IntegerField(verbose_name="Orden de la tarea")
    area = models.CharField(choices=areas.choices, max_length=100, verbose_name="Area")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la tarea")
    proyecto =  models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name="Proyecto")
    estado = models.CharField(choices=estados.choices, default=estados.ESPERA, max_length=20, verbose_name="Estado")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
    fecha_final = models.DateField(verbose_name="Fecha final", blank=True, null=True)
    responsable =  models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Responsable", blank=True, null=True)
    adjunto = models.FileField(verbose_name="Adjunto", blank=True, null=True)

    class Meta:
        verbose_name="Seguimiento"
        verbose_name_plural="Seguimientos"

    def __str__(self):
        return self.nombre

class Minutas(models.Model):
    creador = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Creador")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la minuta")
    fecha = models.DateField(verbose_name="Fecha", blank=True, null=True)
    integrantes = models.CharField(max_length=200, verbose_name="Integrantes")

    class Meta:
        verbose_name="Minuta"
        verbose_name_plural="Minutas"

    def __str__(self):
        return self.nombre

class Acuerdos(models.Model):

    class estados(models.TextChoices):

        CHECK = "CHECK"
        NO_CHECK = "NO CHECK"


    minuta = models.ForeignKey(Minutas, on_delete=models.CASCADE, verbose_name="Minutas")
    tema = models.CharField(max_length=400, verbose_name="Tema/acuerdo")
    responsable = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Responsable", blank=True, null=True)
    estado = models.CharField(choices=estados.choices, default=estados.NO_CHECK, max_length=20, verbose_name="Estado")

    class Meta:
        verbose_name="Acuerdo"
        verbose_name_plural="Acuerdos"

    def __str__(self):
        return self.tema
    
