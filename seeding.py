import model
import csv
from datetime import datetime



def load_geographics():
    with open('seed_data/zip_code_database.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        for row in reader:
            print ("row:", row)
            # row = troubleshooting.  If issue, see where.
            try:
                session=model.connect()
                geo_obj = model.Geographic()

                geo_obj.zipcode = row[0]
                geo_obj.type_addy = row[1]
                geo_obj.primary_city = row[2]
                geo_obj.acceptable_cities = row[3]
                geo_obj.unacceptable_cities = row[4]
                geo_obj.state = row[5]
                geo_obj.county = row[6]
                geo_obj.timezone = row[7]
                geo_obj.area_codes = row[8]
                geo_obj.latitude = float(row[9])
                geo_obj.longitude = float(row[10])
                geo_obj.world_region = row[11]
                geo_obj.country = row[12]
                geo_obj.decommissioned = row[13]
                geo_obj.estimated_population = int(row[14])
                geo_obj.notes = row[15]

                session.add(geo_obj)
                session.commit()
            except:
                print "Error for row data:", row
                f = open('log_file.txt','a')
                f.write("\nError.  failure for row:"+str(row))
                f.close




def load_demographics():
    with open('seed_data/SlimmerData_Consolidated.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        for row in reader:
            print "row:", row
            # row = troubleshooting.  If issue, see where.
            try:
                session=model.connect()
                demo_obj = model.Demographic()

                demo_obj.zipcode = row[0]
                demo_obj.popdensity = float(row[1])
                demo_obj.pctemployed = float(row[2])
                demo_obj.pctmnf = float(row[3])
                demo_obj.pctlogistics = float(row[4])
                demo_obj.pctit = float(row[5])
                demo_obj.pctprof = float(row[6])
                demo_obj.hhincq10 = int(row[7])
                demo_obj.hhincq30 = int(row[8])
                demo_obj.hhincq50 = int(row[9])
                demo_obj.hhincq70 = int(row[10])
                demo_obj.hhincq90 = int(row[11])
                demo_obj.hhincq95 = int(row[12])
                demo_obj.pctheatelec = float(row[13])

                session.add(demo_obj)
                session.commit()
            except:
                print "Error for row data:", row
                f = open('log_file.txt','a')
                f.write("\nError. Failure for row:"+str(row))
                f.close



def main():
    """this contains all the different functions for seeding.  Comment out when seeding is complete"""
    load_geographics()
    load_demographics()




if __name__ == "__main__":
    main()