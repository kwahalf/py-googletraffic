"""
Simple example script demonstrating py-googletraffic usage.
"""

import googletraffic as gt
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# IMPORTANT: Set your Google Maps API key here
# Get one at: https://developers.google.com/maps/get-started
GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

# Or use environment variable:
# import os
# GOOGLE_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def main():
    """Main function to demonstrate traffic raster creation."""
    
    # Define location (Times Square, NYC)
    location = (40.7580, -73.9855)  # (latitude, longitude)
    
    print("Creating traffic raster for Times Square, NYC...")
    print("This will take a few seconds to capture the map...")
    
    # Create traffic raster
    traffic_raster = gt.make_raster(
        location=location,
        height=1000,
        width=1000,
        zoom=14,  # City-level detail
        google_key=GOOGLE_API_KEY,
        wait_time=3  # Wait 3 seconds for traffic layer to load
    )
    
    print(f"✓ Raster created with shape: {traffic_raster.shape}")
    
    # Analyze traffic
    traffic_pixels = traffic_raster[traffic_raster > 0]
    
    if len(traffic_pixels) > 0:
        print("\nTraffic Statistics:")
        print(f"  - Total traffic pixels: {len(traffic_pixels):,}")
        print(f"  - Mean traffic level: {traffic_pixels.mean():.2f}")
        print(f"  - Median traffic level: {np.median(traffic_pixels):.2f}")
        
        print("\nTraffic distribution:")
        level_names = ['', 'No traffic', 'Medium', 'High', 'Heavy']
        for level in range(1, 5):
            count = np.sum(traffic_raster == level)
            percentage = (count / len(traffic_pixels)) * 100
            print(f"  - Level {level} ({level_names[level]}): {count:,} pixels ({percentage:.1f}%)")
    
    # Visualize
    print("\nCreating visualization...")
    
    # Define colors matching Google Maps
    colors = ['white', 'green', 'orange', 'red', 'darkred']
    cmap = ListedColormap(colors)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Traffic map
    im = ax1.imshow(traffic_raster, cmap=cmap, vmin=0, vmax=4)
    ax1.set_title('Traffic Conditions Around Times Square, NYC', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Pixel X')
    ax1.set_ylabel('Pixel Y')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax1, ticks=[0, 1, 2, 3, 4])
    cbar.set_label('Traffic Level')
    
    # Traffic distribution histogram
    traffic_counts = [np.sum(traffic_raster == i) for i in range(1, 5)]
    ax2.bar(['No traffic', 'Medium', 'High', 'Heavy'], traffic_counts,
            color=['green', 'orange', 'red', 'darkred'])
    ax2.set_ylabel('Number of Pixels')
    ax2.set_title('Traffic Level Distribution', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('traffic_example.png', dpi=300, bbox_inches='tight')
    print("✓ Visualization saved to 'traffic_example.png'")
    
    # Save as GeoTIFF
    print("\nSaving as GeoTIFF...")
    output_path = gt.make_raster(
        location=location,
        height=1000,
        width=1000,
        zoom=14,
        google_key=GOOGLE_API_KEY,
        output_path='nyc_traffic.tif'
    )
    print(f"✓ GeoTIFF saved to: {output_path}")
    
    print("\n✅ Done! Check 'traffic_example.png' and 'nyc_traffic.tif'")
    
    # Show the plot
    plt.show()


if __name__ == "__main__":
    if GOOGLE_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
        print("⚠️  ERROR: Please set your Google Maps API key in this script!")
        print("   Get one at: https://developers.google.com/maps/get-started")
    else:
        main()
