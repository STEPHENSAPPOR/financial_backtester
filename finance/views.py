from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import BacktestResult
import requests

# Function to fetch historical data from Alpha Vantage API
def get_historical_data(symbol):
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    historical_data = []
    for date, stats in data.get('Time Series (Daily)', {}).items():
        historical_data.append({
            'date': date,
            'close_price': float(stats['4. close']),
        })
    return historical_data

# Home view
def home(request):
    return render(request, 'finance/home.html')

# Backtest logic
def run_backtest(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        initial_investment = float(request.POST.get('initial_investment', 0))
        moving_average_short = int(request.POST.get('short_ma', 5))
        moving_average_long = int(request.POST.get('long_ma', 20))

        investment = initial_investment
        total_return = 0
        trades_executed = 0
        positions = []   

        # Retrieve historical data
        historical_data = get_historical_data(symbol)

        # Ensure historical data is available
        if not historical_data:
            return JsonResponse({'error': 'No historical data found for this symbol'}, status=404)

        for i in range(len(historical_data)):
            current_data = historical_data[i]

            # Calculate short moving average (buy signal)
            if i >= moving_average_short - 1:
                short_ma = sum(data['close_price'] for data in historical_data[i - moving_average_short + 1:i + 1]) / moving_average_short
                if current_data['close_price'] < short_ma:
                    buy_price = current_data['close_price']
                    positions.append(buy_price)
                    trades_executed += 1
                    investment -= buy_price

            # Calculate long moving average (sell signal)
            if i >= moving_average_long - 1 and positions:
                long_ma = sum(data['close_price'] for data in historical_data[i - moving_average_long + 1:i + 1]) / moving_average_long
                if current_data['close_price'] > long_ma:
                    sell_price = current_data['close_price']
                    total_return += (sell_price - positions.pop())
                    investment += sell_price
                    trades_executed += 1

        # Save backtest result
        backtest_result = BacktestResult(
            test_name=f"Backtest for {symbol}",
            result_value=total_return + investment - initial_investment,
            parameters={
                'initial_investment': initial_investment,
                'short_ma': moving_average_short,
                'long_ma': moving_average_long
            }
        )
        backtest_result.save()

        return JsonResponse({
            'total_return': total_return + investment - initial_investment,
            'trades_executed': trades_executed,
            'test_name': backtest_result.test_name
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Example function to generate a report
def generate_report(request):
    # Fetch backtest results (You might want to filter by a specific test)
    results = BacktestResult.objects.all()  # Adjust this as necessary

    # Create a simple plot (e.g., total return over time)
    plt.figure()
    plt.plot([result.date_run for result in results], [result.result_value for result in results])
    plt.title('Backtest Results Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Return')
    plt.grid()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create PDF using reportlab
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Backtest Results Report")
    p.drawImage(buffer, 100, 500, width=400, height=300)  # Adjust the position and size
    p.showPage()
    p.save()

    return response

# View for displaying backtest results
def results(request):
    # Implement logic to display the results
    return render(request, 'finance/results.html')

