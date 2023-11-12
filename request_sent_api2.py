from sentinelhub import SHConfig, SentinelHubRequest, MimeType, CRS, BBox, SentinelHubDownloadClient

# Set up your Sentinel Hub API key
config = SHConfig()
client_id = 'cbbc4a7d-cad7-44b2-92e9-00489b945b62'
client_secret = 'rtdgkVVhPnanYQGXPn8URSZI6V1pafGcTT395yfV'

config.sh_client_id = client_id
config.sh_client_secret = client_secret

# Define the bounding box and time range for the request
bbox = BBox(bbox=[-122.5, 37.5, -122, 38], crs=CRS.WGS84)
time_interval = ('2022-01-01', '2022-01-10')

# Create a request for Sentinel-2 data
# Create a request for Sentinel-2 data
request = SentinelHubRequest(
   evalscript="""
       // your custom evalscript goes here
       // e.g., return [B08, B04, B03]; // for true color visualization
   """,
   input_data=[
       {
           'dataFilter': {
               'data_source': 'sentinel-2-l2a',
               'timeRange': {'from': '2022-01-01T00:00:00Z', 'to': '2022-01-10T23:59:59Z'},
               'maxCloudCoverage': 10  # maximum cloud coverage
           },
           'processing': {
               'upsampling': 'BICUBIC',
               'downsampling': 'BICUBIC'
           }
       }
   ],
   responses=[
       SentinelHubRequest.output_response('default', MimeType.TIFF)
   ],
   bbox=bbox,
   size=(512, 512),  # specify the image size
   config=config
)

# Execute the request and download the image
download_request = SentinelHubDownloadClient(config=config)
image = download_request(request)

# Save the image to a file or process it further as needed
image.save('output_image.tiff')