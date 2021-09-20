from django.db import models

class Station(models.Model):
    RAIL_OPR_ISTT_CD = models.CharField(max_length=20)
    RAIL_OPR_ISTT_NM = models.CharField(max_length=20)
    LN_CD            = models.CharField(max_length=20)
    LN_NM            = models.CharField(max_length=20)
    STIN_CD          = models.CharField(max_length=20)
    STIN_NM          = models.CharField(max_length=20)
    create_at        = models.DateTimeField(auto_now_add=True)
    update_at        = models.DateTimeField(auto_now=True, null=True)
    delete_at        = models.DateTimeField(null=True)
    is_deleted       = models.BooleanField(default=0)

    class Meta:
        db_table = 'stations'