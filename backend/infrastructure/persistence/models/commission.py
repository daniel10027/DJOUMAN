from django.db import models

class CommissionPolicy(models.Model):
    service_category = models.ForeignKey("persistence.ServiceCategory", on_delete=models.SET_NULL, null=True, blank=True, related_name="commission_policies")
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Pourcentage (ex: 12.5)")
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        target = self.service_category.name if self.service_category else "Global"
        return f"Commission {target} {self.rate}%"
