def daySeparator(filepath):
    with open(filepath,'r') as r:
        # lines will help us keep track of when we're moving to the next record set
        lines = [x.strip() for x in r.readlines()]
        i = 0
        firstDay = lines[i]
        days = dict()
        days[firstDay] = dict()
        i += 1
        while lines[i] != '':
            stockRecord = lines[i].split(' ')
            days[firstDay][stockRecord[0]] = float(stockRecord[1])
            i += 1
        i += 1
        transactionHeader = lines[i]
        transactions = dict()
        transactions[transactionHeader] = dict()
        i += 1
        while lines[i] != '':
            transactionRecord = lines[i].split(' ')
            symbol,transactionCode,shares,totalValue = transactionRecord
            if symbol not in days[firstDay].keys():
                days[firstDay][symbol] = 0
            if symbol == 'Cash':
                if transactionCode == 'DEPOSIT':
                    days[firstDay][symbol] += float(totalValue)
                elif transactionCode == 'FEE':
                    days[firstDay][symbol] -= float(totalValue)
            else:
                if transactionCode == 'SELL':
                    days[firstDay][symbol] -= float(shares)
                    days[firstDay]['Cash'] += float(totalValue)
                elif transactionCode == 'BUY':
                    days[firstDay][symbol] += float(shares)
                    days[firstDay]['Cash'] -= float(totalValue)
                elif transactionCode == 'DIVIDEND':
                    days[firstDay]['Cash'] += float(totalValue)
            i += 1
        i += 2
        reconOut = ''
        while i < len(lines):
            stockRecord = lines[i].split(' ')
            symbol,shares = stockRecord
            try:
                if float(shares) != days[firstDay][symbol]:
                    nextLine = f"{symbol} {float(shares) - days[firstDay][symbol]}\n"
                    reconOut += nextLine
                days[firstDay].pop(symbol)
            except KeyError:
                if symbol not in days[firstDay].keys():
                    reconOut += f"{symbol} {float(shares)}\n"
            i += 1
        for item in days[firstDay].items():
            if item[1] != 0:
                reconOut += f"{item[0]} {item[1]}\n"
        with open('recon.out','w+') as w:
            w.write(reconOut)

def main():
    daySeparator('data.txt')
main()