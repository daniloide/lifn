# -*- coding: utf-8 -*-
# db is global variable here!?
# Data acction for the data
dataActions=['new','edit','delete','deleteAll','details']

@auth.requires_login()
def neddaction():
    """
    new, edit, delete and details.
    """
    #All variables come here from POST
    try:
        # Action type
        dataAction=request.post_vars.dataAction
        try:
            # Table name
            tableName=request.post_vars.tableName
            if dataAction=='new':
                print "%s: new" % tableName
                fields = db[tableName].fields()
                fields.remove('muestreo')
                print fields
                form = SQLFORM( db[tableName], _id="datamanager-new", fields=fields)
                dai = INPUT(_name='dataAction',id='%s_dataAction' % tableName, value='new', _type='hidden')
                tn = INPUT(_name='tableName',id='%s_tableName' % tableName, value='%s' % tableName, _type='hidden')
                form.insert(-1,dai)
                form.insert(-1,tn)
                form.vars.muestreo = request.post_vars.muestreo
            elif dataAction=='edit':
                id=request.post_vars.dataId
                print "%s: edit - %s" % (tableName, id)
                record=db[tableName](id) or redirect(URL('default','index'))
                fields = db[tableName].fields()
                fields.remove('muestreo')
                print fields
                form = SQLFORM(db[tableName], record, showid=False, _id="datamanager-edit", fields=fields)
                dai = INPUT(_name='dataAction',id='%s_dataAction' % tableName, value='edit', _type='hidden')
                tn = INPUT(_name='tableName',id='%s_tableName' % tableName, value='%s' % tableName, _type='hidden')
                did = INPUT(_name='dataId',id='%s_dataId' % tableName, value=id, _type='hidden')
                form.insert(-1,dai)
                form.insert(-1,did)
                form.insert(-1,tn)
                form.vars.muestreo = request.post_vars.muestreo
            elif dataAction=='delete':
                # Just delete, dont show form
                id=request.post_vars.dataId
                print "%s: delete - %s" % (tableName, id)
                if db(db[tableName]['id']==id).isempty():
                    response.flash = T('No record deleted')
                    if request.ajax:
                        return response.json( {'result': False, 'msg':T('No record with this %s' % id)}  )
                else:
                    db(db[tableName]['id']==id).delete()
                    response.flash = T('Record deleted')
                    if request.ajax:
                        return response.json( {'result': True } )
            elif dataAction=='deleteAll':
                print "%s: deleteAll" % (tableName)
                if db( db[tableName]['id']>0 ).isempty():
                    response.flash = T('No record deleted')
                    if request.ajax:
                        return response.json( {'result': False, 'msg':T('No records found') }  )
                else:
                    # WARNING: Delete all record in the table!!!
                    db.commit()
                    try:
                        db( db[tableName]['id']>0 ).delete()
                        # db.executesql("SELECT setval('%s_id_seq', 1, true)" % tableName)
                        #db.executesql("ALTER SEQUENCE %s_id_seq MINVALUE 0;" % tableName)
                        #db.executesql("SELECT setval('%s_id_seq', 0, true);" % tableName)
                        response.flash = T('Records deleted')
                        if request.ajax:
                            return response.json( {'result': True } )
                    except:
                        db.rollback()
            else:
                redirect(URL('default','index'))

            #Remove submit button it's ajax
            if request.ajax:
                submit = form.element('input',_type='submit')
                submit['_style'] = 'display:none;'
            else:
                pass
        except:
            print "tableName error"
            pass
    except:
        print "dataAction error"
        pass

    if form.process().accepted:
        print form.vars
        response.flash = T('Form accepted')
        if request.ajax:
            return response.json( {'result': True } )
    elif form.errors:
        response.flash = T('Form has errors')
        if request.ajax:
            return response.json( {'result': False, 'msg':form.errors} )
    else:
        response.flash = T('Please fill the form')
    return dict(form=form)
