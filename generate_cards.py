"""
Created by Nik and the Cursor AI Assistant
A script to generate high-resolution playing cards from CSV data
"""

import os
import csv
from PIL import Image, ImageDraw, ImageFont
import multiprocessing
from functools import partial

# Card Dimensions (in pixels at 1200 DPI)
DPI = 1200
MM_TO_PIXELS = DPI / 25.4  # Convert mm to pixels at 1200 DPI

# Card dimensions - Updated to 825x1125 pixels
CARD_WIDTH = 825
CARD_HEIGHT = 1125

# Text box dimensions (fixed pixel margins for better control)
MARGIN = 100  # Fixed 100 pixel margin
TEXT_BOX_WIDTH = CARD_WIDTH - (2 * MARGIN)
TEXT_BOX_HEIGHT = CARD_HEIGHT - (2 * MARGIN)
TEXT_BOX_TOP = 120  # Fixed top position for better text placement

# Font Settings (adjusted for new card size)
FONT_SIZE_MAIN = 72  # Increased size for better visibility
FONT_SIZE_NUMBER = 48  # Increased size for card numbers
MAIN_FONT = "Bitter-Bold.ttf"

# Colors
PROMPT_BG_COLOR = (0, 0, 0)
PROMPT_TEXT_COLOR = (255, 255, 255)
RESPONSE_BG_COLOR = (255, 255, 255)
RESPONSE_TEXT_COLOR = (0, 0, 0)

def create_card(text, card_number, output_path, bg_color, text_color):
    # Create image
    image = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        main_font = ImageFont.truetype(MAIN_FONT, FONT_SIZE_MAIN)
        number_font = ImageFont.truetype(MAIN_FONT, FONT_SIZE_NUMBER)
    except OSError:
        print("Arial Bold.ttf not found. Using default font.")
        main_font = ImageFont.load_default()
        number_font = ImageFont.load_default()

    # Calculate text wrapping
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=main_font)
        if bbox[2] - bbox[0] <= TEXT_BOX_WIDTH:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw main text with better spacing
    y = TEXT_BOX_TOP
    line_height = int(FONT_SIZE_MAIN * 1.4)  # Increased line height for better readability
    
    for line in lines:
        draw.text((MARGIN, y), line, font=main_font, fill=text_color)
        y += line_height
    
    # Draw card number in bottom right corner
    number_bbox = draw.textbbox((0, 0), card_number, font=number_font)
    number_width = number_bbox[2] - number_bbox[0]
    number_x = CARD_WIDTH - number_width - MARGIN
    number_y = CARD_HEIGHT - MARGIN - FONT_SIZE_NUMBER
    draw.text((number_x, number_y), card_number, font=number_font, fill=text_color)
    
    # Save image
    image.save(output_path, 'PNG', dpi=(DPI, DPI))

def create_card_back(output_path):
    """Create a card back with 'What Could Go Wrong?' text."""
    # Create image with black background
    image = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), PROMPT_BG_COLOR)
    draw = ImageDraw.Draw(image)
    
    # Use larger font size for card back
    larger_font_size = 96  # Increased size for card back
    
    try:
        main_font = ImageFont.truetype(MAIN_FONT, larger_font_size)
    except OSError:
        print("Arial Bold.ttf not found. Using default font.")
        main_font = ImageFont.load_default()

    # Force the text to split exactly as specified
    lines = ["What Could", "Go Wrong?"]
    
    # Draw main text with better spacing
    y = TEXT_BOX_TOP
    line_height = int(larger_font_size * 1.4)  # Increased line height for better readability
    
    for line in lines:
        draw.text((MARGIN, y), line, font=main_font, fill=PROMPT_TEXT_COLOR)
        y += line_height
    
    # Save image
    image.save(output_path, 'PNG', dpi=(DPI, DPI))

