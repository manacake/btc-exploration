from collections import defaultdict
from datetime import datetime
from numpy import mean
import matplotlib.pyplot as plt
from parseCSV import parse,getFile 

def avgPriceDay(jsonData):
    '''Gives the average price (US Dollars) of each \
    day of the week in the span of a given year'''
    averages = {}
    days = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
    dayNum = dict(enumerate(days))
    dayPrices = defaultdict(list)
    
    # Make a list of prices for each day of the week in dict
    for entry in jsonData:
        price = float(entry['Market Price'])
        date = entry['Date'].split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
   
        #Get an int for Mon = 0 to Sun = 6
        dayZeroSix = datetime(year, month, day).weekday()
        #Get mon-sun depending on passed int
        dayOfWeek = dayNum[dayZeroSix]
        #Contain all prices for each day of week
        dayPrices[dayOfWeek].append(price)
    
    # Get average prices for each day of week
    averages = [mean(dayPrices[d]) for d in days]
    
    plt.plot(averages, 'g')
    plt.xticks(range(7), tuple(days))
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Price (US Dollars)')
    plt.savefig('avgDays.png')
    plt.clf() # Clear current figure

def main():
    jsonData = parse(getFile(), ',')
    avgPriceDay(jsonData)

if __name__ == '__main__':
    main()