from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_gradient_background(size):
    # Create a new image for the gradient
    image = Image.new('RGB', (size, size))
    pixels = image.load()
    
    # Define gradient colors (modern blue gradient)
    start_color = (0, 122, 255)  # iOS Blue
    end_color = (88, 86, 214)    # iOS Purple
    
    # Create smooth gradient
    for y in range(size):
        for x in range(size):
            # Calculate gradient position
            gradient_pos = (x + y) / (size * 2)
            
            # Interpolate between colors
            r = int(start_color[0] * (1 - gradient_pos) + end_color[0] * gradient_pos)
            g = int(start_color[1] * (1 - gradient_pos) + end_color[1] * gradient_pos)
            b = int(start_color[2] * (1 - gradient_pos) + end_color[2] * gradient_pos)
            
            pixels[x, y] = (r, g, b)
    
    return image

def create_icon(size, output_path):
    # Create base image with gradient
    image = create_gradient_background(size)
    draw = ImageDraw.Draw(image)
    
    # Calculate dot size (30% of icon size)
    dot_size = int(size * 0.3)
    
    # Calculate center position
    center = size // 2
    dot_radius = dot_size // 2
    
    # Draw white dot with subtle shadow
    # Shadow
    shadow_offset = max(2, size // 50)
    draw.ellipse((center - dot_radius + shadow_offset, 
                  center - dot_radius + shadow_offset,
                  center + dot_radius + shadow_offset, 
                  center + dot_radius + shadow_offset), 
                 fill=(0, 0, 0, 100))
    
    # Main white dot
    draw.ellipse((center - dot_radius, 
                  center - dot_radius,
                  center + dot_radius, 
                  center + dot_radius), 
                 fill=(255, 255, 255))
    
    # Add rounded corners to the entire icon
    corner_radius = size // 8
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size-1, size-1)], 
                              radius=corner_radius, fill=255)
    
    # Apply mask for rounded corners
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(image, mask=mask)
    
    # Save with transparency
    output.save(output_path, 'PNG')

def main():
    # Create site/icons directory if it doesn't exist
    icons_dir = Path('site/icons')
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate icons in different sizes
    icon_sizes = {
        '192x192': 192,
        '512x512': 512
    }
    
    for name, size in icon_sizes.items():
        output_path = icons_dir / f'icon-{name}.png'
        create_icon(size, output_path)
        print(f"Generated {name} icon at {output_path}")

if __name__ == "__main__":
    main()