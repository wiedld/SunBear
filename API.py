""" This file is divide into sections.  Each section refers to a different API source (zillow vs. pvwatts, etc).   A few sections have multiple APIs (eg. zillow has ~10 APIs).

    Each API has link to the source materials/description.  Also has a brief description of inputs and outputs."""


# helper functions for parsing

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def handleTok(tokenlist):
    texts = ""
    for token in tokenlist:
        texts += " "+ getText(token.childNodes)
    return texts

###############################################################
###############################################################

# PV WATTS
#  used python library: https://github.com/mpaolino/pypvwatts
#  output:  Annual and Monthly solar production kWh
#  dataset can = tmy2, tmy3, intl (International station data)
import os
from pypvwatts import PVWatts

PVWatts.api_key = os.environ["PV_WATTS_KEY"]
result = PVWatts.request(
        system_capacity=4, module_type=1, array_type=1,
        azimuth=190, tilt=30, dataset='tmy2',
        losses=0.13, lat=40, lon=-105)

print "example PV WATTS annual output:", result.ac_annual
# (wiedld): this API is wired in and working!!!!

###############################################################

# ZILLOW

### DETAILS PER HOUSE ###
# http://www.zillow.com/howto/api/GetDeepSearchResults.htm
# input:  address and zip
# output: lattitude and longitude (could then be inputed into PV WATTS)
#           valutation range (high and low)
#           home value index -- avg home value in neighborhood?
#           ZPID = a zillow id (per house). used for the other zillow APIs.
#           Tax assessment,Yearbuilt,lotsizeSqFt,finishedSqFt,Bedrooms
#  *** FIPScounty *** = matches county codes in maps, census data, etc


def data_per_house():
    import os
    Zillow_key = os.environ["ZILLOW_ZWSID"]

    from urllib2 import Request, urlopen, URLError
    from xml.dom import minidom

    # get data and parse
    url_zillow_house = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id="+Zillow_key+"&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA"
    response = urlopen(url_zillow_house)
    dom_zillow_house = minidom.parse(response)


    # retrieve example data by tag
    for node in dom_zillow_house.getElementsByTagName("result"):

        latitude = (handleTok(node.getElementsByTagName('latitude'))).encode("utf8").strip()
        longitude = (handleTok(node.getElementsByTagName('longitude'))).encode("utf8").strip()
        finishedSqFt = (handleTok(node.getElementsByTagName('finishedSqFt'))).encode("utf8").strip()
        bedrooms = (handleTok(node.getElementsByTagName('bedrooms'))).encode("utf8").strip()
        yearBuilt = (handleTok(node.getElementsByTagName('yearBuilt'))).encode("utf8").strip()
        taxAssessment = (handleTok(node.getElementsByTagName('taxAssessment'))).encode("utf8").strip()
        FIPScounty = (handleTok(node.getElementsByTagName('FIPScounty'))).encode("utf8").strip()

    print "latitude:", latitude
    print "longitude:", longitude
    print "Square feet:", finishedSqFt
    print "number of bedrooms:", bedrooms
    print "year built:", yearBuilt
    print "tax assessment:", taxAssessment
    print "county code:", FIPScounty


# data_per_house()



### DETAILS PER NEIGHBORHOOD (or census track) ###
# http://www.zillow.com/howto/api/GetDemographics.htm
# census track data.
# output:   median family income, median home value, avg home size, median age of homeowner, homes with kids, avg year built


