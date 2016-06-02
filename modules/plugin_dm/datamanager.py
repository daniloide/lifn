# -*- coding: utf-8 -*-
from gluon.sqlhtml import *
from gluon.html import *
from gluon import current
from importer import *
from exporter import *
"""
request = current.request
session = current.session
response = current.response
logged = session.auth and session.auth.user
"""

class DataManager(object):
    _isTable=False
    _actionTableName=None
    _rActionURL=None
    _rDetailsURL=None
    _gFieldId=None
    _gDefaultOrder=None
    _gFields=[]
    _gHeaders={}
    _gPaginate=25
    _showId=False
    _showSearch=True
    _query=None
    _rCheckInRows=True
    _muestreo=None

    # Data export
    exportClasses = dict(
        tsv=( ExporterTSV, current.T('TSV') ),
        csv=( ExporterCSV, current.T('CSV') ),
        html=( ExporterHTML, current.T('HTML') ),
        pdf=( ExporterPDF, current.T('PDF') ),
        json=( ExporterJSON, current.T('JSON') ),
        xml=( ExporterXML, current.T('XML') )
    )
    # Data import
    importClasses = dict(
        tsv=( ImporterTSV, current.T('TSV') ),
        csv=( ImporterCSV, current.T('CSV') ),
        json=( ImporterJSON, current.T('JSON') ),
        xml=( ImporterXML, current.T('XML') )
    )


    def __init__(self, database, muestreo, tablename=None, showmactions=True, showdactions=False):
        # database is required
        if database:
            self._db=database
            if tablename:
                # Just a table
                if tablename in self._db.tables:
                    try:
                        self._actionTableName=tablename
                        self._isTable=True
                        self._id='id'
                        self._gFieldId=self._db[tablename][self._id]
                        self._query=(self._db[tablename].muestreo == muestreo)
                        self._gFields=[ self._db[tablename][f] for f in self._db[tablename].fields ]
                        self._gDefaultOrder=self._gFieldId
                        self._muestreo=muestreo
                        #self._gHeaders=[ db[tablename][fn].label for fn in db[tablename].fields ]
                    except:
                        raise HTTP(200, current.T('Table %s doesnt have id field') % tablename)
                else:
                    raise HTTP(200, current.T('Database doesnt have table %s') % tablename)
            else:
                # May be a query!. Setup later!.
                pass
            self._showMActions=showmactions
            self._showDActions=showdactions
            self._rActionURL="/%s/plugin_dm/neddaction.load" % (current.request.application)
        else:
            raise HTTP(200, current.T('No database'))


    def __url2(self, **b):
        # From SQLFORM
        b['args'] = current.request.args + b.get('args', [])
        localvars = current.request.get_vars.copy()
        localvars.update(b.get('vars', {}))
        b['vars'] = localvars
        b['hash_vars'] = False
        # b['user_signature'] = user_signature
        return URL(**b)


    def showMActions(self, val):
        self._showMActions=val


    def showDActions(self, val):
        self._showDActions=val


    def showCheckInRows(self, val):
        self._rCheckInRows=val


    def actionTableName(self, tablename):
        if tablename in self._db.tables:
            self._actionTableName=tablename
        else:
            pass


    ## Begin grid elements
    def gFieldId(self, id='id'):
        if self._actionTableName:
            self._id=id
            self._gFieldId=self._db[self._actionTableName][id]
        else:
            pass

    def gQuery(self, q):
        # Not a table. It is a query
        self._query=q
        self._isTable=False


    def gFields(self, fcols):
        # cols = [(tablename,fieldname),(tablename,fieldname), ... ]
        flist=[]
        for t in fcols:
            tablename=t[0]
            fieldname=t[1]
            if tablename in self._db.tables:
                if fieldname in self._db[tablename].fields:
                    flist.append( self._db[tablename][fieldname] )
                else:
                    print "Field (%s) is not in table (%s)" % (fieldname, tablename)
            else:
                print "The is no table (%s) in database" % tablename
        self._gFields=flist
        if len(self._gFields)>0:
            self._gHideOthersFields()

    def _gHideOthersFields(self):
        from sets import Set
        # Get tables in query
        dbset = self._db(self._query)
        tablenames = self._db._adapter.tables(dbset.query)
        tables = [self._db[tablename] for tablename in tablenames]
        fields= []
        for table in tables:
            for f in table:
                fields.append(f)
        allF = Set( fields )
        toShow = Set(self._gFields)
        toHide = allF - toShow
        for f in toHide:
            f.readable=False

    def gHeaders(self, head):
        #head=['label1', 'label2', ...]
        gridhead={}
        if len(head)==len(self._gFields):
            cont=0
            for l in head:
                # str(field) da tablename.fieldname
                gridhead[ '%s' % self._gFields[cont] ]=l
                cont=cont+1
        else:
            print "Fields and headers must have same size"
        self._gHeaders=gridhead


    def gShowId(self, val):
        # Grid hhas colum with ids
        if self._gFieldId:
            self._showId=val
            self._gFieldId.readable=val
        else:
            pass


    def gShowSearch(self, val):
        #Grid have serach box
        self._showSearch=val


    def gPaginate(self,nrows):
        self._gPaginate=nrows

    def gOrder(self,order):
        self._gDefaultOrder=order

    def gRowsLinks(self,rid):
        #Custom links for every row
        """
        html=None
        if self._showMActions:
            html=SPAN(
                self.rEditButton(rid),
                self.rDeleteButton(rid)
            )
        if self._showDActions:
            if html:
                html=SPAN(html,rDetailsButton(rid))
            else:
                html=detailButton
        return html
        """
        return SPAN(
            SPAN(self.rEditButton(rid), self.rDeleteButton(rid)) if self._showMActions else '',
            self.rDetailsButton(rid) if self._showDActions else '',
            self.rCheckControl(rid) if self._rCheckInRows else ''
        )
    ## End grid elements

    ## Begin row elements
    def rActionURL(self, url):
        #new, edit, delete and deleteall actions
        self._rActionURL=url


    def rDetailsURL(self, url):
        #details
        self._rDetailsURL=url


    def rEditButton(self, rid):
        return A(
            I(_class='icon-edit icon-white'),
            _class='btn btn-inverse btn-mini',
            _title=current.T('Edit this record'),
            _onclick="return editDialogShow('%s','%s',%d);" % (self._rActionURL, self._actionTableName, rid)
        )


    def rDeleteButton(self, rid):
        return A(
            I(_class='icon-trash icon-white'),
            _class='btn-warning btn-mini',
            _style="background-color: #FBCD00; color: rgb(246, 200, 43);background-image: -webkit-linear-gradient(top, rgb(246, 200, 43), rgb(246, 200, 43));",
            _title=current.T('Delete this record'),
            _onclick="return deleteDialogShow('%s','%s', %d);" % (self._rActionURL, self._actionTableName, rid)
        )


    def rDetailsButton(self,rid):
        return A(
            I(_class='icon-th-large icon-white'),
            _class='btn btn-inverse btn-mini',
            _title=current.T('Edit details records'),
            _onclick="return detailsEDialogShow('%s', %d);" % (self._rDetailsURL, rid),
            #_onmouseover="return detailsSDialogShow('%s', %d);" % (self._rActionURL, rid)
        )


    def rCheckControl(self, rid):
        return INPUT(
            _type="checkbox",
            _class='row-checkbox',
            _title=current.T('Select this record'),
            _id="rowcheck_%s" % rid,
            _onclick="checkControlOthers();"
        )
    ## End row elements


    ## Begin toolbar elements
    def tNewButton(self):
        return A(
            SPAN(
                I(_class='icon-pencil icon-white'),
                current.T('Add record')
            ),
            _class='btn btn-inverse btn-mini',
            _title=current.T('Add new record to this table'),
            _onclick="return newDialogShow('%s','%s');" % (self._rActionURL, self._actionTableName),
        )


    def tExportButton(self):
        export_links = []
        if not self._db(self._query).isempty():
            for k, v in sorted(self.exportClasses.items()):
                if not v:
                    continue
                label = v[1] if hasattr(v, "__getitem__") else k
                link = self.__url2(vars=dict(
                    order=current.request.vars.order or '',
                    _export_type=k,
                    keywords=current.request.vars.keywords or '')
                )
                export_links.append(A(current.T(label), _href=link))
        else:
            pass

        return DIV(
            BUTTON(
                SPAN(
                    I(_class='icon-download icon-white'),
                    current.T('Export')
                ),
                _class="btn btn-mini btn-inverse",
                _title=current.T('Export data to file'),
            ),
            BUTTON(
                SPAN(
                    _class="caret"
                ),
                **{
                    '_class':'btn btn-mini btn-inverse dropdown-toggle',
                    '_data-toggle':'dropdown'
                }
            ),
            UL(
                _class="dropdown-menu",
                *[LI(l) for l in export_links]
            ),
            _class="btn-group"
        )


    def tImportButton(self):
        import_links = []
        for k, v in sorted(self.importClasses.items()):
            if not v:
                continue
            label = v[1] if hasattr(v, "__getitem__") else k
            link = self.__url2(vars=dict(
                order=current.request.vars.order or '',
                _export_type=k,
                keywords=current.request.vars.keywords or '')
            )
            import_links.append(A(current.T(label), _href=link))

        return DIV(
            BUTTON(
                SPAN(
                    I(_class='icon-upload icon-white'),
                    current.T('Import')
                ),
                _class="btn btn-mini btn-inverse",
                _title=current.T('Import data from file'),
            ),
            BUTTON(
                SPAN(
                    _class="caret"
                ),
                **{
                    '_class':'btn btn-mini btn-inverse dropdown-toggle',
                    '_data-toggle':'dropdown'
                }
            ),
            UL(
                _class="dropdown-menu",
                *[LI(x) for x in import_links]
            ),
            _class="btn-group"
        )

    def tUtilButton(self):
        #If rows are selectables then utils button
        util_links=[]
        util_links.append( A(current.T('Select all'), _onclick='selectAllRows(true)',_id='selectAllRows') )
        util_links.append( A(current.T('Unselect selected'), _onclick='selectAllRows(false)',_id='unselectRows', _style="display:none") )
        if self._rCheckInRows:
            util_links.append( A(current.T('Clone selected'), _onclick='cloneSelectedRows', _id='cloneSelectedRows', _style="display:none") )
        else:
            pass

        return DIV(
            BUTTON(
                SPAN(
                    I(_class='icon-check icon-white'),
                    current.T('Utils')
                ),
                _class="btn btn-mini btn-inverse",
                _title=current.T('Utilities for selected rows'),
            ),
            BUTTON(
                SPAN(
                    _class="caret"
                ),
                **{
                    '_class':'btn btn-mini btn-inverse dropdown-toggle',
                    '_data-toggle':'dropdown'
                }
            ),
            UL(
                _class="dropdown-menu",
                *[LI(x) for x in util_links]
            ),
            _class="btn-group"
        )


    def tDeleteButton(self):
        delete_links=[]
        if self._rCheckInRows:
            delete_links.append(
                A(
                    current.T('Delete selected'),
                    _id='gMenu_DeleteSelected',
                    _title=current.T('Delete selected records in this table'),
                    _onclick='deleteSelected',
                    _class='disabled'
                )
            )
        else:
            pass
        delete_links.append( SPAN(_class="divider") )
        delete_links.append(
            A(
                current.T('Delete all'),
                _id='deleteAll',
                _title=current.T('Delete all records in this table'),
                _onclick="return deleteAllDialogShow('%s','%s');" % (self._rActionURL, self._actionTableName)
            )
        )
        return DIV(
            BUTTON(
                SPAN(
                    I(_class='icon-trash icon-white'),
                    current.T('Delete')
                ),
                _class="btn btn-warning btn-mini",
                _title=current.T('Delete records'),
            ),
            BUTTON(
                SPAN(
                    _class="caret"
                ),
                **{
                    '_class':'btn btn-warning btn-mini dropdown-toggle',
                    '_data-toggle':'dropdown'
                }
            ),
            UL(
                _class="dropdown-menu",
                *[LI(x) for x in delete_links]
            ),
            _class="btn-group"
        )
    ## Begin toolbar elements


    def grid(self):
        # print row
        return SQLFORM.grid(
            query=self._query,
            fields=self._gFields,
            # headers=self._gHeaders,
            links=[ lambda row: self.gRowsLinks( row[self._id] if self._isTable else row[self._actionTableName][self._id] ) ] if (self._showMActions or self._showDActions) else None,
            field_id=self._gFieldId,
            orderby=self._gDefaultOrder,
            paginate=self._gPaginate,
            sortable=True,
            csv=False, # hide exports!?
            details=False,
            create=False,
            deletable=False,
            editable=False,
            showbuttontext=False,
            maxtextlength=64,
            exportclasses=None,
            ui='web2py',
            formstyle='table3cols',
            _class="web2py_grid",
        )


    def toolBar(self):
        return SPAN(self.tNewButton())
        #return SPAN(self.tNewButton(),self.tDeleteButton() if self._showMActions else '')
