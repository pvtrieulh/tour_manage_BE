from django.db import models
from location.models import Province, District, Commune


class BaseLocation(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Tỉnh / Thành phố"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Quận / Huyện"
    )
    commune = models.ForeignKey(
        Commune,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Phường / Xã"
    )

    class Meta:
        abstract = True