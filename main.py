import pandas as pd
import warnings
from datetime import date, datetime
from wallstreet import Stock, Call, Put
from plotly.colors import n_colors
from plotly.offline import plot
import plotly.graph_objs as go

warnings.filterwarnings("ignore")

stock = input('Enter a stock/ETF: ')

s = Stock(stock)
c = Call(stock)

expireDates = c.expirations

bids = []
asks = []
strikes = []
volumes = []
thetas = []
deltas = []
impliedVolatilities = []

print("Expiration dates for " + stock + ": ")
for date in expireDates:
    dateString = date
    dateObject = datetime.strptime(dateString, "%d-%m-%Y")
    month = str(dateObject.month)
    day = str(dateObject.day)
    year = str(dateObject.year)
    print(month + "-" + day + "-" + year)

userDate = input("Enter an expiration date in the same format as above: ")
dateString = userDate
dateObject = datetime.strptime(dateString, "%m-%d-%Y")
c = Call(stock, d=dateObject.day, m=dateObject.month, y=dateObject.year)
strikePrices = c.strikes

for price in strikePrices[-20:]:
    c.set_strike(price)
    strikes.append(c.strike)
    bids.append(c.bid)
    asks.append(c.ask)
    volumes.append(c.volume)
    thetas.append(round(c.theta(), 5))
    deltas.append(round(c.delta(), 5))


price = str(round(s.price, 2))
print(stock + ":")
print("Price: $" + price)
change = str(round(s.change, 2))
print("Change: $" + change)
percentChange = str(round(s.cp, 2))
print("%" + percentChange)


layout = go.Layout({
    'title': {
        'text': stock,
        'font': {
            'size': 15
        }
    }
})
fig = go.Figure(data=[go.Table(header=dict(values=['<b>Strike</b>', '<b>Bid</b>', '<b>Ask</b>', '<b>Volume</b>', '<b>Theta</b>', '<b>Delta</b>'],
                                           line_color='#B3B3B3',
                                           fill_color='#3D3D3D',
                                           font=dict(color='#00C900')
                                           ),
                               cells=dict(values=[c.strikes[-20:], bids, asks, volumes, thetas, deltas],
                                          line_color='#B3B3B3',
                                          fill_color='#3D3D3D',
                                          font=dict(color='#00C900'),
                                          ),
                               )])
fig.show()

strike = input("Select a strike price: $")
strike = int(strike)
stockPrice = input("Enter the average cost per share: $")
stockPrice = float(stockPrice)
c = Call(stock, d=dateObject.day, m=dateObject.month, y=dateObject.year, strike=strike)
optionPrice = c.price
creditReceived = float(optionPrice * 100)
totalCost = (stockPrice * 100)
breakevenPrice = round(stockPrice - optionPrice, 2)

profitLoss = []
for expiryPrice in strikes:
    profitLoss.append(round((expiryPrice - stockPrice + optionPrice) * 100, 2))

for value in profitLoss:
    if value > (strike - expiryPrice + creditReceived * 100 ):
        value = (strike - expiryPrice + creditReceived * 100)

print(breakevenPrice)

fig = go.Figure(data=[go.Table(header=dict(values=['<b>Price at Expiration</b>', '<b>P/L</b>'],
                                           line_color='#B3B3B3',
                                           fill_color='#3D3D3D',
                                           font=dict(color='#00C900'),
                                           ),
                               cells=dict(values=[strikes, profitLoss])
                               )])
fig.show()


