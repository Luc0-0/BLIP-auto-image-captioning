import gradio as gr
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import io
import numpy as np

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def is_image_url(url):
    """Check if URL points to an image"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif']
    return any(url.lower().endswith(ext) for ext in image_extensions)

def extract_images_from_website(website_url):
    """Extract all image URLs from a website"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(website_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img_tags = soup.find_all('img')
        image_urls = []
        
        for img in img_tags:
            # Try both src and data-src (for lazy loading)
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if src:
                # Skip SVGs and very small images
                if not src.endswith('.svg') and 'data:image' not in src:
                    full_url = urljoin(website_url, src)
                    image_urls.append(full_url)
        
        print(f"Found {len(image_urls)} images on {website_url}")  # Debug
        return image_urls[:10]  # Limit to first 10 images
    except Exception as e:
        print(f"Error extracting images: {e}")  # Debug
        return []

def caption_single_image(image_url):
    """Caption a single image"""
    try:
        print(f"Downloading image from: {image_url}")  # Debug step 1
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(image_url, stream=True, timeout=10, headers=headers)
        
        print(f"Response status: {response.status_code}")  # Debug step 2
        
        image = Image.open(response.raw)
        print(f"Image loaded: {image.size}, mode: {image.mode}")  # Debug step 3
        
        # Convert to RGB if needed (fixes some image format issues)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            print("Converted to RGB")  # Debug step 4
        
        # Generate caption
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs, max_length=50)
        caption = processor.decode(out[0], skip_special_tokens=True)
        
        print(f"Caption generated: {caption}")  # Debug step 5
        
        # Convert PIL image to numpy array for Gradio
        import numpy as np
        image_array = np.array(image)
        
        return caption, image_array
    except Exception as e:
        print(f"Error in caption_single_image: {e}")  # Debug step 6
        return f"Error: {str(e)}", None

# Global variables to store processed images
processed_images = []
current_image_index = 0

def process_url_input(url_input):
    """Process either direct image URL or website URL"""
    global processed_images, current_image_index
    processed_images = []  # Reset
    current_image_index = 0
    
    try:
        if is_image_url(url_input):
            # Direct image URL
            caption, image = caption_single_image(url_input)
            if image is not None:
                processed_images = [{'image': image, 'caption': caption, 'url': url_input}]
                return caption, image, "Image 1/1", gr.update(visible=False), gr.update(visible=False)
            else:
                return caption, None, "", gr.update(visible=False), gr.update(visible=False)
        else:
            # Website URL - extract images
            image_urls = extract_images_from_website(url_input)
            
            if not image_urls:
                return "No valid images found on this website. Try a news site or blog.", None, "", gr.update(visible=False), gr.update(visible=False)
            
            # Process all images
            for i, img_url in enumerate(image_urls):
                print(f"Processing image {i+1}: {img_url}")  # Debug
                caption, image = caption_single_image(img_url)
                
                if image is not None and not caption.startswith("Error"):
                    processed_images.append({
                        'image': image, 
                        'caption': caption, 
                        'url': img_url
                    })
            
            if not processed_images:
                return f"Found {len(image_urls)} images but couldn't process any.", None, "", gr.update(visible=False), gr.update(visible=False)
            
            # Show first image
            first_img = processed_images[0]
            nav_visible = len(processed_images) > 1
            
            return first_img['caption'], first_img['image'], f"Image 1/{len(processed_images)}", gr.update(visible=nav_visible), gr.update(visible=nav_visible)
            
    except Exception as e:
        return f"Error: {str(e)}", None, "", gr.update(visible=False), gr.update(visible=False)

def show_previous_image():
    """Show previous image"""
    global current_image_index
    if processed_images and current_image_index > 0:
        current_image_index -= 1
        img_data = processed_images[current_image_index]
        return img_data['caption'], img_data['image'], f"Image {current_image_index + 1}/{len(processed_images)}"
    return gr.update(), gr.update(), gr.update()

def show_next_image():
    """Show next image"""
    global current_image_index
    if processed_images and current_image_index < len(processed_images) - 1:
        current_image_index += 1
        img_data = processed_images[current_image_index]
        return img_data['caption'], img_data['image'], f"Image {current_image_index + 1}/{len(processed_images)}"
    return gr.update(), gr.update(), gr.update()

# Create Gradio interface
with gr.Blocks(title="Image Captioning") as demo:
    gr.Markdown("# Auto Image Captioning with BLIP")
    gr.Markdown("Enter either a **direct image URL** or a **website URL** to caption all images")
    
    with gr.Row():
        url_input = gr.Textbox(
            label="URL Input", 
            placeholder="Enter image URL or website URL here...",
            lines=1
        )
        
    with gr.Row():
        caption_btn = gr.Button("Generate Captions", variant="primary")
        
    with gr.Row():
        with gr.Column():
            image_output = gr.Image(label="Current Image")
            
            # Navigation controls
            with gr.Row():
                prev_btn = gr.Button("◀ Previous", visible=False)
                info_output = gr.Textbox(label="", lines=1, interactive=False)
                next_btn = gr.Button("Next ▶", visible=False)
                
        with gr.Column():
            caption_output = gr.Textbox(label="Current Caption", lines=5)
    
    # Event handlers
    caption_btn.click(
        fn=process_url_input,
        inputs=url_input,
        outputs=[caption_output, image_output, info_output, prev_btn, next_btn]
    )
    
    prev_btn.click(
        fn=show_previous_image,
        outputs=[caption_output, image_output, info_output]
    )
    
    next_btn.click(
        fn=show_next_image,
        outputs=[caption_output, image_output, info_output]
    )

if __name__ == "__main__":
    demo.launch()