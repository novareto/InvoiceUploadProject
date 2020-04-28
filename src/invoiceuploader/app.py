# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import img2pdf
import logging
import tempfile
import subprocess
import grokcore.view as grok
import re
import os

from StringIO import StringIO
from invoiceuploader import resource
from PIL import Image
from .pdf import UploadPdf
from datetime import datetime
from zeam.form.layout import Form
from invoiceuploader import interface
from zope.interface import implementer
from megrok.nozodb import ApplicationRoot
from zeam.form.base import action, Fields
from dolmen.forms.base import ApplicationForm
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from zope.app.appsetup.product import getProductConfiguration
from uvc.tbskin.viewlets import FlashMessages
from zeam.form.base.markers import NO_VALUE
from ukhtheme.grok.viewlets import BGHeader

logger = logging.getLogger('impageuploader')


settings = getProductConfiguration('settings')


grok.templatedir("templates")


class BGHeader(BGHeader):

    def application_url(self):
        return u"http://www.ukh.de"


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
            self.flash(u'Es sind leider Fehler aufgetreten')
            return
        if data['anrede'] == '':
            self.flash(u'Bitte wählen Sie eine Anrede aus.')
            return
        if data['email'] != '':
            checkmail = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$").match
            if not bool(checkmail(data['email'])):
                self.flash(u'Bitte tragen Sie eine gültige E-Mail Adresse ein.')
                return
        if data['datenschutz'] is False:
            self.flash(u'Bitte bestätigen Sie die Datenschutzerklärung der UKH.')
            return
        for x in data['anlagen']:
            if x == NO_VALUE:
                self.flash(u'Sie haben keine Dateien zum Upload ausgewählt!')
                return
        output_path = settings.get('output_path')
        pdfstreams = []
        pdf_fn = UploadPdf(data, None)
        for attachment in data.get('anlagen'):
            print attachment.filename
            if "pdf" in attachment.filename:
                pdfstreams.append(attachment)


            elif "heic" in attachment.filename:
                from backports.tempfile import TemporaryDirectory
                with TemporaryDirectory() as tmpdirname:
                    ifn = '%s/%s' % (tmpdirname, attachment.filename)
                    ofn = '%s/%s.jpg' % (tmpdirname, attachment.filename)
                    import pdb; pdb.set_trace()

                    with open(ifn, 'wb') as heic:
                        heic.write(attachment.read())
                    subprocess.call(["heif-convert", ifn, ofn])
                    with open(ofn, 'rb') as f:
                        rgbimage = Image.open(f)
                        jpegimage = StringIO()
                        rgbimage.save(jpegimage, format="JPEG")
                        jpegimage.seek(0)
                        pdfimage = img2pdf.convert(jpegimage)
                        pdfstreams.append(StringIO(pdfimage))


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
            writer = PdfFileMerger()
            with open(output_file, 'wb') as output:
                writer.append(deckblatt)
                writer.append(reader)
                writer.write(output)
                #for n in range(reader.getNumPages()):
                #    writer.addPage(reader.getPage(n))
                #    writer.write(output)
        self.flash(u'Vielen Dank, wir haben Ihre Dateien erhalten.')
        self.redirect(self.application_url())
