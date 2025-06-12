# using shapely open states.geojson file and find if each feature polygons the point (lat, lon)
import json
from itertools import chain
from shapely.geometry import shape, Point, Polygon, MultiPolygon

# get a list of Point coordinates from sites.geojson
sitesFeatures = json.load(open('geojson/site.geojson', 'r'))['features']
siteLonLat: dict[int, Point] = {}

print("TOTAL NUMBER sites:", len(sitesFeatures))
print("First site:", sitesFeatures[0])

for feature in sitesFeatures:
    siteId = feature['properties']['id']
    coordinates = feature['geometry']['coordinates']
    siteLonLat[siteId] = Point(coordinates[0], coordinates[1])


# def polygonContainsPoint(feature, point):
#     """Check if a polygon contains a point."""
#     # print("poly test", feature)
#     if feature['geometry']['type'] != 'Polygon':
#         return False
#     polygon = shape(feature['geometry'])
#     return shape(polygon).contains(point)

# # shapely return true if geojson multipolygon contains point
# def multiPolygonContainsPoint(feature, point):
#     """Check if a multipolygon contains a point."""
#     if feature['geometry']['type'] != 'MultiPolygon':
#         return False
#     multiPolygon = shape(feature['geometry'])
#     return multiPolygon.contains(point)


def sitesIdsInFeature(feature):
    """Return a list of site IDs that are in the given feature."""
    # print("Feature ID:", feature['properties']['id'])
    # print("sites", siteLonLat.items())
    return [siteId for siteId, point in siteLonLat.items() \
        if shape(feature['geometry']).contains(point)]



# def pointInFeature(feature, point):



def indexFeatureCollection(regionType: str):
    featureSiteIds: dict[int, list[int]] = {}

    with open(f"geojson/{regionType}.geojson", 'r') as f:
        data = json.load(f)
        num = len(data['features'])
        n = 1
        print(f"Number of {regionType}s:", num)
        for feature in data['features']:
            featureId = feature['properties']['id']
            featureSiteIds[featureId] = sitesIdsInFeature(feature)
            if(regionType == 'site-catchment' and featureId not in featureSiteIds[featureId]):
                featureSiteIds[featureId].append(featureId)  # Ensure site contains site catchment itself
                print(f"Site catchment {featureId} added to site")
            print(f"Indexed {n}/{num} {regionType}", end='\r')
            n += 1
    return featureSiteIds


def flatten(xss):
    return [x for xs in xss for x in xs]

if __name__ == "__main__":
    print("-----------  build-indexes.py  -------------")
    for regionType in ['site-catchment', 'river-catchment', 'state', 'county', 'huc8', 'huc10', 'huc12']:
        featureSiteIds = indexFeatureCollection(regionType)
        allSiteIds = flatten(list(featureSiteIds.values()))

        print(featureSiteIds)
        json.dump(featureSiteIds, open(f'indexes/{regionType}.json', 'w'), indent=None)
        print(f"Wrote indexes/{regionType}.json")
