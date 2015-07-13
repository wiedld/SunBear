from pandas import DataFrame
import unicodedata


# when launching server.py, this statement prints to confirm is connected
test = "pandas is connected"


###########################################################################
##########################################################################
# FUNCTIONS SPECIFIC FOR NEIGHBORHOOD MAP

# currently the db lists only zips for Alameda
def retrieve_neighborhood_zips(county_name):
    import model
    s = model.connect()

    # retrive a list of the zip codes
    cmd = 'SELECT zipcode FROM Geographics WHERE county="%s" '
    zipcode_obj = s.execute(cmd, (county_name))
    zipcode_data = zipcode_obj.fetchall()

    print zipcode_data

    # df_dec2013 = DataFrame(CA_gen_dec13_data)

    # # now convert into dict, so caan easily add county to other df.
    # dict_counties={}
    # for idx, row in enumerate(df_counties.values):
    #     plant_name, county = row
    #     # clean the county name
    #     county = unicodedata.normalize('NFKD',county).encode('ascii','ignore')
    #     county = county.lower().title()
    #     county = county.replace(" County","")
    #     dict_counties[plant_name] = county


retrieve_neighborhood_zips("Alameda")


