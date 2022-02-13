from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    # custom startup code
    def ready(self) -> None:
        from listItems.models import SearchField
        from stocks.models import Stock
        from stocks.func import saveSP500, loadSP500, validateInput, getYF_data
        from collections import namedtuple

        saveSP500()
        tickers,companies = loadSP500()
        
        symbols = ['FB','AAPL','AMZN','NFLX','GOOGL']

        TickerInfo = namedtuple("PriceInfo","ticker company low high open close")
        info_arr = set()
        for i in range(len(symbols)):
            convertedTicker,convertedCompany = validateInput(symbols[i],tickers,companies)[1:3]
            low, high, open, close = getYF_data(convertedTicker)
            info_arr.add(TickerInfo(convertedTicker, convertedCompany, low, high, open, close))

        info_arr = list(info_arr)

        Stock.objects.all().delete()
        for i in range(len(info_arr)):
            ticker_info = info_arr[i]
            s = Stock(
                ticker = ticker_info.ticker,
                company = ticker_info.company,
                open = ticker_info.open,
                close = ticker_info.close,
                low_52wk = ticker_info.low,
                high_52wk = ticker_info.high
            )
            s.save()

        SearchField.objects.all().delete()
        SearchField(count=len(info_arr)).save()