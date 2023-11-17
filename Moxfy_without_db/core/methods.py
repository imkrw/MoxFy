from pypdf import PdfReader
from pypdf import PdfWriter
from PyPDF2 import PdfReader as PR
from PyPDF2 import PdfWriter as PW
from pdf2docx import Converter
from helper import handler
import os
import fitz
import calendar
import random
import string


"""Creat Output Path Function"""


def Output(input_file, outputdir, action, suffix=None):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    dec_name = handler.get_file_name(input_file)
    actions_map = {
        "rotate": f"{dec_name}_rotated_{suffix}.pdf",
        "encrypt": f"{dec_name}_encrypted_{suffix}.pdf",
        "decrypt": f"{dec_name}_decrypted.pdf",
        "compress": f"{dec_name}_compressed.pdf",
        "calendar": f"{dec_name}_{suffix}.pdf",
        "watermark": f"{dec_name}_{suffix}.pdf",
        "split": f"{dec_name}_{suffix}.pdf",
        "pdf2docx": f"{dec_name}_{suffix}.docx",
        "pdf2png": f"{dec_name}_{suffix}.png",
        "pdf2jpg": f"{dec_name}_{suffix}.jpg",
        "delete_page": f"{dec_name}_{suffix}.pdf",
        "delete_pages": f"{dec_name}_{suffix}.pdf",
        "re_arrange": f"{dec_name}_re_arranged_{suffix}.pdf",
    }
    output_path = os.path.join(outputdir, actions_map[action])
    return output_path


"""A Function To Check If The PDF is Encrypted"""


def isEncrypted(file):
    pdf = fitz.Document(file)
    return pdf.isEncrypted


"""Creat Calendar Function"""


def doCreateCalendar(input_year, num_years, outputdir):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    if not str(input_year).isdigit() or len(str(input_year)) != 4:
        raise ValueError("input year must be a 4-digit integer.")

    if num_years <= 0:
        raise ValueError("number of years must be greater than zero.")

    doc = fitz.open()
    font = fitz.Font("spacemo")
    cal = calendar.TextCalendar()

    page_rect = fitz.paper_rect("a4-l")
    w = page_rect.width
    h = page_rect.height
    print_rect = page_rect + (36, 72, -36, -36)

    char_width = font.glyph_advance(32)
    fontsize = print_rect.width / (char_width * 100)

    def page_out(doc, text):
        page = doc.new_page(width=w, height=h)
        tw = fitz.TextWriter(page_rect)
        tw.fill_textbox(print_rect, text, font=font, fontsize=fontsize)
        tw.write_text(page)

    start_year = int(input_year)
    for i in range(num_years):
        text = cal.formatyear(start_year + i, m=4)
        page_out(doc, text)

    doc.subset_fonts()
    output_path = Output(
        input_year, outputdir, action="calendar", suffix=f"{input_year}-{input_year + num_years - 1}"
    )
    doc.save(output_path, garbage=4, deflate=True, pretty=True)
    doc.close()


"""Watermark By Image Function"""


def doWatermarkImage(input_file, input_file_overlay, size, align, outpurdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to watermark and make sure it is a PDF file."
        )
    if not input_file_overlay:
        raise FileNotFoundError("please provide a image file to watermark")
    src = fitz.open(input_file_overlay)
    if not src.is_pdf:
        pdfbytes = src.convert_to_pdf()
        src.close()
        src = fitz.open("pdf", pdfbytes)
    rect = src[0].rect
    factor = size / rect.height
    rect *= factor
    doc = fitz.open(input_file)
    xref = 0
    for page in doc:
        if align == "bottom left":
            rect_align = fitz.Rect(
                10, page.rect.height - rect.height, rect.width, page.rect.height
            )
        if align == "bottom center":
            rect_align = fitz.Rect(
                (page.rect.width - rect.width) / 2,
                page.rect.height - rect.height,
                (page.rect.width + rect.width) / 2,
                page.rect.height - 10,
            )
        if align == "bottom right":
            rect_align = fitz.Rect(
                page.rect.width - rect.width,
                page.rect.height - rect.height,
                page.rect.width - 10,
                page.rect.height,
            )
        if align == "top left":
            rect_align = fitz.Rect(10, 10, rect.width, rect.height + 10)
        if align == "top center":
            rect_align = fitz.Rect(
                (page.rect.width - rect.width) / 2,
                10,
                (page.rect.width + rect.width) / 2,
                rect.height,
            )
        if align == "top right":
            rect_align = fitz.Rect(
                page.rect.width - rect.width, 10, page.rect.width, rect.height
            )
        xref = page.show_pdf_page(rect_align, src, 0, reuse_xref=xref, overlay=False)
    output_path = Output(
        input_file, outpurdir, action="watermark", suffix="Watermarked"
    )
    doc.save(output_path, garbage=4)


