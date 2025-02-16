# Project Summary: Google Drive File Download Development
Date: January 2025

## Project Overview
Developed a Python script to:
- Download files from Google Drive URLs listed in a Google Sheet
- Process PDFs into images
- Handle various document types
- Rename files based on invoice numbers

## Development Journey

### Initial Requirements
- Pull files from Google Sheet
- Process both PDFs and Word documents
- Save with consistent naming convention
- Handle both standard PDFs and image-based PDFs

### Key Challenges & Solutions

1. PDF Processing
   - First Attempt: PDF2Image with poppler
     - Required external dependencies
     - Installation issues on Windows
   - Final Solution: PyMuPDF (fitz)
     - Single pip install
     - Better performance
     - No external dependencies

2. URL Parsing
   - Initial Issue: Code assumed single URL format
   - Challenge: Google Drive uses multiple URL formats
   - Solution: Enhanced URL parsing to handle both formats:
     - drive.google.com/file/d/[ID]
     - drive.google.com/open?id=[ID]

3. File Naming
   - Initial: Complex (row numbers + metadata)
   - Final: Simple (just invoice numbers)
   - Preserved original file extensions

4. Error Handling
   - Implemented continue-on-error
   - Added detailed logging
   - Included fallback mechanisms for file processing

## Technical Implementation Details

### Dependencies
- google.oauth2.credentials
- google_auth_oauthlib.flow
- googleapiclient
- PyMuPDF (fitz)
- Pillow (PIL)

### Key Functions
1. `authenticate()`: Handle Google OAuth
2. `extract_file_id()`: Parse Drive URLs
3. `get_safe_filename()`: Generate consistent filenames
4. `save_file()`: Process and save different file types
5. `download_files_from_sheet()`: Main orchestration

### File Processing Workflow
1. Read Google Sheet
2. Extract valid URLs
3. Download files
4. Process based on type:
   - PDFs → Convert to PNG
   - Word docs → Save as-is
   - Images → Optimize and save
5. Apply consistent naming

## Testing Results

### Working Cases
- Standard PDFs
- Word documents (.doc, .docx)
- Multiple page PDFs
- Various Google Drive URL formats

### Edge Cases Handled
- Empty rows in spreadsheet
- Invalid URLs
- Corrupted PDFs
- Missing column data

## Future Development Opportunities

1. Technical Enhancements
   - PDF type discrimination
   - Parallel downloading
   - Progress tracking
   - Enhanced error recovery

2. Feature Additions
   - Additional file type support
   - Batch processing options
   - Custom naming templates
   - Automated testing

## Lessons Learned

1. Technical
   - Prefer pure Python packages over external dependencies
   - Plan for multiple input formats
   - Implement progressive enhancement
   - Build in robust error handling

2. Process
   - Start simple, add complexity as needed
   - Test with real data early
   - Document decisions and rationale
   - Keep error messages informative

## Current Status
- Working implementation
- Successfully processing files
- Stable and reliable
- Ready for production use

## Repository Structure
```
project/
├── mainv4.py           # Main script
├── token.json          # OAuth tokens (generated)
├── gdrive_oauth.json   # Google API credentials
└── images/             # Output directory (stores downloaded images)
```

## Usage
```python
download_files_from_sheet(
    CREDENTIALS_PATH,
    SPREADSHEET_ID,
    SHEET_NAME,
    URL_COLUMN_INDEX,
    DOWNLOAD_DIR,
    dpi=300,
    quality=95
)
```

### Usage notes from GitHub
* token.json and gdrive_oath.json are not available in public drive
   * Contact author to request permission to access these files. 
* When running the download_images.py from the ipynb:
   * the google authentication credentials also require the user to sign in to a google user account associated with the google drive that requires further credentials including a username and password.  Neither of these are included in the github repo for privacy concerns. 
* Data Version Control is instantiated using DVC:
   * the data folder is not included in the git hub repo
   * the dvc repo is established in a github lfs
   * to access the image data the user would have to clone the repo, dvc init, and run dvc pull
   * to satisfy completion requirements for the UCSD course submission a url to the data will be provided separately


## Maintenance Notes
- Check Google API quotas periodically
- Monitor token refresh
- Review error logs
- Update dependencies as needed

## Contact
For questions or modifications, contact Alden Smith (alden.w.smith.iii@gmail.com).