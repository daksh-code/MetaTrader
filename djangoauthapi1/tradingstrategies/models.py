from django.db import models

class StockQuerySet(models.QuerySet):
    def active(self):
        return self.filter(stock_is_active=True)

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    stock_is_active = models.BooleanField(default=False)

    objects = StockQuerySet.as_manager()

    def __str__(self):
        return self.symbol

class Strategy(models.Model):
    name = models.CharField(max_length=100)
    stock = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'stock_is_active': True},
        related_name='strategies'
    )
    quantity=models.IntegerField()
    #max_stop_loss=models.DecimalField(null=True,max_digits=10, decimal_places=2)
    max_stop_loss=models.FloatField(null=True)
    risk_to_reward_ratio = models.FloatField()
    strategy_is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.name