"""Split All Pages Function"""


def doSplit(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to split and make sure it is a PDF file."
        )
    src = fitz.open(input_file)
    for i in range(len(src)):
        doc = fitz.open()
        doc.insert_pdf(src, from_page=i, to_page=i)
        output_path = Output(input_file, outputdir, action="split", suffix=f"page_{i+1}")
        doc.save(output_path)
        doc.close()


"""Custom Split Page Function"""


def doSplitCustomPage(input_file, page_number, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to split and make sure it is a PDF file."
        )
    src = fitz.open(input_file)
    if page_number >= 1 and page_number <= len(src):
        doc = fitz.open()
        doc.insert_pdf(src, from_page=page_number-1, to_page=page_number-1)
        output_path = Output(
            input_file, outputdir, action="split", suffix=f"page_{page_number}"
        )
        doc.save(output_path)
        doc.close()
    else:
        raise ValueError("Page number must be between 1 and {}.".format(len(src)))


"""Split Range Pages Function"""


def doSplitRangePages(input_file, from_page_number, to_page_number, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to split and make sure it is a PDF file."
        )
    src = fitz.open(input_file)
    if from_page_number >= 1 and to_page_number >= from_page_number and to_page_number <= len(src):
        doc = fitz.open()
        doc.insert_pdf(src, from_page=from_page_number-1, to_page=to_page_number-1)
        output_path = Output(
            input_file,
            outputdir,
            action="split",
            suffix=f"page_{from_page_number}_{to_page_number}",
        )
        doc.save(output_path)
        doc.close()
    else:
        raise ValueError("Page number must be between 1 and {}.".format(len(src)))


"""Rotate All Pages Function"""


def doRotate(input_file, rotation_angle: int, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to rotate and make sure it is a PDF file."
        )
    if rotation_angle is None:
        raise ValueError("please provide a rotation angle.")
    output_path = Output(input_file, outputdir, action="rotate", suffix=rotation_angle)
    doc = fitz.open(input_file)
    for page in doc:
        page.set_rotation(rotation_angle)
    doc.save(output_path)
    doc.close()


"""Custom Rotate Page Function"""


def doRotateCustomPage(input_file, rotation_angle: int, page_number: int, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to rotate and make sure it is a PDF file."
        )
    if rotation_angle is None:
        raise ValueError("please provide a rotation angle.")
    if page_number < 1:
        raise ValueError("page number must be 1 or greater.")
    output_path = Output(input_file, outputdir, action="rotate", suffix=f"page_{page_number}_{rotation_angle}")
    doc = fitz.open(input_file)
    if 1 <= page_number <= len(doc):
        page = doc[page_number-1]
        page.set_rotation(rotation_angle)
        doc.save(output_path)
        doc.close()
    else:
        raise ValueError("page number must be between 1 and {}.".format(len(doc)))


"""Rotate Range Pages Function"""


