#!/usr/bin/env python3
"""
Script to check resolution of PNG and PDF figures in a folder.
Reports pixel dimensions and DPI for PNG files, and page size with inferred DPI for PDF files.
"""

import os
from pathlib import Path
from PIL import Image
import sys

# Try to import PyMuPDF (fitz), fall back to PyPDF2 if not available
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    try:
        import PyPDF2
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False
        print("Warning: Neither PyMuPDF nor PyPDF2 is available. PDF files will not be processed.")
        print("Please install PyMuPDF with: pip install PyMuPDF")
        print("Or install PyPDF2 with: pip install PyPDF2")

def check_png_resolution(filepath):
    """Check resolution of a PNG file."""
    try:
        with Image.open(filepath) as img:
            width_px, height_px = img.size
            
            # Get DPI from EXIF data if available
            dpi_x = dpi_y = None
            if hasattr(img, 'info') and 'dpi' in img.info:
                dpi_x, dpi_y = img.info['dpi']
            elif 'resolution' in img.info:
                dpi_x, dpi_y = img.info['resolution']
            
            return {
                'format': 'PNG',
                'width_px': width_px,
                'height_px': height_px,
                'dpi_x': dpi_x,
                'dpi_y': dpi_y
            }
    except Exception as e:
        return {
            'format': 'PNG',
            'width_px': None,
            'height_px': None,
            'dpi_x': None,
            'dpi_y': None,
            'error': str(e)
        }

def check_pdf_resolution(filepath):
    """Check resolution of a PDF file."""
    if not HAS_PYMUPDF and not HAS_PYPDF2:
        return {
            'format': 'PDF',
            'width_px': None,
            'height_px': None,
            'dpi_x': None,
            'dpi_y': None,
            'error': 'No PDF library available'
        }
    
    try:
        if HAS_PYMUPDF:
            # Use PyMuPDF (preferred method)
            doc = fitz.open(filepath)
            
            if len(doc) == 0:
                doc.close()
                return {
                    'format': 'PDF',
                    'width_px': None,
                    'height_px': None,
                    'dpi_x': None,
                    'dpi_y': None,
                    'error': 'Empty PDF'
                }
            
            # Get first page dimensions (assuming single-page figures)
            page = doc[0]
            rect = page.rect
            
            # Convert from points to inches (1 point = 1/72 inches)
            width_inches = rect.width / 72.0
            height_inches = rect.height / 72.0
            
            # Try to find raster images in the PDF to infer DPI
            dpi_x = dpi_y = None
            images = page.get_images()
            
            if images:
                # Get the first image
                xref = images[0][0]
                base_image = doc.extract_image(xref)
                
                if base_image:
                    # Get image dimensions in pixels
                    img_width_px = base_image['width']
                    img_height_px = base_image['height']
                    
                    # Get image bounding box on the page
                    image_rects = page.get_image_rects(xref)
                    if image_rects:
                        img_rect = image_rects[0]
                        img_width_inches = img_rect.width / 72.0
                        img_height_inches = img_rect.height / 72.0
                        
                        # Calculate inferred DPI
                        if img_width_inches > 0:
                            dpi_x = img_width_px / img_width_inches
                        if img_height_inches > 0:
                            dpi_y = img_height_px / img_height_inches
            
            # If no images found, calculate pixel dimensions assuming 300 DPI
            if dpi_x is None or dpi_y is None:
                assumed_dpi = 300
                width_px = int(width_inches * assumed_dpi)
                height_px = int(height_inches * assumed_dpi)
                dpi_x = dpi_y = assumed_dpi
            else:
                # Use the page dimensions scaled by the inferred DPI
                width_px = int(width_inches * dpi_x)
                height_px = int(height_inches * dpi_y)
            
            doc.close()
            
            return {
                'format': 'PDF',
                'width_px': width_px,
                'height_px': height_px,
                'dpi_x': dpi_x,
                'dpi_y': dpi_y,
                'width_inches': width_inches,
                'height_inches': height_inches
            }
        
        else:
            # Fallback to PyPDF2 (basic method)
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if len(pdf_reader.pages) == 0:
                    return {
                        'format': 'PDF',
                        'width_px': None,
                        'height_px': None,
                        'dpi_x': None,
                        'dpi_y': None,
                        'error': 'Empty PDF'
                    }
                
                # Get first page dimensions
                page = pdf_reader.pages[0]
                mediabox = page.mediabox
                
                # Convert from points to inches (1 point = 1/72 inches)
                width_inches = float(mediabox.width) / 72.0
                height_inches = float(mediabox.height) / 72.0
                
                # PyPDF2 doesn't provide DPI info, so assume 300 DPI for print quality
                assumed_dpi = 300
                width_px = int(width_inches * assumed_dpi)
                height_px = int(height_inches * assumed_dpi)
                
                return {
                    'format': 'PDF',
                    'width_px': width_px,
                    'height_px': height_px,
                    'dpi_x': assumed_dpi,
                    'dpi_y': assumed_dpi,
                    'width_inches': width_inches,
                    'height_inches': height_inches
                }
                
    except Exception as e:
        return {
            'format': 'PDF',
            'width_px': None,
            'height_px': None,
            'dpi_x': None,
            'dpi_y': None,
            'error': str(e)
        }

