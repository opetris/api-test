import uvicorn
from fastapi import FastAPI
import json
from haversine import haversine

def define_app():
    app = FastAPI()

    #-------Mise en forme base resto---------------
    # Opening JSON file
    resto_ref = open('restaurants_paris.geojson')

    # returns JSON object as a dictionary
    resto_ref_json = json.load(resto_ref)

    # Get list from restau_paris
    resto_list = resto_ref_json['features']

    # restos list with coordinates
    resto_list_short = [(i['properties']['name'],(float(i['geometry']['coordinates'][1]),float(i['geometry']['coordinates'][0]))) for i in resto_list]

    #--------- Function resto around customer point ----------

    def getrestolist(lat,long,rad):
        search_result = []
        customer_point = (lat,long)
        print(customer_point)


        for point in resto_list_short:
            d = haversine(customer_point, point[1])
            print(point[1])
            print(d)
            d_conv = d*(10**3)
            if d_conv <= rad:
                search_result.append((point,d_conv))
        return search_result


    #------ Retrieve resto list next to the customer ----------------

    @app.get("/search/")
    def search_resto(lat: float, long:float, rad:float):
        result = getrestolist(lat, long ,round(rad))
        return result

    return app

app = define_app()

def launch_server():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":

    launch_server()


# link
#/search/?lat=48.8319929&long=2.3245488&rad=100

# example
#latitude=48.8319929 longitude=2.3245488 radius=100
