import sys

def dayReconciler(inPath,outPath):
    with open(inPath,'r') as r:
        # lines will help us keep track of when we're moving to the next record set
        lines = [x.strip() for x in r.readlines()]
        # The variable i will help us terminate each while loop
        i = 1

        # Assign the shares on day 0 to a key of their respective symbol in a dictionary
        firstDay = dict()
        while lines[i] != '':
            stockRecord = lines[i].split(' ')
            firstDay[stockRecord[0]] = float(stockRecord[1])
            i += 1
        i += 2

        # Perform transaction operations on the symbols and shares in day 0
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

        # Compare Day 0 after transactions with records for Day 1 and append the error value record to reconOut if inequal
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
        
        # Append the value record of any stock symbols from Day 0 not in Day 1, as this indicates further inconsistencies
        for item in firstDay.items():
            if item[1] != 0:
                reconOut += f"{item[0]} {item[1]}\n"
        # Write reconOut to recon.out
        with open(outPath,'w+') as w:
            w.write(reconOut)

def main():
    # Read in optional file input and output paths
    inPath = sys.argv[1] if len(sys.argv) > 1 else 'recon.in'
    outPath = sys.argv[2] if len(sys.argv) > 2 else 'recon.out'
    dayReconciler(inPath,outPath)
main()