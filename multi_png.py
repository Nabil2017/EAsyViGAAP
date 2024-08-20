import os

png_dir = './FASTQC_Results'

output_html = './FASTQC_Results/aggregated_png_report.html'

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bioinformatics Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ text-align: center; }}
        img {{ display: block; margin-left: auto; margin-right: auto; width: 80%; }}
        .image-container {{ margin-bottom: 50px; }}
    </style>
</head>
<body>
    <h1>Bioinformatics Analysis Report</h1>
    {images}
</body>
</html>
"""

image_tags = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.png'):
        image_path = os.path.join(png_dir, file_name)
        image_tags.append(f'<div class="image-container"><h2>{file_name}</h2><img src="{image_path}" alt="{file_name}"></div>')

images_html = '\n'.join(image_tags)

final_html = html_template.format(images=images_html)

with open(output_html, 'w') as f:
    f.write(final_html)

print(f"HTML report generated: {output_html}")

