from flask import Flask, render_template, redirect, request, jsonify
#import model
#import API
import os

app = Flask(__name__)
app.secret_key = os.environ["flask_app_key"]

@app.route("/county_map")
def county_map():
    """rendering the county-map. has js file with insertion of interactive d3 elements (slider, donut)."""

    return render_template("county_map.html")




@app.route("/county-map-data", methods=['POST'])
def county_map_data():
    """get data for topojson map of counties.  Called during initial rendering."""
    chosen_state = request.data
    # print "CHOSEN STATE:", chosen_state

    data_for_topojson = pdm.fuel_mix_for_map(chosen_state)
    # print "DATA FOR MAP: \n", data_for_topojson
    return jsonify(data_for_topojson)




@app.route("/scenario-result", methods=['POST'])
def scenario_result():
    """Take data structure from frontend, pipe through binary_decision_tree, return result to front."""

    from calculations import binary_decision_tree as bdt
    print bdt.test

    user_input = request.json
    result = bdt.bdt_on_user_input(user_input)

    return jsonify(result)


#########################################################
#########################################################
# USA MAP -- CLICK ON STATES

@app.route("/usa_map")
def usa_map():
    """rendering the usa-map. has js file with insertion of interactive d3 elements (slider, donut)."""

    return render_template("usa_map.html")




@app.route("/usa-map-data", methods=['POST'])
def usa_map_data():
    """get data for topojson map of counties.  Called during initial rendering."""

    data_for_topojson = pdm.fuel_mix_for_map_usa()
    return jsonify(data_for_topojson)




@app.route("/scenario-result-usa", methods=['POST'])
def scenario_result_usa():
    """Take data structure from frontend, pipe through binary_decision_tree, return result to front."""

    from calculations import binary_decision_tree as bdt
    print bdt.test

    user_input = request.json
    result = bdt.bdt_on_user_input_usa(user_input)

    return jsonify(result)



#########################################################
#########################################################
#  CURRENT MIX


@app.route("/current")
def current_mix():
    """renders the page immediately"""

    return render_template("current_mix.html")




@app.route("/current-mix-data", methods=['POST'])
def current_mix_data():
    """mix is pulled in seperately.  should come from cache"""

    global cached_current_mix
    return jsonify(cached_current_mix)



# test with every 30 seconds.  Once working, move to every 5 minutes
#@cache.cached(timeout=30, key_prefix='fuel_mix_for_cache')
@app.route("/get-fuel-mix-for-cache")
def get_fuel_mix_for_cache():
    """Called regularily by the cache function.  Gets the current fuel mix, and pipe through to frontend object"""

    solar, wind = RT_scrape.get_solar_wind()
    demand = RT_scrape.get_demand()

    global cached_current_mix
    cached_current_mix = ML.predict_current_mix(solar,wind,demand)





###########################################################
###########################################################
# ABOUT

@app.route("/about")
def about_HB_project():
    """Explains how the under-the-cover works."""

    return render_template("about.html")



#########################################################
#########################################################



def main():
    """populate the cache for the first time."""
    #get_fuel_mix_for_cache()
    global cached_current_mix

    solar, wind = RT_scrape.get_solar_wind()
    demand = RT_scrape.get_demand()

    cached_current_mix = ML.predict_current_mix(solar,wind,demand)
    print ("cached current mix:", cached_current_mix)


def main():
    pass



if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)

