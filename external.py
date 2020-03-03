#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# External embeds and widgets

ticker_tv = '<!-- TradingView Widget BEGIN --> <div class="tradingview-widget-container"> <div class="tradingview-widget-container__widget"></div> <div class="tradingview-widget-copyright"><a href="https://br.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">Ticker Tape</span></a> por TradingView</div> <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async> { "symbols": [ { "description": "Ibovespa", "proName": "BMFBOVESPA:IBOV" }, { "description": "SLC", "proName": "BMFBOVESPA:SLCE3" }, { "description": "Dólar", "proName": "USDBRL" } ], "colorTheme": "light", "isTransparent": false, "displayMode": "regular", "locale": "br" } </script> </div> <!-- TradingView Widget END -->'

calendar_tv = '<!-- TradingView Widget BEGIN --> <div class="tradingview-widget-container"> <div class="tradingview-widget-container__widget"></div> <div class="tradingview-widget-copyright"><a href="https://br.tradingview.com/markets/currencies/economic-calendar/" rel="noopener" target="_blank"><span class="blue-text">Calendário Econômico</span></a> por TradingView</div> <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async> { "colorTheme": "light", "isTransparent": true, "width": "100%", "height": "500", "locale": "br", "importanceFilter": "-1,0,1", "currencyFilter": "BRL" } </script> </div> <!-- TradingView Widget END -->'
