import tkinter as tk
from tkinter import filedialog
import ezdxf
import simplekml
from pyproj import Transformer

# Function to convert DXF to KML with coordinate transformation
def convert_dxf_to_kml(input_path, output_path, transformer):
    # Read the DXF file
    doc = ezdxf.readfile(input_path)
    msp = doc.modelspace()

    # Create a KML object
    kml = simplekml.Kml()

    # Loop through each entity in the DXF file
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            # Transform coordinates
            start_lon, start_lat = transformer.transform(start.x, start.y)
            end_lon, end_lat = transformer.transform(end.x, end.y)
            kml.newlinestring(coords=[(start_lon, start_lat), (end_lon, end_lat)])

    # Save the KML file
    kml.save(output_path)

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open a file dialog to select the DXF file
input_file_path = filedialog.askopenfilename(
    title="Select DXF file",
    filetypes=[("DXF files", "*.dxf")]
)

# Open a file dialog to select the output KML file path
output_file_path = filedialog.asksaveasfilename(
    title="Save KML file",
    defaultextension=".kml",
    filetypes=[("KML files", "*.kml")]
)

# Define the coordinate transformation
# You need to replace 'epsg:32633' with the correct EPSG code for your DXF file's coordinate system
transformer = Transformer.from_crs("epsg:32608", "epsg:4326", always_xy=True)

# Convert the DXF file to KML
if input_file_path and output_file_path:
    convert_dxf_to_kml(input_file_path, output_file_path, transformer)
    print(f"Conversion completed: {output_file_path}")
else:
    print("File selection cancelled.")
