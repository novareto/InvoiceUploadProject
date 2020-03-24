# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import img2pdf
import logging
import grokcore.view as grok
from invoiceuploader import resource


from PIL import Image
from .pdf import UploadPdf
from datetime import datetime
from StringIO import StringIO
from zeam.form.layout import Form
from invoiceuploader import interface
from zope.interface import implementer
from megrok.nozodb import ApplicationRoot
from zeam.form.base import action, Fields
from dolmen.forms.base import ApplicationForm
from PyPDF2 import PdfFileReader, PdfFileWriter
from zope.app.appsetup.product import getProductConfiguration
from uvc.tbskin.viewlets import FlashMessages


logger = logging.getLogger('impageuploader')


settings = getProductConfiguration('settings')


grok.templatedir("templates")


@implementer(interface.IInvoiceUploader)
class InvoiceUploader(ApplicationRoot):
    pass


class FlashMessages(FlashMessages):
    pass


class LandingPage(ApplicationForm):
    grok.context(interface.IInvoiceUploader)
    grok.name("index")
    grok.require("zope.Public")

    fields = Fields(interface.IInvoice)

    def update(self):
        resource.style.need()

    @action("Senden")
    def handel_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u'Es sind leider Feher aufgetreten')
            return
        output_path = settings.get('output_path')
        pdfstreams = []
        pdf_fn = UploadPdf(data, None)
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
        fn_base = datetime.now().strftime('%Y%m%d_%H%M%S')
        for i, reader in enumerate(map(PdfFileReader, pdfstreams)):
            output_file = "%s/%s_%s.pdf" % (output_path, fn_base, i)
            logger.info('Write File %s' % output_file)
            writer = PdfFileWriter()
            with open(output_file, 'wb') as output:
                writer.addPage(deckblatt.getPage(0))
                for n in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(n))
                    writer.write(output)
        self.flash(u'Vielen Dank wir haben Ihre Dateien erhalten.')
        self.redirect(self.application_url())
