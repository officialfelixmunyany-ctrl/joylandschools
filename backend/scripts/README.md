Place a site logo at `backend/static/images/logo.jpg` so the navbar shows the logo. You can create a small placeholder image using any image editor or use the following one-liner in PowerShell to create a 1x1 white JPEG (requires ImageMagick 'magick' command):

# Create a 1x1 white JPEG placeholder (ImageMagick)
magick -size 1x1 canvas:white backend\static\images\logo.jpg

Alternatively, copy an existing logo file to `backend/static/images/logo.jpg`.