def scan_folder(folder_path):
    """Scan folder for PNG and PDF files and check their resolution."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return []
    
    results = []
    
    # Find all PNG and PDF files
    png_files = sorted(folder.glob('*.png'))
    pdf_files = sorted(folder.glob('*.pdf'))
    
    print(f"Found {len(png_files)} PNG files and {len(pdf_files)} PDF files.")
    print()
    
    # Process PNG files
    for png_file in png_files:
        print(f"Processing {png_file.name}...", end=' ', flush=True)
        result = check_png_resolution(png_file)
        result['filename'] = png_file.name
        results.append(result)
        print("Done")
    
    # Process PDF files
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...", end=' ', flush=True)
        result = check_pdf_resolution(pdf_file)
        result['filename'] = pdf_file.name
        results.append(result)
        print("Done")
    
    return results

def print_table(results):
    """Print results as a formatted table."""
    if not results:
        print("No files found.")
        return
    
    # Print header
    print("\n" + "=" * 100)
    print(f"{'Filename':<40} {'Format':<8} {'Width (px)':<12} {'Height (px)':<12} {'DPI X':<10} {'DPI Y':<10}")
    print("=" * 100)
    
    # Print rows
    for result in results:
        filename = result.get('filename', 'Unknown')
        format_type = result.get('format', 'Unknown')
        width_px = result.get('width_px', 'N/A')
        height_px = result.get('height_px', 'N/A')
        dpi_x = result.get('dpi_x', 'N/A')
        dpi_y = result.get('dpi_y', 'N/A')
        
        # Format values
        if width_px is not None:
            width_px = f"{width_px:,}"
        if height_px is not None:
            height_px = f"{height_px:,}"
        if dpi_x is not None:
            dpi_x = f"{dpi_x:.1f}"
        if dpi_y is not None:
            dpi_y = f"{dpi_y:.1f}"
        
        # Check for errors
        if 'error' in result:
            error_msg = f" [ERROR: {result['error']}]"
        else:
            error_msg = ""
        
        print(f"{filename:<40} {format_type:<8} {str(width_px):<12} {str(height_px):<12} {str(dpi_x):<10} {str(dpi_y):<10}{error_msg}")
    
    print("=" * 100)
    
    # Print summary statistics
    print("\nSummary:")
    png_count = sum(1 for r in results if r.get('format') == 'PNG')
    pdf_count = sum(1 for r in results if r.get('format') == 'PDF')
    error_count = sum(1 for r in results if 'error' in r)
    
    print(f"  Total files: {len(results)}")
    print(f"  PNG files: {png_count}")
    print(f"  PDF files: {pdf_count}")
    if error_count > 0:
        print(f"  Files with errors: {error_count}")

def main():
    """Main function."""
    # Default folder path
    folder_path = r"C:\Users\oprio\Documents\thesis_docx_to_latex\source\figures"
    
    # Allow command-line argument for folder path
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    
    print(f"Scanning folder: {folder_path}")
    print()
    
    results = scan_folder(folder_path)
    print_table(results)

if __name__ == "__main__":
    main()