def data_neighborhood():
    import os
    Zillow_key = os.environ["ZILLOW_ZWSID"]

    from urllib2 import Request, urlopen, URLError
    from xml.dom import minidom

    # get data and parse
    # url_zillow_neighborhood = "http://www.zillow.com/webservice/GetDemographics.htm?zws-id="+Zillow_key+"&zip=94501"
    url_zillow_neighborhood = "http://www.zillow.com/webservice/GetDemographics.htm?zws-id="+Zillow_key+"&state=WA&city=Seattle&neighborhood=Ballard"

    response = urlopen(url_zillow_neighborhood)
    dom_zillow_neighborhood = minidom.parse(response)


    # retrieve example data by tag
    for node in dom_zillow_neighborhood.getElementsByTagName("attribute"):
        report_type = (handleTok(node.getElementsByTagName("name"))).encode("utf8").strip()

        if report_type=='Median Household Income':
            neighborhood_node = node.childNodes[1].childNodes[0]
            median_household_income = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        if report_type=='Median Home Size (Sq. Ft.)':
            neighborhood_node = node.childNodes[1].childNodes[0]
            median_home_size = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        if report_type=='Avg. Year Built':
            neighborhood_node = node.childNodes[1].childNodes[0]
            avg_yr_built = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        if report_type=='Average Household Size':
            neighborhood_node = node.childNodes[1].childNodes[0]
            avg_household_size = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        if report_type=='Owners':
            neighborhood_node = node.childNodes[1].childNodes[0]
            owners_pct = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        if report_type=='Renters':
            neighborhood_node = node.childNodes[1].childNodes[0]
            renters_pct = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()


    print "median_household_income:", median_household_income   # 44512.013
    print "Neighborhood median home size:", median_home_size           # 1197 (test case)
    print "Neighborhood avg yr built:", avg_yr_built      # 1995 (test case)
    print "avg_household_size:", avg_household_size     # 2.58883240
    print "owners_pct:", owners_pct                 # 0.66268764
    print "renters_pct:", renters_pct               # 0.33731236



# data_neighborhood()


# get neighborhoods in Alameda CA
# http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=X1-ZWz1er05pybo5n_2t4xn&state=CA&county=Alameda



def neighborhoods_in_county():
    import os
    Zillow_key = os.environ["ZILLOW_ZWSID"]

    from urllib2 import Request, urlopen, URLError
    from xml.dom import minidom

    url_zillow_neighborhood = "http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id="+Zillow_key+"&state=CA&county=Alameda"

    response = urlopen(url_zillow_neighborhood)
    dom_zillow_neighborhood = minidom.parse(response)


    # need only region tags in the list
    list_regions = dom_zillow_neighborhood.getElementsByTagName("list")

    for node in dom_zillow_neighborhood.getElementsByTagName("region"):
        name = (handleTok(node.getElementsByTagName("name"))).encode("utf8").strip()
        latitude = (handleTok(node.getElementsByTagName("latitude"))).encode("utf8").strip()
        longitude = (handleTok(node.getElementsByTagName("longitude"))).encode("utf8").strip()

        print "NEW NEIGHBORHOOD"
        print name
        print latitude
        print longitude



neighborhoods_in_county()





###############################################################
# OTHER ZILLOW APIs - tbd if team sees a useful purpose for data.


# http://www.zillow.com/howto/api/GetSearchResults.htm
# input:  address and zip
# output: lattitude and longitude (could then be inputed into PV WATTS)
#           valutation range (high and low)
#           home value index -- avg home value in neighborhood?
#           ZPID = a zillow id (per house). used for the other zillow APIs.


# http://www.zillow.com/howto/api/GetDeepComps.htm
# input:  zpid, and num of sales to compare (make up =1)
# output: Tax assessment,Yearbuilt,lotsizeSqFt,finishedSqFt,Bedrooms


# http://www.zillow.com/howto/api/GetUpdatedPropertyDetails.htm
# relator updated details.  Can have roof, heating sources, etc.  But this data is not provided for all homes -- so not standard.  not for MVP.


###############################################################

# NOAA
# python packages:
# https://pypi.python.org/pypi?%3Aaction=search&term=noaa&submit=search
import os
Noaa_token = os.environ["NOAA_TOKEN"]
# print Noaa_token
# (wiedld): not sure yet if we'll use this api.  TBD - discuss with team.


