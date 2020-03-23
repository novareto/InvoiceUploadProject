# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import grokcore.view as grok
# from invoiceuploader import resource
from invoiceuploader import interface
from zope.interface import implementer
from megrok.nozodb import ApplicationRoot
from zeam.form.layout import Form
from zeam.form.base import action, Fields
from dolmen.forms.base import ApplicationForm
from .pdf import UploadPdf
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import img2pdf
from StringIO import StringIO


grok.templatedir("templates")


@implementer(interface.IInvoiceUploader)
class InvoiceUploader(ApplicationRoot):
    pass


class LandingPage(ApplicationForm):
    grok.context(interface.IInvoiceUploader)
    grok.name("index")
    grok.require("zope.Public")

    fields = Fields(interface.IInvoice).omit('captcha')

    @action("Senden")
    def handel_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u'Es sind leider Feher aufgetreten')
            return
        output_file = "/tmp/klaus.pdf"
        pdfstreams = []
        pdf_fn = UploadPdf(data, None)
        writer = PdfFileWriter()
        for attachment in data.get('anlagen'):
            if "pdf" in attachment.filename:
                pdfstreams.append(attachment)
            elif "jpeg" in attachment.filename or 'jpg' or 'png' in attachment.filename:
                pilimage = Image.open(attachment)
                if pilimage.mode == "RGBA":
                    rgbimage = pilimage.convert("RGB")
                else:
                    rgbimage = pilimage
                jpegimage = StringIO()
                rgbimage.save(jpegimage, format="JPEG")
                jpegimage.seek(0)
                pdfimage = img2pdf.convert(jpegimage)
                pdfstreams.append(StringIO(pdfimage))
        deckblatt = PdfFileReader(pdf_fn)
        for stream in pdfstreams:
            with open(output_file, 'wb') as output:
                for reader in map(PdfFileReader, pdfstreams):
                    writer.addPage(deckblatt.getPage(0))
                    for n in range(reader.getNumPages()):
                        writer.addPage(reader.getPage(n))
                        writer.write(output)
        print(data)
