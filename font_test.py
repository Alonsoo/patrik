
import pyfiglet

# Define the text you want to preview
preview_text = "Ab#"

# Get a list of all available fonts
all_fonts = pyfiglet.FigletFont.getFonts()

print(f"--- Found {len(all_fonts)} fonts. Starting preview... ---\n")

# Loop through each font and print the rendered text
for font_name in all_fonts:
    try:
        # Generate the ASCII art for the current font
        ascii_art = pyfiglet.figlet_format(preview_text, font=font_name)
        
        # Display the font name and its preview
        print(f"FONT NAME: {font_name}")
        print("-" * 40)
        print(ascii_art)
        print("=" * 40 + "\n")
        
    except Exception as e:
        # Skip fonts that throw rendering errors
        print(f"Skipping font '{font_name}' due to error.\n")

print("--- Preview Complete ---")
