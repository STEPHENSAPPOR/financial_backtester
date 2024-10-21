from django.urls import path
from .views import home, results, run_backtest  # Import run_backtest view

urlpatterns = [
    path('', home, name='home'),                # Home page
    path('results/', results, name='results'),  # Existing line for results
    path('run_backtest/', run_backtest, name='run_backtest'),  # Path for run_backtest
]

