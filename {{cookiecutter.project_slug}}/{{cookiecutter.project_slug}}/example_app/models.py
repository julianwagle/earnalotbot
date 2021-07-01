from django.db import models

class TransactionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self.db)

    def all(self):
        return self.get_queryset().active()

class Transaction(models.Model):
    transaction_code = models.CharField(default=True, null=True, blank=True, max_length=100)
    TRANSACTIONS = (
        ('B', 'Buy'),
        ('H', 'Hold'),
        ('S', 'Sell'),
    )
    action = models.CharField(default=True, null=True, blank=True, max_length=4, choices=TRANSACTIONS)
    symbol = models.CharField(default=True, null=True, blank=True, max_length=6)
    date_time = models.DateTimeField(auto_now=True, null=True)
    share_price = models.FloatField(default=True, null=True, blank=True)
    share_quant = models.FloatField(default=True, null=True, blank=True)
    share_equity = models.FloatField(default=True, null=True, blank=True)
    roi_total = models.FloatField(default=True, null=True, blank=True)
    roi_net = models.FloatField(default=True, null=True, blank=True)
    avg_buy_price = models.FloatField(default=True, null=True, blank=True)
    testing = models.BooleanField(default=True)

    objects = TransactionManager()
    def __str__(self):
        return self.transaction_code
