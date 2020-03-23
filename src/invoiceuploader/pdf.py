#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue
from time import localtime, strftime

bcp = "/".join(__file__.split("/")[:-2])


def getDaleDir():
    """
    Gibt das Directory für die Speicherung der Dokumente
    zurück und legt das Verzeichnis an, wenn es nicht
    bereits existiert.
    """
    basepath = "/tmp/ausgang/fax133"
    archdir = datetime.datetime.now().strftime("%y/%m/%d")
    path = "%s/%s" % (basepath, archdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum):
    c.setFillColor(black)
    c.setFont(schriftartfett, 10)
    c.drawString(2.2 * cm, 28.5 * cm, u"Upload-Eingangsdokument")
    c.setFont(schriftart, 8)
    t1 = u"Dieses Formular wurde über den Online-Service der Unfallkasse Hessen erstellt und versandt und trägt daher keine Unterschrift."
    c.drawString(2.2 * cm, 1.5 * cm, t1)
    return c


def UploadPdf(data, tmp):

    data = {}
    data["anrede"] = u"Herr"
    data["titel"] = u""
    data["nachname"] = u"Seibert"
    data["vorname"] = u"Markus"
    data["email"] = u"m.seibert@ukh.de"
    data["telefon"] = u"069-29972-526"
    data["aktz"] = u"2020000001"
    data["unternehmen"] = u"Unfallkasse / KT"
    data["notiz"] = u"bla bla bla...."

    seite = 1
    datum = str(strftime("%d.%m.%Y", localtime()))
    if tmp is None:
        datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
        # Datei Name Verzeichnis
        verzeichnis = getDaleDir()
        # dateiname = datum2 + '_' + grunddaten.context.id + '.pdf'
        dateiname = datum2 + ".pdf"
        saveverzeichnis = verzeichnis + "/" + dateiname
    else:
        saveverzeichnis = tmp
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u"Druckversion")
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    # Seite 1
    c = pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum)
    y1 = 28.5
    x1 = 16
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Seite: " + str(seite))
    # Empfänger (UKH)
    y1 = 26.0
    x1 = 2.2
    c.setFont(schriftartfett, 12)
    c.drawString(x1 * cm, y1 * cm, u"Unfallkasse Hessen")
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u"Leonardo-da-Vinci-Allee 20")
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"60486 Frankfurt am Main")
    # Absender
    c.setFillColor(black)
    c.setFont(schriftartfett, 16)
    c.drawString(2.2 * cm, 22 * cm, u"Upload " + datum)
    # Daten
    c.setFont(schriftart, 11)
    y1 = 21.0
    x1 = 2.2
    x2 = 7.0
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Anrede:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["anrede"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Titel:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["titel"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Nachname, Vorname:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["nachname"] + u", " + data["vorname"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"E-Mail:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["email"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Telefon:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["telefon"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Aktenzeichen:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["aktz"])
    y1 -= 0.5
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Unternehmen:")
    c.setFont(schriftart, 11)
    c.drawString(x2 * cm, y1 * cm, data["unternehmen"])
    y1 -= 1.0
    c.setFont(schriftartfett, 11)
    c.drawString(x1 * cm, y1 * cm, u"Notiz:")
    y1 -= 0.5
    text = cutrow(data["notiz"], 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x1 * cm, y1 * cm, text[z1])
        z1 += 1
    # ----------------------------------------------
    # Seitenwechsel
    # ----------------------------------------------
    c.showPage()
    c = pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum)
    seite += 1
    c.setFillColor(black)
    c.setFont(schriftartfett, 11)
    y1 = 28.5
    x1 = 16
    c.drawString(x1 * cm, y1 * cm, u"Seite: " + str(seite))
    # ----------------------------------------------

    # Hier müsste ein Bild etc. eingefügt werden...
    #
    # ????

    # Seitenumbruch
    c.showPage()
    # ENDE und Save
    c.save()
    return saveverzeichnis


def cutrow(text, ende=100, maxrows=20, maxstring=3000):
    text = text.replace("<br />", "\n")
    text = text.replace("<p>", "")
    text = text.replace("</p>", "")
    text = text.replace("<ul>", "")
    text = text.replace("</ul>", "")
    text = text.replace("<ol>", "")
    text = text.replace("</ol>", "")
    text = text.replace("<li>", "  - ")
    text = text.replace("</li>", "")
    text = text.replace('<span style="text-decoration: underline;">', "")
    text = text.replace("</span>", "")
    text = text.replace("<em>", "")
    text = text.replace("</em>", "")
    text = text.replace('<p style="text-align: left;">', "")
    text = text.replace('<p style="text-align: center;">', "")
    text = text.replace('<p style="text-align: right;">', "")
    text = text.replace("<strong>", "")
    text = text.replace("</strong>", "")
    text = text.replace('<span style="font-size: 10px;">', "")
    text = text.replace('<span style="font-size: 12px;">', "")
    text = text.replace('<span style="font-size: 13px;">', "")
    text = text.replace('<span style="font-size: 14px;">', "")
    text = text.replace('<span style="font-size: 16px;">', "")
    text = text.replace('<span style="font-size: 18px;">', "")
    text = text.replace('<span style="font-size: 20px;">', "")
    text = text.replace("\t", "     ")
    text = text.replace("\r", " ")
    start = 0
    konstante = ende
    druckliste = []
    laenge = len(text) / 5
    if laenge == 0:
        laenge = 1
    for x in range(laenge):
        if start != -1:
            textteil = text[start:ende]
            # Klaerung, ob bereits Umbrueche vorhanden sind
            umbruch = textteil.find("\n")
            # Wenn nein, Einbau eines Umbruches
            if umbruch == -1:
                if textteil > " ":
                    if len(textteil) < konstante:
                        druckliste.append(textteil)
                        zeilenende = konstante
                    else:
                        zeilenende = textteil.rfind(" ")
                        druckliste.append(textteil[:zeilenende])

                    # Wenn kein anderer Text mehr kommt - Abbruch
                    if start == start + zeilenende + 1:
                        start = -1
                    else:
                        start = start + zeilenende + 1
                        ende = start + konstante
            # Wenn ja, dann weiter mit dem naechsten Textteil
            else:
                druckliste.append(textteil[:umbruch])

                # Wenn kein neuer Text mehr kommt - Abbruch
                if start == start + umbruch + 1:
                    start = -1
                else:
                    start = start + umbruch + 1
                    ende = start + konstante
    return druckliste
