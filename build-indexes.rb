require "rgeo"
puts "Yay" if RGeo::Geos.capi_supported?


require 'rgeo/geo_json'


# str1 = '{"type":"Point","coordinates":[1,2]}'
# file = 'geojson/counties.geojson'
file = 'geojson/huc10.geojson'
json = RGeo::GeoJSON.decode(File.read(file))
f = json[0]
f['huc10']



require 'csv'
CSV.read("sites.csv")


