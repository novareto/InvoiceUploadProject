# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


from zope import interface, schema
from grokcore.component import provider
from uvc.uploader.field import FilesField
from uvc.protectionwidgets import Captcha
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@provider(IContextSourceBinder)
def source_anrede(context):
    return SimpleVocabulary([
        SimpleTerm(u'', u'', u''),
        SimpleTerm(u'Herr', u'Herr', u'Herr'),
        SimpleTerm(u'Frau', u'Frau', u'Frau'),
        SimpleTerm(u'Divers', u'Divers', u'Divers'),
    ])


class IInvoiceUploader(interface.Interface):
    """ """


class IInvoice(interface.Interface):

    anrede = schema.Choice(
        title=u"Anrede:",
        description=u"",
        source=source_anrede,
        required=True
    )

    titel = schema.TextLine(
        title=u"Titel:",
        description=u"",
        required=False
    )

    nachname = schema.TextLine(
        title=u"Nachname:",
        description=u"",
        required=True
    )

    vorname = schema.TextLine(
        title=u"Vorname:",
        description=u"",
        required=True
    )

    email = schema.TextLine(
        title=u"E-Mail:",
        description=u"",
        required=True
    )

    telefon = schema.TextLine(
        title=u"Telefon:",
        description=u"",
        required=True
    )

    aktz = schema.TextLine(
        title=u"Aktenzeichen:",
        description=u"",
        required=False
    )

    unternehmen = schema.TextLine(
        title=u"Versichertes Unternehmen:",
        description=u"",
        required=False
    )

    notiz = schema.Text(
        title=u"Ihre Mitteilung an uns:",
        description=u"",
        required=False
    )

    anlagen = FilesField(
        title=u"Anlagen",
        description=u"Bitte beachten Sie, dass nur folgende Formate zugelassen werden. (gif, png, jpeg, pdf)",
        required=False
    )

    datenschutz = schema.Bool(
        title=u"Datenschutz",
        description=u"Hiermit bestätige ich die Datenschutzbedingungen der UKH",
        required=True
    )

    captcha = Captcha(
        title=u"Sicherheitscode",
        required=True
    )
