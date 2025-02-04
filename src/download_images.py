from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import fitz  # PyMuPDF
import io
import os
from pathlib import Path
from PIL import Image
import mimetypes

# OAuth Scopes - adjust as needed
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate(credentials_path):
    """
    Authenticate and create credentials
    """
    try:
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path,
            SCOPES
        )
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials

def extract_file_id(file_url):
    """Extract file ID from different Google Drive URL formats"""
    try:
        if '/file/d/' in file_url:
            # Handle format: https://drive.google.com/file/d/FILE_ID/view...
            file_id = file_url.split('/file/d/')[1].split('/')[0]
        elif 'open?id=' in file_url:
            # Handle format: https://drive.google.com/open?id=FILE_ID
            file_id = file_url.split('open?id=')[1].split('&')[0]
        else:
            return None
        return file_id
    except Exception as e:
        print(f"URL parsing error: {e}")
        return None

def get_safe_filename(row, original_filename):
    """Create filename from column B value and preserve extension"""
    # Get extension from original filename
    file_ext = os.path.splitext(original_filename)[1]
    
    # Get value from column B (index 1) or use 'no_invoice_num' if not available
    invoice_num = row[1] if len(row) > 1 and row[1] else 'no_invoice_num'
    
    # Clean the invoice number (remove special characters)
    invoice_num = ''.join(c for c in str(invoice_num) if c.isalnum() or c in '-_')
    
    # Create new filename: invoice_number.extension
    new_filename = f"{invoice_num}{file_ext}"
    
    # Replace any remaining invalid characters
    new_filename = new_filename.replace(' ', '_')
    
    return new_filename

def save_file(file_content, filename, download_dir, dpi=300, quality=95):
    """Handle different file types appropriately"""
    file_path = download_dir / filename
    file_lower = filename.lower()
    mime_type, _ = mimetypes.guess_type(filename)
    
    # Handle PDFs
    if file_lower.endswith('.pdf'):
        try:
            # Try to open as PDF
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            
            if pdf_document.page_count > 0:
                # Valid PDF - convert pages to images with quality settings
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    zoom = dpi / 72  # standard PDF DPI is 72
                    matrix = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=matrix)
                    
                    img_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    image_path = file_path.with_name(f"{file_path.stem}_page_{page_num + 1}.png")
                    
                    # Save with quality settings
                    if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                        img_data.save(str(image_path), "JPEG", quality=quality)
                    else:
                        img_data.save(str(image_path), "PNG", optimize=True)
                        
                print(f"Converted PDF to {pdf_document.page_count} images at {dpi} DPI")
                
            else:
                raise ValueError("Empty PDF document")
                
            pdf_document.close()
            
        except Exception as e:
            print(f"PDF processing failed ({str(e)}), trying as image...")
            try:
                # Try to handle as image
                img = Image.open(io.BytesIO(file_content))
                save_path = file_path.with_suffix('.png')
                img.save(str(save_path), 'PNG', optimize=True)
                print(f"Successfully saved as image: {save_path}")
            except Exception as img_e:
                print(f"Image conversion failed ({str(img_e)}), saving original file")
                with file_path.open('wb') as f:
                    f.write(file_content)
    
    # Handle images
    elif mime_type and mime_type.startswith('image/'):
        try:
            img = Image.open(io.BytesIO(file_content))
            if file_lower.endswith(('.jpg', '.jpeg')):
                img.save(str(file_path), quality=quality)
            else:
                img.save(str(file_path), optimize=True)
            print(f"Saved image: {file_path}")
        except Exception as e:
            print(f"Image processing failed ({str(e)}), saving original")
            with file_path.open('wb') as f:
                f.write(file_content)
    
    # Handle other files
    else:
        with file_path.open('wb') as f:
            f.write(file_content)
        print(f"Saved original file: {file_path}")

def download_files_from_sheet(
    credentials_path, 
    spreadsheet_id, 
    sheet_name, 
    url_column_index, 
    download_dir_str='downloaded_files',
    dpi=300,
    quality=95
):
    """Download files from Google Drive based on URLs in a Google Sheet"""
    # Convert download directory string to Path object
    download_dir = Path(download_dir_str)
    download_dir.mkdir(parents=True, exist_ok=True)
    
    # Authenticate and build services
    credentials = authenticate(credentials_path)
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Get sheet data
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, 
        range=sheet_name
    ).execute()
    values = result.get('values', [])
    
    # Debug info
    print(f"Total rows retrieved: {len(values)}")
    url_count = sum(1 for row in values[1:] if len(row) > url_column_index and row[url_column_index])
    print(f"Found {url_count} URLs to process\n")
    
    # Process each row
    for index, row in enumerate(values[1:], start=2):
        try:
            if len(row) <= url_column_index or not row[url_column_index]:
                print(f"Row {index}: No URL found")
                continue
                
            file_url = row[url_column_index]
            file_id = extract_file_id(file_url)
            
            if not file_id:
                print(f"Row {index}: Invalid URL format: {file_url}")
                continue
            
            # Get file metadata
            file_metadata = drive_service.files().get(
                fileId=file_id,
                fields='name,mimeType,size'
            ).execute()
            
            original_filename = file_metadata['name']
            filename = get_safe_filename(row, original_filename)
            print(f"Row {index}: Processing {filename}")
            
            # Download file
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Row {index}: Download {int(status.progress() * 100)}% complete")
            
            # Save and process file
            save_file(fh.getvalue(), filename, download_dir, dpi, quality)
            print(f"Row {index}: Successfully processed {filename}\n")
            
        except Exception as e:
            print(f"Row {index}: Error - {str(e)}\n")

if __name__ == '__main__':
    # Replace with your actual paths and IDs
    CREDENTIALS_PATH = r'D:\UCSD_MJM_1_Data_Download\gdrive_oauth.json'
    SPREADSHEET_ID = r'1gdjS8gaGFaQs6J09yv7SeiYKy6ZdOLnXoZfIrQQpGoY'
    SHEET_NAME = r'Estimates/Invoices'
    URL_COLUMN_INDEX = 7  # For column H
    DOWNLOAD_DIR = r'D:\UCSD_MJM_1_Data_Download\images'
    
    download_files_from_sheet(
        CREDENTIALS_PATH, 
        SPREADSHEET_ID, 
        SHEET_NAME, 
        URL_COLUMN_INDEX,
        DOWNLOAD_DIR,
        dpi=300,  # Adjust DPI for PDF conversion
        quality=95  # Adjust JPEG quality
    )