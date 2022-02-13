from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    # custom startup code
    def ready(self) -> None:
        #return super().ready()
        from listItems.models import SearchField
        from stocks.models import Stock
        from stocks.func import saveSP500, loadSP500, validateInput, getYF_data
        
        saveSP500()
        tickers,companies = loadSP500()
        
        symbols = ['FB','AAPL','AMZN','NFLX','GOOGL']

        Stock.objects.all().delete()
        # for i in range(len(symbols)):
        #     convertedTicker,convertedCompany = validateInput(symbols[i],tickers,companies)[1:3]
        #     low, high, open, close = getYF_data(convertedTicker)
        #     s = Stock(
        #         ticker = convertedTicker,
        #         company = convertedCompany,
        #         open = open,
        #         close = close,
        #         low_52wk = low,
        #         high_52wk = high
        #     )
        #     s.save()

        ticker = 'FB'
        low, high, open, close = getYF_data(ticker)
        s = Stock(
            ticker = ticker,
            company = 'Meta Platforms',
            open = open,
            close = close,
            low_52wk = low,
            high_52wk = high
        )
        s.save()

        ticker = 'AAPL'
        low, high, open, close = getYF_data(ticker)
        s = Stock(
            ticker = ticker,
            company = 'Apple',
            open = open,
            close = close,
            low_52wk = low,
            high_52wk = high
        )
        s.save()

        SearchField.objects.all().delete()
        SearchField(count=len(symbols)).save()