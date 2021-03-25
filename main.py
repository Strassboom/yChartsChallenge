#def dayParser(lines,dayName,index):
    

def daySeparator(filepath):
    with open(filepath,'r') as r:
        lines = [x.strip() for x in r.readlines()]
        i = 0
        firstDay = lines[i]
        dayList = [firstDay]
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
        i += 1
        nextDay = lines[i]
        dayList.append(nextDay)
        days[nextDay] = dict()

        print(lines)

def main():
    daySeparator('data.txt')
main()