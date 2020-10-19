import yfinance as yf
import json
'''
TODO    Expand Currency exchanger to support more than DKK to USD

'''
def dkkToUsd(dkk):
    var = yf.Ticker("USDDKK=X").info["ask"]
    usd = dkk/var
    return usd

def isDKK(cur):
    if cur == "DKK":
        return True
    else:
        return False

def getQuote(name, amount):
    n = yf.Ticker(name)
    result = n.info["ask"]
    if isDKK(n.info["currency"]) == True:
        cur = "DKK"
        result = dkkToUsd(result)
    else:
        cur = "USD"
    price = float(result)*float(amount)
    print(str(amount) + " shares of " + name +  " costs $" + str(price))

def getPrice(name, amount):
    n = yf.Ticker(name)
    result = n.info["ask"]
    price = float(result)*float(amount)
    return price

def save():
    amount = me.amount
    stock = me.stocks
    stockAmount = me.stockAmount
    saves = {"Amount" : amount, "Stocks" : stock, "StockAmount" : stockAmount}
    with open("info.json", "w") as write_file:
        json.dump(saves, write_file, indent=4)


class Account:
    amount = 0
    def __init__(self, amount, stocks, stockAmount):
        self.amount = amount
        self.stocks = dict(stocks)
        self.stockAmount = dict(stockAmount)

    def buy(self, name, amount):
        price = getPrice(name, amount)
        name = name.upper()
        self.amount -= price
        self.stocks[name] = [price]
        self.stockAmount[name] = [amount]
        print(name + " bought for $" + str(price))

    
    def sell(self, name):
        name = name.upper()
        price = getPrice(name, stockAmount[name])
        diff = self.stocks[name] - price
        self.amount += price
        del self.stocks[name]
        del self.stockAmount[name]
        print(name + " sold for $" + str(price) + ": Difference " + diff)
        print("Exit to save before checking value")

    def value(self):
        total = self.amount
        for x, y in self.stockAmount.items():
            val = getPrice(x,y[0])
            diff = val - self.stocks[x][0]
            getQuote(x,y[0])
            total += val
            print("change is : " + str(diff))
        print("Total value = $" + str(total))

    
with open("info.json", "r") as read_file:
    data = json.load(read_file)

stocks = data["Stocks"]
amount = data["Amount"]
stockAmount = data["StockAmount"]

me = Account(int(amount), stocks, stockAmount)


while True:
    ins = input("Buy, sell, quote or value?")
    if ins.upper() == "BUY":
        inb = input("Which stock to buy(in stock format)")
        try:
            inba = int(input("How many stocks to buy?"))
        except:
            print("Needs to be integer")
        me.buy(inb, inba)
    elif ins.upper() == "SELL":
        print("Stocks availible to sell: ")
        for x in me.stocks:
            print(x)
        inps = input("Which stock to sell?")
        me.sell(inps.upper())
    elif ins.upper() == "QUOTE":
        inb = input("Which stock to quote(in stock format)")
        try:
            inba = int(input("How many stocks to quote?"))
        except:
            print("Needs to be integer")
        getQuote(inb, inba)
    elif ins.upper() == "VALUE":
        me.value()
    else:
        break

save()
