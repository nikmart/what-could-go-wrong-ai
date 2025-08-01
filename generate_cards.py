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
    process_csv('prompts-ai.csv', 'PROMPTS', PROMPT_BG_COLOR, PROMPT_TEXT_COLOR)
    process_csv('responses-ai.csv', 'RESPONSES', RESPONSE_BG_COLOR, RESPONSE_TEXT_COLOR)
    
    # Create card back
    os.makedirs('PROMPTS', exist_ok=True)
    create_card_back('PROMPTS/card_back.png')

if __name__ == '__main__':
    # This guard is important for multiprocessing on Windows
    main() 