from django.db import models

class BacktestResult(models.Model):
    test_name = models.CharField(max_length=100)
    result_value = models.FloatField()
    date_run = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField()  # You can store parameters as JSON

    def __str__(self):
        return f"{self.test_name} - {self.result_value}"

class StockData(models.Model):  # Consider renaming to StockData
    symbol = models.CharField(max_length=10)  # Stock symbol (e.g., AAPL)
    date = models.DateField()                  # Date of the record
    open_price = models.FloatField()           # Open price
    close_price = models.FloatField()          # Close price
    high_price = models.FloatField()           # High price
    low_price = models.FloatField()            # Low price
    volume = models.BigIntegerField()          # Volume of shares traded

    class Meta:
        ordering = ['date']
        unique_together = ('symbol', 'date')     # Ensures no duplicate entries for the same symbol and date

    def __str__(self):
        return f"{self.symbol} on {self.date}"