def create_instruction_card(qr_image_path, url, output_path):
    """Create a special instruction card with QR code and URL."""
    # Create image with white background
    image = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), RESPONSE_BG_COLOR)
    draw = ImageDraw.Draw(image)
    
    try:
        # Load fonts
        title_font = ImageFont.truetype(MAIN_FONT, 84)  # Larger font for title
        url_font = ImageFont.truetype(MAIN_FONT, 48)    # Smaller font for URL
    except OSError:
        print(f"{MAIN_FONT} not found. Using default font.")
        title_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
    
    # Load and resize QR code
    try:
        qr_image = Image.open(qr_image_path)
        # Calculate QR code size (about 1/3 of card width)
        qr_size = int(CARD_WIDTH * 0.4)
        qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Calculate QR code position (center horizontally and vertically)
        qr_x = (CARD_WIDTH - qr_size) // 2
        qr_y = (CARD_HEIGHT - qr_size) // 2  # True center of the card
        
        # Paste QR code onto the card
        image.paste(qr_image, (qr_x, qr_y))
        
    except Exception as e:
        print(f"Error loading QR code: {e}")
        # If QR code fails, we'll still create the card with text
    
    # Use the QR code position for other elements
    qr_y = (CARD_HEIGHT - qr_size) // 2
    
    # Position title above QR code
    title_words = ["Gameplay", "Instructions"]
    title_bottom_y = qr_y - 150  # 100 pixels above QR code
    
    for i, word in enumerate(title_words):
        word_bbox = draw.textbbox((0, 0), word, font=title_font)
        word_width = word_bbox[2] - word_bbox[0]
        word_x = (CARD_WIDTH - word_width) // 2
        word_y = title_bottom_y - (len(title_words) - 1 - i) * int(84 * 1.2)  # Position from bottom up
        draw.text((word_x, word_y), word, font=title_font, fill=RESPONSE_TEXT_COLOR)
    
    # Position URL below QR code
    url_y = qr_y + qr_size + 80  # 80 pixels below QR code
    url_bbox = draw.textbbox((0, 0), url, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    
    # If URL is too long, wrap it
    if url_width > TEXT_BOX_WIDTH:
        # Simple character-based wrapping to preserve exact URL
        lines = []
        current_line = ""
        
        for char in url:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=url_font)
            if bbox[2] - bbox[0] <= TEXT_BOX_WIDTH:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        # Draw wrapped URL lines
        line_height = int(48 * 1.2)
        for i, line in enumerate(lines):
            line_bbox = draw.textbbox((0, 0), line, font=url_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (CARD_WIDTH - line_width) // 2
            line_y = url_y + (i * line_height)
            draw.text((line_x, line_y), line, font=url_font, fill=RESPONSE_TEXT_COLOR)
    else:
        # URL fits on one line
        url_x = (CARD_WIDTH - url_width) // 2
        draw.text((url_x, url_y), url, font=url_font, fill=RESPONSE_TEXT_COLOR)
    
    # Save image
    image.save(output_path, 'PNG', dpi=(DPI, DPI))

def process_row(row, output_dir, bg_color, text_color):
    """Process a single row from the CSV file."""
    if len(row) >= 2:
        text, card_number = row[0], row[1]
        output_path = os.path.join(output_dir, f'{card_number}.png')
        create_card(text, card_number, output_path, bg_color, text_color)

def process_csv(filename, output_dir, bg_color, text_color):
    os.makedirs(output_dir, exist_ok=True)
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)

    # Create a partial function with fixed arguments
    process_func = partial(process_row, 
                         output_dir=output_dir, 
                         bg_color=bg_color, 
                         text_color=text_color)

    # Use all available CPU cores
    with multiprocessing.Pool() as pool:
        pool.map(process_func, rows)

def main():
    # Create main directory structure
    os.makedirs('CARD IMAGES', exist_ok=True)
    os.makedirs('CARD IMAGES/PROMPT', exist_ok=True)
    os.makedirs('CARD IMAGES/RESPONSE', exist_ok=True)
    
    process_csv('prompts-ai.csv', 'CARD IMAGES/PROMPT', PROMPT_BG_COLOR, PROMPT_TEXT_COLOR)
    process_csv('responses-ai.csv', 'CARD IMAGES/RESPONSE', RESPONSE_BG_COLOR, RESPONSE_TEXT_COLOR)
    
    # Create card back
    create_card_back('CARD IMAGES/card_back.png')
    
    # Create instruction card with QR code
    create_instruction_card('wcgw-instructions-qr.png', 'https://nikmartelaro.com/what-could-go-wrong-ai/', 'CARD IMAGES/instructions.png')

if __name__ == '__main__':
    # This guard is important for multiprocessing on Windows
    main() 