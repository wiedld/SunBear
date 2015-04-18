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

# GENABILITY API stuff
import requests
import os

GENABILITY_APP_ID = os.environ['GENABILITY_APP_ID']
GENABILITY_API_KEY = os.environ['GENABILITY_API_KEY']
BASE_GENABILITY_URL = 'https://api.genability.com/rest/public/'


def get_from_territory(level, territory_name):
    """This gets data at country, state, county or zipcode level, defined by the 'level'
    function parameter. State name, specific zipcode, etc. defined by the territory_name param.
    Data is returned as a JSON object."""

    # parse the input from the front into a request payload
    if level == "zipcode":
        payload = {"territoryType": "ZIPCODE"}
    elif level == "county":
        payload = {"territoryType": "COUNTY"}

    payload["value"] = territory_name

    # make the request
    r = requests.get(BASE_GENABILITY_URL, auth=(GENABILITY_APP_ID, GENABILITY_API_KEY), params=payload)

    # try/except in case API returns an error. If error, return msg
    # Indicating this. If success, return JSON object.

    try:
        if r.status_code == 200:
            return r.content

    except:
        print "We've encountered an issue fetching the data you requested. Please try again."
        return api_result.status_code


# PV WATTS
#  used python library: https://github.com/mpaolino/pypvwatts
#  output:  Annual and Monthly solar production kWh
#  dataset can = tmy2, tmy3, intl (International station data)
# import os
# from pypvwatts import PVWatts

# PVWatts.api_key = os.environ["PV_WATTS_KEY"]
# result = PVWatts.request(
#         system_capacity=4, module_type=1, array_type=1,
#         azimuth=190, tilt=30, dataset='tmy2',
#         losses=0.13, lat=40, lon=-105)

# print "example PV WATTS annual output:", result.ac_annual
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


data_per_house()



### DETAILS PER NEIGHBORHOOD (or census track) ###
# http://www.zillow.com/howto/api/GetDemographics.htm
# census track data.
# output:   median family income, median home value, avg home size, median age of homeowner, homes with kids, avg year built


def data_neighboorhood():
    import os
    Zillow_key = os.environ["ZILLOW_ZWSID"]

    from urllib2 import Request, urlopen, URLError
    from xml.dom import minidom

    # get data and parse
    url_zillow_neighborhood = "http://www.zillow.com/webservice/GetDemographics.htm?zws-id="+Zillow_key+"&state=WA&city=Seattle&neighborhood=Ballard"
    response = urlopen(url_zillow_neighborhood)
    dom_zillow_neighborhood = minidom.parse(response)


    # retrieve example data by tag
    for node in dom_zillow_neighborhood.getElementsByTagName("attribute"):
        report_type = (handleTok(node.getElementsByTagName("name"))).encode("utf8").strip()

        # neighboorhood values = single family home.
        if report_type=='Median Single Family Home Value':
            neighborhood_node = node.childNodes[1].childNodes[0]
            single_family_home_value = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        # neighboorhood values = single family home.
        if report_type=='Median Home Size (Sq. Ft.)':
            neighborhood_node = node.childNodes[1].childNodes[0]
            median_home_size = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()

        # neighboorhood values = single family home.
        if report_type=='Avg. Year Built':
            neighborhood_node = node.childNodes[1].childNodes[0]
            avg_yr_built = (handleTok(neighborhood_node.getElementsByTagName("value"))).encode("utf8").strip()


    print "Neighborhood value of Single Family Home:", single_family_home_value
    print "Neighborhood median home size:", median_home_size           # 1197 (test case)
    print "Neighborhood avg yr built:", avg_yr_built      # 1995 (test case)


data_neighboorhood()



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


