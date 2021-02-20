from django.db import models
# Create your models here.


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name="Nombre")

    def __unicode__(self):
        return self.name
    class Meta: 
        verbose_name = 'Provincia'


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name="Nombre")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Provincia")

    def __unicode__(self):
        return self.name
    class Meta: 
        verbose_name = 'Distrito'

class Township(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name="Nombre",unique=True)
    distrit = models.ForeignKey(District, on_delete=models.CASCADE,verbose_name="Distrito")

    def __unicode__(self):
        return self.name
    class Meta: 
        verbose_name = 'Municipio'

class HistoricProvince(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name = "Provincia")
    confirmedPDIA = models.IntegerField(null=False,verbose_name="Confirmados PDIA")
    totalConfirmed = models.IntegerField(null=False,verbose_name="Total Confirmados")
    Hospitalized = models.IntegerField(null=False, verbose_name="Hospitalizados")
    ICU = models.IntegerField(null=False,verbose_name="UCIS")
    deceased = models.IntegerField(null=False,verbose_name="Fallecidos")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'province'], name='CONSTR_NO_REPEAT_REGISTRPROV')
        ]
        verbose_name = 'Histórico de datos por Provincia'


class HistoricDistrit(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=100, default="", verbose_name='Fecha de diagnóstico')    
    distr = models.ForeignKey(District, on_delete=models.CASCADE,null=True, verbose_name="Distrito")
    Confirmados_PCR_TA = models.IntegerField(null=False, verbose_name='Confirmados por PCR TOTAL')
    Confirmados_PCR_TA_14d = models.IntegerField(null=False, verbose_name='Confirmados PCR 14 días')
    confirmed14100hab =  models.IntegerField(null=False,verbose_name='Confirmados 14 días x 100.000 hab')
    totalConfirmed = models.IntegerField(null=False, verbose_name='Confirmados totales')
    deceases = models.IntegerField(null=False, verbose_name='Fallecidos')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'distr'], name='CONSTR_NO_REPEAT_REGISTRDISTR')
        ]
        verbose_name = 'Histórico de datos por distrito sanitario'

class HistoricTownship(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(max_length=100, default="", verbose_name='Fecha de diagnóstico')
    township = models.ForeignKey(Township, on_delete=models.CASCADE,null=True, verbose_name='Municipio')
    Confirmados_PCR_TA = models.IntegerField(null=False, verbose_name='Confirmados por PCR TOTAL')
    Confirmados_PCR_TA_14d = models.IntegerField(null=False, verbose_name='Confirmados PCR 14 días')
    confirmed14100hab =  models.IntegerField(null=False,verbose_name='Confirmados 14 días x 100.000 hab')
    totalConfirmed = models.IntegerField(null=False, verbose_name='Confirmados totales')
    deceases = models.IntegerField(null=False, verbose_name='Fallecidos')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'township'], name='CONSTR_NO_REPEAT_REGISTRTOWN')
        ]
        verbose_name = 'Histórico de datos por municipio'