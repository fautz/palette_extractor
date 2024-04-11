from datetime import datetime
import colorgram
from colorthief import ColorThief
from extcolors import extract_from_path
from flask import Flask, render_template, request
from PIL import Image
from Pylette import extract_colors

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    num_colors = 10
    extcolors_tolerance = 32
    
    if request.method == 'POST':        
        image = request.files['file']
        num_colors = int(request.form['num_colors'])
        extcolors_tolerance = int(request.form['extcolors_tolerance'])

        # save image with unique name based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image.save('static/' + timestamp + image.filename)

        # get image path
        image_path = 'static/' + timestamp + image.filename

        palette_mc = extract_colors(image, palette_size=num_colors, mode='MC')
        pylette_palette_mc = []
        for color in palette_mc:
            pylette_palette_mc.append('#%02x%02x%02x' % color.rgb)

        palette_km = extract_colors(image, palette_size=num_colors, mode='KM')
        pylette_palette_km = []
        for color in palette_km:
            pylette_palette_km.append('#%02x%02x%02x' % color.rgb)

        palette = ColorThief(image_path).get_palette(color_count=num_colors, quality=1)
        colorthief_palette = []
        for color in palette:
            colorthief_palette.append('#%02x%02x%02x' % color)

        palette = colorgram.extract(image_path, num_colors)
        colorgram_palette = []
        for color in palette:
            colorgram_palette.append('#%02x%02x%02x' % color.rgb)

        img = Image.open(image_path)
        colors, pixel_count = extract_from_path(image_path, tolerance=extcolors_tolerance, limit=num_colors)
        extcolors_palette = []
        for color, count in colors:
            extcolors_palette.append('#%02x%02x%02x' % color)

        return render_template(
            'index.html',
            image_path=image_path,
            pylette_palette_mc=pylette_palette_mc,
            pylette_palette_km=pylette_palette_km,
            colorthief_palette=colorthief_palette,
            colorgram_palette=colorgram_palette,
            extcolors_palette=extcolors_palette,
            num_colors=num_colors,
            extcolors_tolerance=extcolors_tolerance,
        )
        
    return render_template(
        'index.html',
        num_colors=num_colors,
        extcolors_tolerance=extcolors_tolerance,
    )
















