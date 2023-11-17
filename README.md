# Moxfy: The Ultimate PDF Toolkit

A project that provides a collection of tools for working with PDF files. It offers various features, making it a versatile solution for managing PDF documents.

<image src="media/Main.PNG">

# Features:
- Compression: Shrink PDF file sizes while maintaining content quality, perfect for easy sharing and storage.
- Conversion: Convert PDFs to various formats, extracting content effortlessly.
- Decryption: Remove password protection and encryption from PDFs hassle-free.
- Encryption: Apply strong encryption using AES-256, AES-128, RC4-128, or RC4-40 to safeguard PDFs.
- Merging: This feature now offers the capability to combine multiple files
- Rotation: Adjust page orientations for optimal reading.
- Splitting: Divide large PDFs into manageable chunks.
- Watermarking: Add image watermarks for branding or protection.
- Calendar: Create PDF calendars with year views.
- Management: Efficiently delete, rearrange, and organize pages.

# Installation:
```bash
$ pip install -r requirements.txt or manual
```

# Configuration:
- Moxfy_adminPanel must put your own database details (.env file by default) in credentials.py (MongoDB)
- Moxfy_with_db must put your own database details (.env file by default) in db/config.py (MongoDB)
- Moxfy_with_db must put your own discord webhook api details (.env file by default) in pages/report/page.py
- Moxfy_without_db must put your own discord webhook api details (.env file by default) in pages/report/page.py

# Packaging:
- https://flet.dev/ 
- https://pub.dev/packages/serious_python 
and other tools ex. auto-py-to-exe, pyinstaller

# Tested on:
- Python version: 3.12.0
- Windows 10 Version 22H2 (OS Build 19045.3570)





