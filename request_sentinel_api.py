import requests
# Get access token

# Your client credentials
client_id = 'cbbc4a7d-cad7-44b2-92e9-00489b945b62'
client_secret = 'rtdgkVVhPnanYQGXPn8URSZI6V1pafGcTT395yfV'
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}

response = requests.post('https://services.sentinel-hub.com/oauth/token', data=token_data)
access_token = response.json().get("access_token")

# Sentinel Hub API request
api_url = "https://services.sentinel-hub.com/api/v1/process"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "multipart/form-data",
}

data = {
    "request": {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-94.04798984527588, 41.7930725281021],
                            [-94.04803276062012, 41.805773608962869],
                            [-94.06738758087158, 41.805901566741308],
                            [-94.06734466552735, 41.7967199475024],
                            [-94.06223773956299, 41.79144072064381],
                            [-94.0504789352417, 41.791376727347969],
                            [-94.05039310455322, 41.7930725281021],
                            [-94.04798984527588, 41.7930725281021],
                        ]
                    ],
                },
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": "2022-10-01T00:00:00Z",
                            "to": "2022-10-31T00:00:00Z",
                        }
                    },
                }
            ],
        },
        "output": {
            "width": 512,
            "height": 512,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/jpeg",
                        "quality": 80,
                    },
                }
            ],
        },
    },
    "evalscript": """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands:["B04", "B08"],
                }],
                output: {
                    id: "default",
                    bands: 3,
                }
            }
        }

        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)

            if (ndvi<-0.5) return [0.05,0.05,0.05]
            else if (ndvi<-0.2) return [0.75,0.75,0.75]
            // Add the rest of your conditions here...

        }
    """,
}

response = requests.post(api_url, headers=headers, data=data)

# Print the response
print(response.text)