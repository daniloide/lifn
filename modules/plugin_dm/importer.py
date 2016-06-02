# -*- coding: utf-8 -*-
class ImportClass(object):
    label = None
    file_ext = None
    content_type = None

    def __init__(self, rows):
        self.rows=rows


    def importData(self):
        raise NotImplementedError


class ImporterTSV(ImportClass):
    label = 'TSV'
    file_ext = "tsv"
    content_type = "text/tsv"

    def __init__(self, rows):
        ImportClass.__init__(self, rows)

    def importData(self):
        pass


class ImporterCSV(ImportClass):
    label = 'CSV'
    file_ext = "csv"
    content_type = "text/csv"

    def __init__(self, rows):
        ImportClass.__init__(self, rows)

    def importData(self):
        pass


class ImporterJSON(ImportClass):
    label = 'JSON'
    file_ext = "json"
    content_type = "text/json"

    def __init__(self, rows):
        ImportClass.__init__(self, rows)

    def importData(self):
        pass


class ImporterXML(ImportClass):
    label = 'XML'
    file_ext = "xml"
    content_type = "text/xml"

    def __init__(self, rows):
        ImportClass.__init__(self, rows)

    def importData(self):
        pass
