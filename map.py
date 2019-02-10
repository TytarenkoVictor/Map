import folium
from collections import Counter


def file_open(file_name, year):
    '''(str, int) -> (list, list)
    This function open file and return specific data.'''
    f = open(file_name, "r", encoding="UTF-8", errors="ignore")
    lines = f.readlines()
    lst = []
    films_set = set()
    lst1 = []
    for line in lines[15:]:
        if str(year) in line:
                new_line = line.replace("\n", "").split("\t")
                if new_line[0][0:6] not in films_set:
                    films_set.add(new_line[0][0:6])
                    lst.append(new_line)
                else:
                    continue
                if len(new_line[-1]) > 14:
                    lst1.append(new_line[-1])
    f.close()
    return lst, lst1


def coordinats(cities):
    '''list -> (list, list)
    This function recieves list of data and returns list of geo data and list
    of movies.'''
    lst = []
    lst_movies = []
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    for city in cities[0:50]:
        try:
            location = geolocator.geocode(city[-1], timeout=50000)
            lst.append([location.latitude, location.longitude])
            lst_movies.append(city[0].replace("{#", "{"))
        except AttributeError:
            continue
    return lst, lst_movies


def most_common_city(data):
    '''list -> (list, list)
    This function recieves list of data, determines most common cities and
    returns their latitude and longitude and list with films info.'''
    listi = []
    lst_i = []
    count = Counter(data).most_common(5)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    for locat in count:
        try:
            location = geolocator.geocode(locat[0], timeout=50000)
            listi.append([location.latitude, location.longitude])
            lst_i.append(locat)
        except AttributeError:
            continue
    return listi, lst_i


def most_common_countries(inf):
    '''list->list
    This function recieves list of films data and determines top 10 most
    popular countries and returns list of their titles.'''
    lst = []
    lst1 = []
    for elem in inf:
        lst.append(elem.split(",")[-1][1:])
    count = Counter(lst).most_common(10)
    for element in count:
        if element[0] == "USA":
            lst1.append("United States")
        elif element[0] == "UK":
            lst1.append("United Kingdom")
        else:
            lst1.append(element[0])
    return lst1


def f(x, lst):
    '''(dict, list) -> dict
    This function recieves dictionary with countries data and list of countries
    titles and returns dictionary with color data.'''
    y = {}
    if x['properties']['NAME'] in lst:
        y = {'fillColor': 'orange'}
    return y


if __name__ == "__main__":
    try:
        user = int(input("Enter year(1910 - 2019):"))
        if user <= 2019 and user >= 1910:
            map = folium.Map(location=[48.314775, 25.082925], zoom_start=1)
            fg_hc = folium.FeatureGroup(name="Movies by year")
            for cor, mov in zip(coordinats(file_open("locations.list", user)[0])[0], coordinats(file_open("locations.list", user)[0])[1]):
                fg_hc.add_child(folium.CircleMarker(location=cor, radius=10, popup=str(mov), fill_color='red', color='red', fill_opacity=0.5))
            fg_pp = folium.FeatureGroup(name="Top locations by year")
            for loc, tit in zip(most_common_city(file_open("locations.list", user)[1])[0], most_common_city(file_open("locations.list", user)[1])[1]):
                fg_pp.add_child(folium.Marker(location=loc, popup=str(tit), icon=folium.Icon()))
            f3_pp = folium.FeatureGroup(name="Top 10 countries")
            cont = most_common_countries(file_open("locations.list", user)[1])
            f3_pp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function= lambda x: f(x, cont)))
            map.add_child(fg_hc)
            map.add_child(fg_pp)
            map.add_child(f3_pp)
            map.add_child(folium.LayerControl())
            map.save("Map.html")
        else:
            print("Incorrect input")
    except ValueError:
        print("Incorrect input")
