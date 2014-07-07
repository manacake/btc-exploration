import re
from bs4 import BeautifulSoup as bsoup
import geojson
import pygeoip
from urllib2 import urlopen

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def getIPAddrs(n):
    '''Retrieves n amount of pages from Blockchain's node log
    and grabs all the ip addresses from each page. Inavlid and
    duplicate addresses are removed. Returns a set of IP addresses.'''
    addrs = set() # Holds all our IP Addresses
    base = 'http://blockchain.info/ip-log/'
    # Go through how many pages of bitcoin node log
    for i in range(n):
        url = base + str(i)
        try:
            html = urlopen(url)
        except:
            print 'Could not open url page# {}'.format(i+1)
            break
    
        soup = bsoup(html)
        # Use regex to sift out IP addresses
        uIP = soup.find_all(text = re.compile('([0-9]+)(?:\.[0-9]+){3}'))
        # Get rid of invalid or duplicate IP addresses
        for ip in uIP:
            if len(ip) <= 15:
                addrs.add(ip)
    return addrs

def makeMap(n):
    '''Make a geoJSON map output file from IP addresses.
    Takes in a positive integer n to process n amount of pages
    from Blockchain's node log'''
    addrs = getIPAddrs(n)
    print len(addrs)
    geoMap = {'type': 'FeatureCollection'}
    pointList = []
    
    while (addrs):
        data = {}
        ip = addrs.pop()
    
        ipRecord = gi.record_by_addr(ip)
        longitude = ipRecord['longitude']
        latitude = ipRecord['latitude']
        country = ipRecord['country_name']
        city = ipRecord['city']
        
        data['type'] = 'Feature'
        #longitude,latitude,altitude for coords
        data['geometry'] = {'type': 'Point',
                            'coordinates': [longitude, latitude]}
        data['properties'] = {'city': city,
                              'country': country}
        pointList.append(data)
    
    for p in pointList:
        geoMap.setdefault('features', []).append(p)
    
    out = open('out-geomap', 'w')
    out.write(geojson.dumps(geoMap))
    out.close()
    
def main():
    makeMap(2)
    
if __name__ == '__main__':
    main()