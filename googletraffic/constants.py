"""
Constants for traffic color detection and classification.
"""

# Traffic level definitions (based on Google Maps colors)
TRAFFIC_LEVELS = {
    1: "No traffic (Green)",
    2: "Medium traffic (Orange)",
    3: "High traffic (Red)",
    4: "Heavy traffic (Dark Red)",
}

# RGB color ranges for traffic detection (approximate values)
# These ranges help identify traffic colors in screenshots
TRAFFIC_COLORS = {
    1: {  # Green - no traffic
        "name": "green",
        "rgb_center": (99, 197, 124),
        "tolerance": 40,
    },
    2: {  # Orange - medium traffic
        "name": "orange",
        "rgb_center": (242, 139, 52),
        "tolerance": 40,
    },
    3: {  # Red - high traffic
        "name": "red",
        "rgb_center": (240, 70, 70),
        "tolerance": 40,
    },
    4: {  # Dark Red - heavy traffic
        "name": "dark_red",
        "rgb_center": (129, 31, 31),
        "tolerance": 40,
    },
}

# Google Maps zoom levels and approximate meters per pixel
# Source: https://wiki.openstreetmap.org/wiki/Zoom_levels
ZOOM_SCALES = {
    0: 156543.03,  # World
    1: 78271.52,
    2: 39135.76,
    3: 19567.88,
    4: 9783.94,
    5: 4891.97,
    6: 2445.98,
    7: 1222.99,
    8: 611.50,
    9: 305.75,
    10: 152.87,
    11: 76.44,
    12: 38.22,
    13: 19.11,
    14: 9.55,
    15: 4.78,
    16: 2.39,  # Street level
    17: 1.19,
    18: 0.60,
    19: 0.30,
    20: 0.15,  # Building level
}

# Default map tile size in pixels (standard for most mapping APIs)
TILE_SIZE = 640

# HTML template for Google Maps with traffic layer
GOOGLE_MAPS_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Google Maps Traffic</title>
    <style>
        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        #map {{
            height: 100%;
            width: 100%;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        let map;
        let trafficLayer;

        function initMap() {{
            map = new google.maps.Map(document.getElementById("map"), {{
                center: {{ lat: {lat}, lng: {lng} }},
                zoom: {zoom},
                mapTypeId: 'roadmap',
                disableDefaultUI: true,
                styles: [
                    {{
                        featureType: "poi",
                        stylers: [{{ visibility: "off" }}]
                    }},
                    {{
                        featureType: "transit",
                        stylers: [{{ visibility: "off" }}]
                    }}
                ]
            }});

            trafficLayer = new google.maps.TrafficLayer();
            trafficLayer.setMap(map);

            // Signal that map is ready
            window.mapReady = true;
        }}

        window.initMap = initMap;
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap&libraries=&v=weekly" async></script>
</body>
</html>
"""