def doRotateRangePages(input_file, rotation_angle: int, start_page: int, end_page: int, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to rotate and make sure it is a PDF file."
        )
    if rotation_angle is None:
        raise ValueError("please provide a rotation angle.")
    if start_page < 1:
        raise ValueError("start page number must be 1 or greater.")
    if end_page < start_page:
        raise ValueError(
            "end page number must be greater than or equal to the start page."
        )
    doc = fitz.open(input_file)
    output_path = Output(input_file, outputdir, action="rotate", suffix=f"page_{start_page}_{end_page}_{rotation_angle}")
    if end_page > len(doc):
        raise ValueError(
            "end page number exceeds the total number of pages in the PDF."
        )
    for page_number in range(start_page, end_page + 1):
        page = doc[page_number-1]
        page.set_rotation(rotation_angle)
    doc.save(output_path)
    doc.close()


"""Merge PDF Function"""


def doMerge(input_files, outputdir):
    if not input_files:
        raise ValueError(
            "please provide a file to merge and make sure it is a PDF file."
        )
    if len(input_files) < 2:
        raise ValueError("please provide a file at least 2 files.")
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    merged_doc = fitz.open()
    for input_file in input_files:
        doc = fitz.open(input_file)
        merged_doc.insert_pdf(doc)
        doc.close()

    """
    To prevent an error with name when saving a file.
    """

    output_file_name = (
        "".join(random.choice(string.ascii_lowercase) for _ in range(5)) + ".pdf"
    )
    output_path = os.path.join(outputdir, output_file_name)
    merged_doc.save(output_path)
    merged_doc.close()


"""Encrypt PDF Function"""


def doEncrypt(input_file, userpass, ownerpass, encryption_method, permissions, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to encrypt and make sure it is a PDF file."
        )
    if not userpass and not ownerpass:
        raise ValueError("please provide the user and the owner password.")
    if isEncrypted(input_file):
        raise ValueError("the file is already encrypted.")
    output_path = Output(
        input_file, outputdir, action="encrypt", suffix=encryption_method
    )
    perm = fitz.PDF_PERM_ACCESSIBILITY
    try:
        if permissions.get("print", True):
            perm |= fitz.PDF_PERM_PRINT
        if permissions.get("copy", True):
            perm |= fitz.PDF_PERM_COPY
        if permissions.get("annotate", True):
            perm |= fitz.PDF_PERM_ANNOTATE
        if permissions.get("modify", True):
            perm |= fitz.PDF_PERM_MODIFY
        if permissions.get("form", True):
            perm |= fitz.PDF_PERM_FORM
        if permissions.get("assemble", True):
            perm |= fitz.PDF_PERM_ASSEMBLE
        if permissions.get("printhq", True):
            perm |= fitz.PDF_PERM_PRINT_HQ
    except:
        pass
    pdf = fitz.open(input_file)
    encrypt_dict = {
        "AES_256": fitz.PDF_ENCRYPT_AES_256,
        "AES_128": fitz.PDF_ENCRYPT_AES_128,
        "RC4_128": fitz.PDF_ENCRYPT_RC4_128,
        "RC4_40": fitz.PDF_ENCRYPT_RC4_40,
    }
    encrypt_meth = encrypt_dict.get(encryption_method)
    pdf.save(
        output_path,
        encryption=encrypt_meth,
        user_pw=userpass,
        owner_pw=ownerpass,
        permissions=int(perm),
    )


"""Decrypt PDF Function"""


def doDecrypt(input_file, password, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to decrypt and make sure it is a PDF file."
        )
    if not password:
        raise ValueError("please provide the user or the owner password.")
    if not isEncrypted(input_file):
        raise ValueError("the file is not encrypted.")
    output_path = Output(input_file, outputdir, action="decrypt")
    decrypt_meth = fitz.PDF_ENCRYPT_NONE
    if isEncrypted(input_file):
        pdf = fitz.open(input_file)
        if pdf.authenticate(password):
            pdf.save(output_path, encryption=decrypt_meth)


"""Convert PDF TO DOCX Function"""


def do2docx(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to convert and make sure it is a PDF file."
        )
    output_path = Output(input_file, outputdir, action="pdf2docx", suffix="Converted")
    cv = Converter(input_file)
    cv.convert(output_path)
    cv.close()


