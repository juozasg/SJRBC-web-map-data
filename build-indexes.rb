require "rgeo"
require 'csv'
require 'rgeo/geo_json'

puts "Yay" if RGeo::Geos.capi_supported?

file = 'geojson/huc10.geojson'
features = RGeo::GeoJSON.decode(File.read(file))
rows = CSV.read('sites/sites.csv', headers: true)

indexRows = ['siteId','huc10']

factory = RGeo::Geographic.spherical_factory
rows.each do |row|
	point = factory.point(row['lon'].to_f, row['lat'].to_f)
	matching_feature = features.find { |feature| feature.geometry.contains?(point) }
	huc10 = matching_feature ? matching_feature['huc10'] : ''
	index = row['siteId'] + ',' + huc10
	# puts index
	indexRows << index
end

File.write('indexes/sites.csv', indexRows.join("\n"))


