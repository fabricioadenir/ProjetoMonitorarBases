from django.db import models
from datetime import datetime


class User(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nome ')
    positon = models.CharField(max_length=250, verbose_name='Cargo ')
    email = models.EmailField(verbose_name='E-mail ')
    team = models.CharField(max_length=40, verbose_name='Time ')
    detail = models.CharField(max_length=500, verbose_name='Detalhes ')
    id_user = models.CharField(
        primary_key=True, max_length=50, verbose_name='Usuário ')
    password = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='Senha ')
    photo = models.ImageField("Anexos", null=True, blank=True,
                                upload_to='static/img')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "0-User"


class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Cliente ')
    id_client = models.CharField(
        primary_key=True, max_length=10, verbose_name='Sigla do cliente')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1-Cliente"


class System(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Cliente ')
    name = models.CharField(max_length=250, verbose_name='Sistema ')
    initials = models.CharField(
        max_length=10, verbose_name='Sigla do sistema ')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "2-Sistema"


class Module(models.Model):
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, verbose_name='Sistema ')
    name = models.CharField(max_length=250, verbose_name='Modulo ')
    description = models.CharField(
        max_length=250, verbose_name='Descrição do modulo ')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "3-Modulo"


class Functionality(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, verbose_name='Modulo')
    name = models.CharField(max_length=250, verbose_name='Funcionalidade ')
    description = models.CharField(
        max_length=250, verbose_name='Descrição da funcionalidade ')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "4-Funcionalidade"


class DataBases(models.Model):
    DRIVE_CHOICES = (
        (u'sql_server', u'SQL Server'),
        (u'oracle', u'Oracle'),
        (u'mongodb', u'MongoDB'),
        (u'postgresql', u'PostgreSQL'),
        (u'mysql', u'MySQL'),
        (u'elasticsearch', u'ElascticSearch'),
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Cliente ')
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, verbose_name='Sistema ')
    _type = models.CharField(
        max_length=200, choices=DRIVE_CHOICES, verbose_name='Tipo de base ')
    server_instancia = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='Server Instancia ')
    ip = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='IP ')
    port = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='PORT ')
    uri = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='URI ')
    database = models.CharField(
        max_length=100, verbose_name='DataBase ')
    collection = models.CharField(
        max_length=100, verbose_name='Coleção Mongo  ', null=True, blank=True)
    user = models.CharField(
        null=True, default=None, blank=True, max_length=100, verbose_name='Usuário ')
    password = models.CharField(
        null=True, default=None, blank=True, max_length=50, verbose_name='Senha ')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.database

    class Meta:
        verbose_name_plural = "5-DataBases"


class Monitoring(models.Model):
    ORIGEM_CHOICES = (
        (u'rtc', u'RTC'),
        (u'sac', u'SAC'),
        (u'sccd', u'SCCD'),
        (u'interno', u'INTERNO'),
        (u'outro', u'Outro'),

    )
    name = models.CharField(
        unique=True, verbose_name='Nome ', max_length=250)
    source = models.CharField(
        max_length=20, choices=ORIGEM_CHOICES, verbose_name='Origem ')
    description_source = models.TextField(verbose_name='Descição ')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Cliente ')
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, verbose_name='Sistema ')
    functionality = models.ForeignKey(
        Functionality, on_delete=models.CASCADE, verbose_name='Local do sistema ')
    database = models.ForeignKey(
        DataBases, on_delete=models.CASCADE, verbose_name='DataBase ou Index')
    timeout = models.PositiveIntegerField(
        verbose_name='TimeOut em segundos ', help_text="Tempo de espera pela execução da query.")
    query = models.TextField(
        verbose_name='Query ')
    last_execution = models.DateField(verbose_name="Ultima execução",
                                      null=True, blank=True)
    is_enabled = models.BooleanField(
        verbose_name="Está Cadastrada ", default=False, editable=False)
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "6-Monitorar"


def increment_invoice_number():
    pass


class QueryResults(models.Model):
    query = models.ForeignKey(
        Monitoring, on_delete=models.CASCADE, verbose_name='Query', editable=True)
    count_values = models.IntegerField(
        verbose_name='Quantidade de erros encontrado ', editable=True)
    values = models.TextField(
        null=True, verbose_name='Valores ', editable=True)
    note = models.TextField(
        null=True, verbose_name='Observação ', editable=True)
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=True, auto_now_add=True)

    def __str__(self):
        return self.query.name

    class Meta:
        verbose_name_plural = "8-QueryResults"


class Routines(models.Model):
    query = models.ForeignKey(
        Monitoring, on_delete=models.CASCADE, verbose_name='Query ')
    active_query = models.BooleanField(verbose_name='Ativar consulta ')
    initial_date = models.DateField('Inicio das consultas ')
    and_date = models.DateField('Válido até ')
    created_date = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    date = datetime.now().strftime("%Y-%m-%d")

    def save(self, *args, **kwargs):
        date_inicital = self.initial_date.strftime("%Y-%m-%d")
        and_date = self.and_date.strftime("%Y-%m-%d")

        if (date_inicital <= self.date) and (and_date >= self.date) and (self.active_query):
            self.query.is_enabled = True
            self.query.save(update_fields=['is_enabled'])
        else:
            self.query.is_enabled = False
        self.query.save(update_fields=['is_enabled'])
        super(Routines, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "7-Rotina"