"""Convert All Pages Into PNG Format"""


def do2png(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to convert and make sure it is a PDF file."
        )
    doc = fitz.open(input_file)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        output_path = Output(
            input_file, outputdir, action="pdf2png", suffix=f"page_{page.number+1}"
        )
        pix.save(output_path)
    doc.close()


"""Convert All Pages Into JPG Format"""


def do2jpg(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to convert and make sure it is a PDF file."
        )
    doc = fitz.open(input_file)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        output_path = Output(
            input_file, outputdir, action="pdf2jpg", suffix=f"page_{page.number+1}"
        )
        pix.save(output_path)
    doc.close()


"""Compress PDF With Loseless Function"""


def doCompressLoseLess(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to compress and make sure it is a PDF file."
        )
    output_path = Output(input_file, outputdir, action="compress")
    pdf = fitz.open(input_file)
    pdf.save(
        output_path,
        deflate=True,
        garbage=4,
        deflate_fonts=True,
    )


"""Compress PDF With Removing Duplication"""


def doCompressRemoveDuplication(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to compress and make sure it is a PDF file."
        )
    output_path = Output(input_file, outputdir, action="compress")
    pdf_reader = PR(input_file)
    pdf_writer = PW()
    unique_pages = []
    for page_num in range(len(pdf_reader.pages)):
        current_page = pdf_reader.pages[page_num]
        if current_page not in unique_pages:
            unique_pages.append(current_page)
            pdf_writer.add_page(current_page)

    with open(output_path, "wb") as out:
        pdf_writer.write(out)


"""Compress PDF With Removing All Images"""


def doCompressRemoveImages(input_file, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to compress and make sure it is a PDF file."
        )
    output_path = Output(input_file, outputdir, action="compress")
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.remove_images()
    with open(output_path, "wb") as f:
        writer.write(f)


"""Delete Page"""


def doDeletePage(input_file, page_number, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to delete and make sure it is a PDF file."
        )
    if page_number < 1:
        raise ValueError("page number must be greater than or equal to 1.")
    doc = fitz.open(input_file)
    if 1 <= page_number <= len(doc):
        output_path = Output(
            input_file,
            outputdir,
            action="delete_page",
            suffix=f"deleted_page_{page_number}",
        )
        doc.delete_page(page_number-1)
        doc.save(output_path)
    else:
        raise ValueError("page number must be between 1 and {}.".format(len(doc)))


"""Delete Pages"""


def doDeletePages(input_file, from_page_number, to_page_number, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to delete and make sure it is a PDF file."
        )
    if from_page_number < 1 or to_page_number < from_page_number:
        raise ValueError("invalid page range. page numbers must be greater than or equal to 1, and 'to_page' must be greater than or equal to 'from_page'.")
    doc = fitz.open(input_file)
    num_pages = len(doc)
    if from_page_number > num_pages or to_page_number > num_pages:
        raise ValueError("page numbers exceed the total number of pages in the PDF.")
    output_path = Output(
        input_file,
        outputdir,
        action="delete_pages",
        suffix=f"deleted_page_{from_page_number}_{to_page_number}",
    )
    doc.delete_pages(from_page=from_page_number-1, to_page=to_page_number-1)
    doc.save(output_path)


"""Re-Arrange Page"""


def doReArrange(input_file, from_page_number, to_page_number, outputdir):
    if not input_file:
        raise FileNotFoundError(
            "please provide a file to re-arrange and make sure it is a PDF file."
        )
    if from_page_number < 1 or to_page_number < 1:
        raise ValueError("page numbers must be greater than or equal to 1.")
    doc = fitz.open(input_file)
    num_pages = len(doc)
    if from_page_number > num_pages or to_page_number > num_pages:
        raise ValueError("page numbers exceed the total number of pages in the PDF.")
    output_path = Output(input_file, outputdir, action="re_arrange", suffix=f"page_{from_page_number}_{to_page_number}")
    doc.move_page(from_page_number-1, to_page_number-1)
    doc.save(output_path)
