# -*- coding: utf-8 -*-
from gluon.sqlhtml import *

class ExporterPDF(ExportClass):
    label = 'PDF'
    file_ext = "pdf"
    content_type = "text/pdf"

    def __init__(self, rows):
        ExportClass.__init__(self, rows)

    def export(self):
        if self.rows:
            return self.rows.as_xml()
        else:
            return '<rows></rows>'

