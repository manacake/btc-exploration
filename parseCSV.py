import os
import urllib2
import csv

def parse(csvFile, sep):
    '''Parses a market-price CSV from Blockchain's API into JSON-format.'''
    outFile = open('jsonFile', 'w')
    # Returns an iterator over the file
    csvData = csv.reader(csvFile, delimiter = sep)
    jsonData = [] # Our JSON data
    # Headers for our CSV (if applicable)
    headers = ['Date', 'Time', 'Market Price']
    # Or get headers from the 0th row of csv file
    # headers = csvData.next()
    
    outFile.write('[')
    for row in csvData:
        row = row[0].split() + row[1:]
        outFile.write('{},'.format(dict(zip(headers, row))))
        jsonData.append(dict(zip(headers, row)))
    # Seek relative to EOF, backward -1
    outFile.seek(-1, os.SEEK_END)
    outFile.truncate()
    outFile.write(']')
    outFile.close()
    
    return jsonData

def getFile():
    url = 'http://blockchain.info/charts/market-price?showDataPoints=false&timespan=&show_header=true&daysAverageString=1&scale=0&format=csv&address='
    return urllib2.urlopen(url)

def main():
    csvFile = getFile()
    jsonData = parse(csvFile, ',')
    csvFile.close()
    
if __name__ == '__main__':
    main()