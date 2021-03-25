def daySeparator(filepath):
    with open(filepath,'r') as r:
        # lines will help us keep track of when we're moving to the next record set
        lines = [x.strip() for x in r.readlines()]
        # The variable i will help us terminate each while loop
        i = 1
        firstDay = dict()
        while lines[i] != '':
            stockRecord = lines[i].split(' ')
            firstDay[stockRecord[0]] = float(stockRecord[1])
            i += 1
        i += 1
        transactionHeader = lines[i]
        transactions = dict()
        transactions[transactionHeader] = dict()
        i += 1
        while lines[i] != '':
            transactionRecord = lines[i].split(' ')
            symbol,transactionCode,shares,totalValue = transactionRecord
            if symbol not in firstDay.keys():
                firstDay[symbol] = 0
            if symbol == 'Cash':
                if transactionCode == 'DEPOSIT':
                    firstDay[symbol] += float(totalValue)
                elif transactionCode == 'FEE':
                    firstDay[symbol] -= float(totalValue)
            else:
                if transactionCode == 'SELL':
                    firstDay[symbol] -= float(shares)
                    firstDay['Cash'] += float(totalValue)
                elif transactionCode == 'BUY':
                    firstDay[symbol] += float(shares)
                    firstDay['Cash'] -= float(totalValue)
                elif transactionCode == 'DIVIDEND':
                    firstDay['Cash'] += float(totalValue)
            i += 1
        i += 2
        reconOut = ''
        while i < len(lines):
            stockRecord = lines[i].split(' ')
            symbol,shares = stockRecord
            try:
                if float(shares) != firstDay[symbol]:
                    nextLine = f"{symbol} {float(shares) - firstDay[symbol]}\n"
                    reconOut += nextLine
                firstDay.pop(symbol)
            except KeyError:
                if symbol not in firstDay.keys():
                    reconOut += f"{symbol} {float(shares)}\n"
            i += 1
        for item in firstDay.items():
            if item[1] != 0:
                reconOut += f"{item[0]} {item[1]}\n"
        with open('recon.out','w+') as w:
            w.write(reconOut)

def main():
    daySeparator('data.txt')
main()