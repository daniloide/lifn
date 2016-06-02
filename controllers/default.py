# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

"""
from gluon import *
"""
# RFPV
import logging
logger = logging.getLogger("web2py.app.lifn")
logger.setLevel(logging.DEBUG)

def tipoDeBosque(muestreoId):
    if db( (db.DatosGenerales.muestreo == muestreoId) ).isempty():
        return '-'
    else:
        return db(
            (db.DatosGenerales.muestreo == muestreoId) &
            (db.DatosGenerales.tipoDeBosque == db.TipoBosque.id)
        ).select(
            db.TipoBosque.tipo
        )[0]['tipo']

def index():
    """
    Página principal
    """
    session.show_title = True
    session.menuL_enabled = False
    if not db( (db.auth_user.id > 0) ).isempty():
        if auth.is_logged_in():
            if session.muestreoId:
                session.muestreoId=-1
            if not db( (db.TipoBosque.id > 0) ).isempty():

                # virtual field to complete
                db.Muestreo.completado = Field.Virtual(
                    'completado',
                    lambda row: completedPercentage(row.Muestreo.id)
                )

                """
                db.Muestreo.tb = Field.Virtual(
                    'tb',
                    lambda row: tipoDeBosque(row.Muestreo.id)
                )
                """

                # The query
                query=(
                    (db.Muestreo.punto == db.Punto.id) &
                    (db.MuestreoUsuario.muestreo == db.Muestreo.id) &
                    (db.MuestreoUsuario.usuario == db.auth_user.id)
                )

                left = [
                    db.DatosGenerales.on(db.Muestreo.id==db.DatosGenerales.muestreo),
                    db.MuestreoTipoReporte.on(db.Muestreo.id==db.MuestreoTipoReporte.muestreo),
                ]

                db.Muestreo.id.readable = False
                db.DatosGenerales.id.readable = False
                db.DatosGenerales.muestreo.readable = False
                db.DatosGenerales.fecha.readable = False
                db.DatosGenerales.facilidadProgresion.readable = False
                db.DatosGenerales.propietario.readable = False
                db.DatosGenerales.predio.readable = False
                db.MuestreoTipoReporte.id.readable = False
                db.MuestreoTipoReporte.muestreo.readable = False
                db.MuestreoTipoReporte.comentario.readable = False

                fields = (
                    db.Muestreo.id,
                    db.Punto.nombre,
                    db.Muestreo.anioMuestreo,
                    db.MuestreoUsuario.usuario,
                    db.MuestreoTipoReporte.tipo,
                    db.DatosGenerales.tipoDeBosque,
                    db.DatosGenerales.subbosque,
                    db.Punto.lon,
                    db.Punto.lat,
                    db.DatosGenerales.departamento,
                    db.Muestreo.completado,
                    db.MuestreoUsuario.realizado,
                )

                # hide others fields
                from sets import Set
                dbset = db(query)
                tablenames = db._adapter.tables(dbset.query)
                tables = [db[tablename] for tablename in tablenames]
                afields= []
                for table in tables:
                    for f in table:
                        afields.append(f)
                allF = Set( afields )
                toShow = Set( fields )
                toHide = allF - toShow
                for f in toHide:
                    f.readable=False

                #Define headers as tuples/dictionaries
                headers = {
                    'Muestreo.id':'Id',
                    'Punto.nombre':'Nombre',
                    'Muestreo.anioMuestreo':'Año',
                    'MuestreoUsuario.usuario':'Asignado',
                    'Muestreo.completado':'Completado (%)',
                    'Muestreo.tb':'Tipo bosque',
                    'Punto.lon':'Longitud',
                    'Punto.lat':'Latitud',
                }

                #Let's specify a default sort order on date_of_birth column in grid
                default_sort_order=[db.Punto.nombre]

                app = '%s' % ( request.application)
                # links
                links = [
                    dict(

                        header = T('Edit'),
                        body = lambda row: A(
                            I(_class='icon-edit icon-white'),
                            _class='btn btn-small',
                            _title=current.T('Edit this record'),
                            #_onclick="return editDialogShow('%s','%s',%d);" % (self._rActionURL, self._actionTableName, rid)
                            _href=URL( app , 'default', 'datosGenerales?m=%s' % (row.Muestreo.id) ),
                        )
                    )
                ]

                #Creating the grid object
                grid = SQLFORM.grid(
                    query=query,
                    left=left,
                    field_id=db.Muestreo.id,
                    fields=fields,
                    headers=headers,
                    orderby=default_sort_order,
                    links=links,
                    create=False,
                    deletable=False,
                    editable=False,
                    details=False,
                    maxtextlength=64,
                    paginate=50
                )
                stats = estadisticas()
                return dict(logged_in=auth.is_logged_in(), show_title=False, stats = stats, user = user, grid=grid)
            else:
                redirect(URL('loadTypes'))
        else:
            redirect(URL('user/login'))
    else:
        redirect(URL('firstRun'))

def tablePunto():
    string = request.get_vars['search']
    if not string:
        string = ''
    if session.has_key('plant'):
        del session.plant
    user = 'user'
    if auth.user != None and auth.has_membership('administrador', auth.user.id):
        user = 'admin'
    response.generic_patterns = ['html']
    headers = getHeaders(user)

    controlPanelData = getControlPanelData(user,string)
    return dict(headers = headers, controlPanelData = controlPanelData, user = user)


def getControlPanelData(user, string):
    ret = []
    if string:
        query = ( db.Punto.nombre.like(string + '%') )
    else:
        query = ( db.Punto.id > 0 )
    # print "getControlPanelData: %s" % query
    if user == 'admin':
        formularios = db(
            (db.MuestreoUsuario.usuario==db.auth_user.id) &
            (db.MuestreoUsuario.muestreo==db.Muestreo.id) &
            (db.Muestreo.punto==db.Punto.id) &
            (query)
        ).select()
        for form in formularios:
            username = form.auth_user.username
            hasReport = db(db.MuestreoTipoReporte.muestreo == form.Muestreo.id).select()
            if hasReport != None:
                cell = {
                    'nombre':form.Punto.nombre,
                    'anio':form.Muestreo.anioMuestreo,
                    'porcentaje':completedPercentage(form.MuestreoUsuario.muestreo),
                    'username':username,
                    'link':"/%s/default/datosGenerales/?m=%s" % (request.application, form.Muestreo.id)
                }
            else:
                cell = {
                    'nombre':form.Punto.nombre,
                    'anio':form.Muestreo.anioMuestreo,
                    'porcentaje':completedPercentage(form.MuestreoUsuario.muestreo),
                    'link':"/%s/default/muestreoTipoReporte/?m=%s" % (request.application, form.Muestreo.id),
                    'username':username
                }
            ret.append(cell)
    else:
        formularios = db(
            (db.MuestreoUsuario.usuario==auth.user_id) &
            (db.MuestreoUsuario.muestreo==db.Muestreo.id) &
            (db.Muestreo.punto==db.Punto.id) &
            (query)
        ).select()
        for form in formularios:
            hasReport = db(
                (db.MuestreoTipoReporte.muestreo == form.Muestreo.id)
            ).select()
            if hasReport != None:
                cell = {
                    'nombre':form.Punto.nombre,
                    'anio':form.Muestreo.anioMuestreo,
                    'porcentaje':completedPercentage(form.MuestreoUsuario.muestreo),
                    'link':"/%s/default/datosGenerales/?m=%s" % (request.application, form.Muestreo.id)
                }
            else:
                cell = {
                    'nombre':form.Punto.nombre,
                    'anio':form.Muestreo.anioMuestreo,
                    'porcentaje':completedPercentage(form.MuestreoUsuario.muestreo),
                    'link':"/%s/default/muestreoTipoReporte/?m=%s" %(request.application, form.Muestreo.id)
                }
            ret.append(cell)
    return ret

def getHeaders(user):
    colNames = []
    if user == 'admin':
        colNames = [
            'Nombre Muestreo',
            'Año',
            'Realizado%',
            'Asignado a',
            'Ver Muestreo'
        ]
    else:
        colNames = [
            'Nombre Muestreo',
            'Año',
            'Realizado?',
            'Ver Muestreo'
        ]
    return colNames


def fail():
    """
    Página que cambia el diseño de la página de error y muestra una vista amistosa
    """
    session.show_title = False
    return dict()

def about():
    """
    Despliega información acerca de la empresa
    """
    session.show_title = False
    return dict()

@auth.requires_membership('administrador')
def loadTypes():
    """
    Página donde se pueden ingresar los datos iniciales que contendrá la aplicación referente a los tipos
    """
    session.show_title = False
    form = FORM(
            DIV(_id="file-uploader"),
            INPUT (_type='submit',_value='Continuar')
        )
    if form.validate():
        redirect(URL('index'))
    else:
        return dict(form=form)


@auth.requires_membership('administrador')
def loadSQLTypes():
    """
    Método que ejecuta los INSERTS en la base de datos
    """
    import os
    filename = 'sqltypes.sql'
    ret = {}
    try:
        f = open( os.path.join(request.folder, 'sql', filename) )
        sqlLines = f.readlines()
        db.commit()
        cl=1
        for sql in sqlLines:
            # print "%i: %s" % (cl,sql)
            db.executesql(sql)
            cl=cl+1
        ret['resp'] = 'OK'
    except:
        db.rollback()
        ret['resp'] = 'NOK'
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps({'ret': ret})


def panelDeControl():
    """
    Página incluída en las tabs del index que muestra el panel de control
    """
    session.menuL_enabled = False
    user = 'user'
    if auth.user != None and auth.has_membership('administrador', auth.user.id):
        user = 'admin'
    return dict(op=user)

def estadisticas():
    """
    Página incluída en las tabs del index que muestra las estadísticas
    """
    session.menuL_enabled = False
    divEstadisticas = ""
    divNoAsignados = ""
    if auth.user != None and auth.has_membership('administrador', auth.user.id):
        divEstadisticas = estadisticasAdmin()
        divNoAsignados = DIV(TABLE(_id= "puntosNoAsignados"), DIV(_id="puntosNoAsignadosNavGrid"), _id="divNoAsignados", _style="float:left; margin-right: 5px; margin-bottom: 5px;")
    else:
        divEstadisticas = estadisticasDigitador()
    return dict(divEstadisticas=divEstadisticas, divNoAsignados=divNoAsignados)

def estadisticasAdmin():
    """
    Método que devuelve las estadísticas del administrador
    """
    session.menuL_enabled = False
    totalMuestreos = db(db.Muestreo.id > 0).count()
    completados = 0
    muestreos = db(db.Muestreo.id > 0).select()
    for muestreo in muestreos:
        if checkIfFinished(muestreo):
            completados = completados + 1
    usuariosRegistrados = db(db.auth_user.id == db.auth_membership.user_id)(db.auth_membership.group_id == db.auth_group.id)(db.auth_group.role == "digitador").count()
    dbInfo = dbStats()
    moreInfo = ""
    if dbInfo != {}:
        moreInfo = TR(TD("Última vez que se ha iniciado sesión", _colspan=2, _style="color: white; background-color: #184831; line-height: 26px; font-weight: bold; text-align: left;")), TR(TD("Fecha"), TD(dbInfo['date'])), TR(TD("Hora"), TD(dbInfo['time'])), TR(TD("IP"), TD(dbInfo['ip']))
    return DIV(TABLE(TR(TD("Resumen", _colspan=2, _style="color: white; background-color: #184831; line-height: 26px; font-weight: bold; text-align: left;")),TR(TD("Muestreos Completados"), TD(str(completados) + "/" + str(totalMuestreos))),TR(TD("Usuarios Registrados"), TD(str(usuariosRegistrados))), moreInfo, _class="resumen"), DIV(_style="clear:both;"),_id='resumenDiv')

def estadisticasDigitador():
    """
    Método que devuelve las estadísticas del digitador
    """
    session.menuL_enabled = False
    muestreosCompletados = db(db.MuestreoUsuario.realizado == True)(db.MuestreoUsuario.usuario == auth.user.id).count()
    totalMuestreos = db(db.MuestreoUsuario.usuario == auth.user.id).count()
    dbInfo = dbStats()
    moreInfo = ""
    if dbInfo != {}:
        moreInfo = TR(TD("Último Logeo", _colspan=2, _style="color: white; background-color: #184831; line-height: 26px; font-weight: bold; text-align: left;")), TR(TD("Fecha"), TD(dbInfo['date'])), TR(TD("Hora"), TD(dbInfo['time'])), TR(TD("IP"), TD(dbInfo['ip']))
    return DIV(TABLE(TR(TD("Resumen", _colspan=2, _style="color: white; background-color: #184831; line-height: 26px; font-weight: bold; text-align: left;")),TR(TD("Muestreos Completados"), TD(str(muestreosCompletados) + "/" + str(totalMuestreos))), moreInfo, _class="resumen"), DIV(_style="clear:both;"),_id='resumenDiv')

def puntosSinAsignar():
    """
    Método que retorna el JQGrid con los usuarios que han iniciado sesión
    """
    ret = []
    points = db(db.Muestreo.punto == db.Punto.id).select()
    excludePoints = db(db.MuestreoUsuario.muestreo == db.Muestreo.id)(db.Muestreo.punto == db.Punto.id).select()
    excludeNames = []
    for row in excludePoints:
        excludeNames.append(row.Punto.nombre)
    for row in points:
        if(row.Punto.nombre not in excludeNames):
            cell = {'cell': [row.Punto.nombre, row.Muestreo.anioMuestreo]}
            ret.append(cell)
    page = 1
    if request.get_vars['page']:
        page = int(request.get_vars['page'])
    rows = 10
    if request.get_vars['rows']:
        rows = int(request.get_vars['rows'])
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps({'total':len(ret)/rows, 'page':page, 'records':len(ret), 'rows': ret})

def dbStats():
    eventos = db(db.auth_event.user_id == auth.user.id)(db.auth_event.description == T('User') + ' ' + str(auth.user.id) + ' ' + T('Logged-in')).select(orderby=~db.auth_event.time_stamp, limitby=(0,2))
    lastLogin = {}
    first = True

    for event in eventos:
        if not first:
            timeAndDate = event.time_stamp
            lastLogin['date'] = timeAndDate.strftime("%d/%m/%Y")
            lastLogin['time'] = timeAndDate.strftime("%H:%M:%S")
            lastLogin['ip'] = event.client_ip
        first = False
    return lastLogin

def error():
    """
    Método de Web2Py para mostrar los errores de la aplicación
    """
    return dict()


def loadForm():
    """
    Método que permite cargar las páginas dentro de las tabs
    """
    if request.vars['c']:
        variables = {'c' : request.vars['c'] }
    else:
        variables = ""
    return dict(load=request.vars['f'], variables=variables)


def loggedInUsers():
    """
    Método que alimenta el JQGrid de los usuarios que han iniciado sesión al consultar la base de datos
    """
    query = db.auth_event.description.contains(T('Logged-'))
    events = db(query).select(db.auth_event.user_id, db.auth_event.description,
        orderby=db.auth_event.user_id|db.auth_event.time_stamp)
    users = []
    userString = T('User') + ' ' + str(auth.user.id) + ' ' + T('Logged-in')
    for i in range(len(events)):
        last_event = ((i == len(events) - 1) or
                       events[i+1].user_id != events[i].user_id)
        if last_event and  userString == events[i].description:
            users.append(events[i].user_id)
    return users


def firstRun():
    """
    Página que se presenta la primera vez que se ejecuta la aplicación
    """
    session.menuL_enabled = False
    hasUser = db(db.auth_user.id > 0).select().first()

    #RFPV
    logging.debug("firstRun - request: %s\n" % request)
    logging.debug("firstRun - session: %s\n" % session)


    if hasUser==None:

        welcomeMsg = H2(T('Bienvenido al Inventario Forestal Nacional'))
        body = P("""Este es la primera vez que se utiliza el programa, por favor introduzca sus datos.
            Este usuario será el administrador y encargado de enviar los datos de los formularios a la DGF.
            También puede agregar usuarios, visualizar los formularios a completar y distribuirlos a los usuarios que desee.
            """)
        form = SQLFORM(db.auth_user, labels={'username':'Usuario', 'first_name':'Nombre', 'last_name':'Apellido', 'email':'Correo electrónico', 'password':'Contraseña'}, submit_button='Registrar administrador')
        confirmP = TR(TD(LABEL('Confirmar Contraseña:'), _class="w2p_fl"), TD(INPUT(_type='password', _name='confirmP', _id='confirmP'), _class="w2p_fw", _id="confirmP_row"), TD("", _class="w2p_fc"))
        form[0].insert(5, confirmP)
        # RFPV
        if form.accepts(request.vars, session):
        # if form.process().accepted:
            auth.add_group('digitador', 'Este rol contiene las personas que ingresan datos de formularios')
            auth.add_group('administrador', 'Rol del administrador')
            adminId = db(db.auth_user.id > 0).select().first().id
            adminGroupId = auth.id_group(role='administrador')
            digitadorGroupId = auth.id_group(role='digitador')
            db.auth_membership.insert(group_id = adminGroupId, user_id = adminId)
            db.auth_membership.insert(group_id = digitadorGroupId, user_id = adminId)
            redirect(URL('user/login'))
        elif form.errors:
            response.flash = T("There are errors. Please correct them")
        else:
            pass
        return dict(welcomeMsg=welcomeMsg, body=body, form=form, request=request, session=session)
    else:
        redirect(URL("index"))

@auth.requires_membership('administrador')
def muestreoUsuarios():
    """
    Página que permite asignar muestreos a los usuarios del sistema
    """
    session.menuL_enabled = False
    session.show_title = False
    opts = []
    optsAsign = []
    optsUsers = []
    rows = db(
        (db.Muestreo.punto == db.Punto.id)
    ).select()
    excludeRows = db(
        (db.MuestreoUsuario.muestreo == db.Muestreo.id) &
        (db.Muestreo.punto == db.Punto.id)
    ).select()
    excludeNames = []
    for row in excludeRows:
        excludeNames.append(row.Punto.nombre)
    for row in rows:
        if (row.Punto.nombre not in excludeNames):
            aux = "%s - %d" % (row.Punto.nombre,row.Muestreo.anioMuestreo)
            opts.append( OPTION(aux, _value=row.Muestreo.id) )
    users = db(db.auth_user.id > 0).select()
    firstId = 0
    for user in users:
        if firstId == 0:
            firstId = user.id
        optsUsers.append(OPTION(user.username, _value=user.id))
    asignados = db(
        (db.MuestreoUsuario.usuario == firstId) &
        (db.Muestreo.punto == db.Punto.id) &
        (db.MuestreoUsuario.muestreo == db.Muestreo.id)
    ).select()
    # print asignados
    for asign in asignados:
        # if completedPercentage(asign.Muestreo.id) == 0:
        aux = "%s - %d" % (asign.Punto.nombre, asign.Muestreo.anioMuestreo)
        optsAsign.append(OPTION(aux, _value=asign.Muestreo.id))
    userSelect = TABLE(
        TR(
            TD(LABEL("Usuario:"),
               _class="w2p_fl"
            ),
            TD(
                SELECT(optsUsers, _name='user', _id='user'),
                _class="w2p_fw"
            ),
            TD(_id='progressBar')
        )
    )
    form = FORM(userSelect,
                TABLE(
                        TR(
                            TD(LABEL("Formularios sin asignar:", _class = "table-th")),
                            TD(""),
                            TD(LABEL("Formularios asignados:", _class = "table-th"))),
                        TR(
                            TD(
                                DIV(
                                    SELECT(
                                        opts,
                                        _name='todos',
                                        _id='todos',
                                        _multiple= "multiple",
                                        _size = "50"
                                    ),
                                    _id="formTodos",
                                    _style = "display: inline-block; margin-top: -10px;"
                                )
                            ),
                            TD(
                                DIV(
                                    DIV(
                                        INPUT(_type = "button", _name = "selectAll", _value = ">>")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "selectOneOrMultiple", _value = "=>")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "deselectOneOrMultiple", _value = "<=")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "deselectAll", _value = "<<")
                                    ),
                                    _id="buttons",
                                    _style="float:left; margin-top: 10px;"
                                )
                            ),
                            TD(
                                DIV(
                                    SELECT(
                                        optsAsign,
                                        _name='asignados',
                                        _id='asignados',
                                        _multiple= "multiple",
                                        _size = "50"
                                    ),
                                    _id="formAsignados",
                                    _style = "display: inline-block; margin-top: -10px;"
                                )
                            )
                        ),
                        TR(
                            TD(),
                            TD(),
                            TD(
                                DIV(
                                    INPUT(_type="button", _value="Guardar asignaciones", _id="guardar", _style="float: right; margin-top: 10px;"),_id="saveButton", _style="clear:both;")
                                )
                        )
                    )
                )
    return dict(form=form)


def saveMuestreoUsuarios():
    """
    Método que utilizando ajax guarda los muestreos asignados al usuario seleccionado
    """
    if request.get_vars['user'] and request.get_vars['asign'] and request.get_vars['todos']:
        userId = int(request.get_vars['user'])
        if request.get_vars['asign'] != "0":
            muestreos = request.get_vars['asign'].split(",")
        else:
            muestreos = []
        if request.get_vars['todos'] != "0":
            sacarM = request.get_vars['todos'].split(",")
        else:
            sacarM = []
        for muestreo in muestreos:
            row = db(db.MuestreoUsuario.usuario == userId)(db.MuestreoUsuario.muestreo == int(muestreo)).select().first()
            if row == None:
                db.MuestreoUsuario.insert(muestreo=int(muestreo), usuario=userId, realizado=False)
                accionAsignar = db(db.TipoAccion.tipo == "Muestreo asignado").select().first().id
                import datetime
                db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = userId, accion = accionAsignar, muestreo = muestreo)
        for sacar in sacarM:
            row = db(db.MuestreoUsuario.usuario == userId)(db.MuestreoUsuario.muestreo == int(sacar)).select().first()
            if row != None:
                row.delete_record()
                accionAsignar = db(db.TipoAccion.tipo == "Muestreo reasignado").select().first().id
                import datetime
                db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = userId, accion = accionAsignar, muestreo = sacar)

def asignedFormsUser():
    """
    Devuelve los puntos muestrales asignados del usuario seleccionado
    """
    optsAsign = ""
    if request.get_vars['user']:
        idUser = int(request.get_vars['user'])
        asignados = db(db.MuestreoUsuario.usuario == idUser)(db.Muestreo.punto == db.Punto.id)(db.MuestreoUsuario.muestreo == db.Muestreo.id).select()
        for asign in asignados:
            if completedPercentage(asign.Muestreo.id) == 0:
                aux = "%s - %d" % (asign.Punto.nombre, asign.Muestreo.anioMuestreo)
                optsAsign += "<option value=\""+str(asign.Muestreo.id)+"\">"+aux+"</option>"
    return optsAsign

def remainingPoints():
    """
    Devuelve los puntos muestrales sin asignar
    """
    opts = ""
    rows = db(db.Muestreo.punto == db.Punto.id).select()
    excludeRows = db(db.MuestreoUsuario.muestreo == db.Muestreo.id)(db.Muestreo.punto == db.Punto.id).select()
    excludeNames = []
    for row in excludeRows:
        excludeNames.append(row.Punto.nombre)
    for row in rows:
        if(row.Punto.nombre not in excludeNames):
            aux = "%s - %d" % (row.Punto.nombre,row.Muestreo.anioMuestreo)
            opts+= "<option value=\""+str(row.Muestreo.id)+"\">"+aux+"</option>"
    return opts



def __hasPermission(muestreoId):
    """
    Método que verifica que el usuario que ha iniciado sesión puede acceder al muestreo
    """
    existsMuestreo = db(db.MuestreoUsuario.muestreo==muestreoId).select().first()
    muestreo = db(db.MuestreoUsuario.usuario==auth.user_id)(db.MuestreoUsuario.muestreo==muestreoId).select().first()
    return existsMuestreo != None and (muestreo != None or auth.has_membership('administrador', auth.user.id))

def __hasGeneralData(muestreoId):
    """
    Método que verifica que se han ingresado datos generales al muestreo
    """
    rows = db(db.DatosGenerales.muestreo==muestreoId).select().first()
    return rows != None


@auth.requires_membership('digitador')
def datosGenerales():
    """
    Página que modela el ingreso de los datos generales de un punto muestral
    """
    # print "datosGenerales.request.get_vars: %s" % request.get_vars

    if request.get_vars['m'] and __hasPermission(request.get_vars['m']):

        checkNewRepSel()

        rowReport = db(
            (db.MuestreoTipoReporte.muestreo == session.muestreoId) &
            (db.MuestreoTipoReporte.tipo == db.TipoReporte.id)
        ).select().first()
        if rowReport == None:
            redirect(URL('muestreoTipoReporte', vars=dict(m=session.muestreoId)))
        elif rowReport != None and rowReport.TipoReporte.id == CON_INFORMACION:
            recordId = db(db.DatosGenerales.muestreo==session.muestreoId).select().first()
            opts = []
            plantacion = ""
            cambio = ""
            if recordId != None:
                rows = db(db.TipoSubBosque.tipo == recordId.tipoDeBosque).select()
                idSubTipoSelected = recordId.subbosque
                plantacion = esPlantacion(recordId.tipoDeBosque)
                session.plant = plantacion
                recordId = recordId.id
                for row in rows:
                    if row.id == idSubTipoSelected:
                        opts.append(OPTION(row.nombre, _value=row.id, _selected='selected'))
                    else:
                        opts.append(OPTION(row.nombre, _value=row.id))

            form = SQLFORM(
                db.DatosGenerales,
                record=recordId,
                showid = False,
                fields=['tipoDeBosque', 'fecha', 'facilidadProgresion', 'departamento', 'propietario', 'predio'],
                submit_button='Guardar',
                _autocomplete="off"
            )
            subbosque = TR(
                TD(LABEL('Tipo de Subbosque:'), _class="w2p_fl"),
                TD(SELECT(opts, _name='subbosque', _id='subbosque'),_class="w2p_fw"),
                TD("Subtipo del bosque seleccionado", _class="w2p_fc")
            )
            form[0].insert(1, subbosque)
            form.vars.muestreo = session.muestreoId
            if request.post_vars['subbosque']:
                form.vars.subbosque = request.post_vars['subbosque']
            if form.validate(keepvalues=True):
                plantacion = esPlantacion(int(form.vars.tipoDeBosque))
                session.plant = plantacion
                recordId = form.vars.id
                row = db(db.DatosGenerales.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.DatosGenerales.insert(**dict(form.vars))
                    response.flash = T("Successfully saved")
                    session.muestreoPorcentaje = returnPercentage()
                cambio = "True"
                redirect(URL("datosGenerales", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T('Fill in the general data')
            return dict(form=form, plant=plantacion, muestreo = session.muestreoId, cambio = cambio, menuL = sideMenu(), selected=1)
        else:
            redirect(URL('muestreoTipoReporte', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def subSelectData():
    """
    Retorna las opciones de sub bosque dependiendo del tipo de bosque seleccionado
    """
    if request.get_vars['id'] and request.get_vars['t']:
        idParent = int(request.get_vars['id'])
        if str(request.get_vars['t']) == "TipoSubBosque":
            rows = db(db.TipoSubBosque.tipo == idParent).select()
        else:
            rows = None
        ret = dict()
        for row in rows:
            ret[row.id] = row.nombre
        import gluon.contrib.simplejson
        return gluon.contrib.simplejson.dumps(ret)
    else:
        pass

def subSelectDataPlantacion():
    """
    Retorna las opciones de sub especie dependiendo del género seleccionado
    """
    if request.get_vars['id']:
        idParent = int(request.get_vars['id'])
        rows = db(db.TipoEspecie.genero == idParent).select()
        ret = dict()
        for row in rows:
            ret[row.id] = row.especie
        import gluon.contrib.simplejson
        return gluon.contrib.simplejson.dumps(ret)
    else:
        pass

def esPlantacion(idTipoBosque):
    """
    Retorna si el bosque es una plantación
    """
    idPlant = db(db.TipoBosque.tipo=='Plantación').select().first().id
    return idPlant == idTipoBosque


def sideMenu():
    """
    Método que construye el menú lateral
    """
    rowReport = db(
        (db.MuestreoTipoReporte.muestreo == session.muestreoId) &
        (db.MuestreoTipoReporte.tipo == db.TipoReporte.id)
    ).select().first()
    if rowReport != None:
        if rowReport.TipoReporte.id == BOSQUE_CORTADO or \
            rowReport.TipoReporte.id == NO_BOSQUE or \
            rowReport.TipoReporte.id == NO_INGRESO:
            return {
                0:['muestreoTipoReporte', "Estado Punto Muestral"]
            }
        else:
            # session.muestreoPorcentaje = returnPercentage()
            rowDG = db(
                (db.DatosGenerales.muestreo == session.muestreoId)
            ).select().first()
            if rowDG != None:
                tabs = {
                    0:['muestreoTipoReporte', "Estado Punto Muestral"],
                    1:['datosGenerales', "Datos Generales"],
                    2:['distancias', "Distancias"],
                    3:['fotos', "Fotos"],
                    4:['coordenadasParcela', "Coordenadas Parcela"],
                    6:['equipoTrabajo', "Equipo Trabajo"],
                    7:['observaciones', "Observaciones"],
                    8:['agua', "Agua"],
                    9:['fauna', "Fauna"],
                    10:['relieve', "Relieve"],
                    11:['suelo',"Suelo"],
                    12:['coberturaVegetal', "Cobertura Vegetal"],
                    14:['flora', "Flora"],
                    16:['problemasAmbientales', "Problemas Ambientales"],
                    18:['fuego', "Fuego"]
                }
                tabsPlant = {
                    5:['plantacion', "Plantación"],
                    13:['productosNoMadereros', "Productos No Madereros"],
                    17:['ForestacionMantenimientoEstructura', "Forestación"],
                    20:['parcelaBosquePlantado' ,"Parcela circular (6 m radio)", 1],
                    21:['parcelaBosquePlantado' ,"Parcela circular (10 m radio)", 2],
                    22:['parcelaBosquePlantado' ,"Parcela circular (14 m radio)", 3],
                    23:['parcelaBosquePlantado' ,"Parcela circular (18 m radio)", 4]
                }
                tabsNativo = {
                    13:['productosNoMadereros', "Productos No Madereros"],
                    19:['especiesInvasoras', "Especies Invasoras"],
                    25:['parcelaBosqueNatural', "Parcela (20 x 10 m)"]
                }
                sideMenu = tabs
                if session.plant == True:
                    session.GeneroPlantado = generoPlantacion(session.muestreoId)
                    if session.GeneroPlantado:
                        if session.GeneroPlantado == "Eucalyptus":
                            tabsPlant[24] = ['SanidadEucalipto', "Sanidad Eucalyptus"]
                        elif session.GeneroPlantado == "Pinus":
                            tabsPlant[24] = ['SanidadPino', "Sanidad Pinus"]
                    sideMenu = dict(tabs.items() + tabsPlant.items())
                else:
                    sideMenu = dict(tabs.items() + tabsNativo.items())
            else:
                sideMenu = {
                    0:['muestreoTipoReporte', "Estado Punto Muestral"],
                    1:['datosGenerales', "Datos Generales"]
                }
            return sideMenu
    else:
        return {
            0:['muestreoTipoReporte', "Estado Punto Muestral"]
        }


def checkNewRepSel():
    """Usuario comenzo a ver nuevo reporte
    """
    if (session.muestreoId==request.get_vars['m']):
        pass
    else:
        session.muestreoId = request.get_vars['m']
        session.menuL_enabled = True
        session.muestreoNombre = sampleName()
        session.muestreoPorcentaje = returnPercentage()

def muestreoTipoReporte():
    """
    Página que permite discriminar el estado de la parcela y si se pudo recabar información
    """
    # print "request.get_vars: %s" % request.get_vars

    if __hasPermission(request.get_vars['m']):
        checkNewRepSel()
        rowReport = db(
            (db.MuestreoTipoReporte.muestreo == request.get_vars['m']) &
            (db.MuestreoTipoReporte.tipo == db.TipoReporte.id)
        ).select().first()

        # print "rowReport: %s" % rowReport

        val = "infoRelevada"
        comentario = ""
        if rowReport != None:
            if rowReport.TipoReporte.id == NO_BOSQUE:
                val = "ausenciaBosque"
            elif rowReport.TipoReporte.id == BOSQUE_CORTADO:
                val = "bosqueCortado"
            elif rowReport.TipoReporte.id == NO_INGRESO:
                val = "noSePuedeIngresar"
            else:
                val = "infoRelevada"
            comentario = rowReport.MuestreoTipoReporte.comentario
        else:
            pass

        form = FORM(
            INPUT(_id = "iInfoRelevada", _type="radio", _name="tipoReporte", _value="infoRelevada", value=val, _style="display:none;"),
            INPUT(_id = "iAusenciaBosque", _type="radio", _name="tipoReporte", _value="ausenciaBosque", value=val, _style="display:none;"),
            INPUT(_id = "iBosqueCortado", _type="radio", _name="tipoReporte", _value="bosqueCortado", value=val, _style="display:none;"),
            INPUT(_id = "iNoSePuedeIngresar", _type="radio", _name="tipoReporte", _value="noSePuedeIngresar", value=val, _style="display:none;"),
            DIV(
                SPAN(
                    TABLE(
                        TR(
                            TD(LABEL('Ausencia de Bosque'),_colspan=4,_style="border:solid 1px;text-align: left;"),
                            TD('',_colspan=2),
                            TD(LABEL('Bosque cortado',_style="text-align:right;"),_colspan=4,_style="border:solid 1px;text-align:right;"),
                        ),
                        TR(
                            TD('',_colspan=1,_style="width:200px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 1px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 1px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:25px;border-right:solid 0px;"),
                            TD('',_colspan=1,_style="width:200px;border-right:solid 0px;"),
                            _height="20px"
                        ),
                        TR(
                            TD('',_style="width:200px;"),
                            TD(
                                DIV(
                                    BUTTON(
                                        "Si",
                                        _id="bInfoRelevada",
                                        _class="btn toggle-btn",
                                        _type= "button",
                                    ),
                                    BUTTON(
                                        "Si",
                                        _id="bAusenciaBosque",
                                        _class="btn toggle-btn",
                                        _type= "button",
                                    ),
                                    BUTTON(
                                        "Si",
                                        _id="bBosqueCortado",
                                        _class="btn toggle-btn",
                                        _type= "button",
                                    ),
                                    BUTTON(
                                        "Si",
                                        _id="bNoSePuedeIngresar",
                                        _class="btn toggle-btn",
                                        _type= "button",
                                    ),
                                    _class="btn-group",
                                    **{'_data-toggle':'buttons-radio'}

                                ),
                            _colspan=8,
                            _style="border:solid 0px;width:200px;"
                            ),
                            TD('',_width="200px"),
                        ),
                        TR(
                            TD('',_colspan=2,_style="border-right:solid 1px;"),
                            TD('',_colspan=6,_style="border-right:solid 1px;"),
                            TD('',_colspan=2),
                            _height="20px"
                        ),
                        TR(
                            TD(LABEL('Con información relevada'),_colspan=2,_style="border:solid 1px;text-align:left;"),
                            TD('',_colspan=6),
                            TD(LABEL('No se puede ingresar',_style="text-align:right;"),_colspan=2,_style="border:solid 1px;text-align:right;"),
                        ),
                        _border="0",
                        _cellspacing="0",
                        _cellpadding="0"
                    ),
                    TABLE(
                        TR(
                            TD(LABEL("Comentario:"), _class="w2p_fl"),
                            TD(TEXTAREA(_id="comentario", _name="comentario", value=comentario), _class="w2p_fw")
                        ),
                        TR(
                            TD(""),
                            TD(INPUT(_type="submit", _value="Guardar"), _class="w2p_fw"),
                            _id="submit_record__row"
                        )
                    )
                ),
                _class="btn-group",
                **{'_data-toggle':'buttons-radio'}
            )
        )

        if request.post_vars['tipoReporte']:
            tipoRep = "Con informacion relevada"
            if request.post_vars['tipoReporte'] == "ausenciaBosque":
                tipoRep = "Ausencia de Bosque"
            elif request.post_vars['tipoReporte'] == "bosqueCortado":
                tipoRep = "Bosque cortado"
            elif request.post_vars['tipoReporte'] == "noSePuedeIngresar":
                tipoRep = "No se puede ingresar"
            idTipoReporte = db(db.TipoReporte.tipo == tipoRep).select().first()
            if idTipoReporte != None:
                form.vars.tipoRep = idTipoReporte.id
            else:
                form.vars.tipoRep = "0"

        if form.validate(keepvalues=True):
            rep = db(db.MuestreoTipoReporte.muestreo == session.muestreoId).select().first()
            if rep != None:
                rep.update_record(tipo=form.vars.tipoRep, comentario=form.vars.comentario)
                response.flash = T("Successfully modified")
            else:
                db.MuestreoTipoReporte.insert(muestreo=session.muestreoId, tipo=form.vars.tipoRep, comentario=form.vars.comentario)
                response.flash = T("Successfully saved")
            session.muestreoPorcentaje = returnPercentage()
            if tipoRep == "Con informacion relevada":
                redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
        elif form.errors:
            response.flash = T("There are errors. Please correct them")
        else:
            if rowReport != None:
                #print "%s" % request.post_vars
                response.flash = T("Modify the data")
            else:
                response.flash = T('Fill in the status of the parcel')
        return dict(form=form, menuL = sideMenu(), selected=0)
    else:
        redirect(URL('index'))


@auth.requires_membership('digitador')
def distancias():
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        trackName = ''
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.Distancias.muestreo==session.muestreoId).select().first()
            if recordId != None:
                if recordId.track != '':
                    trackName = recordId.track
                recordId = recordId.id

            form = SQLFORM(
                db.Distancias,
                record=recordId,
                showid = False,
                fields=[
                    'carreteraCaminoVecinal',
                    'caminoVecinalCaminoAcceso',
                    'caminoAccesoPuntoGPS',
                    'puntoGPSCentroParcela',
                    'rumboCaminoCentroParcela'
                ],
                submit_button=T('Save'),
                _cellspacing=0,
                _cellpadding=0,
                _border=0
            )
            if trackName != '':
                info = TR(
                    TD(
                        "",
                        _style="height: 35px;"
                    ),
                    TD(
                        DIV(
                            A("Track", _href=URL(f='link_handler_track', vars=dict(id=recordId))),
                            A("Obtener Información del track",_style="margin-left: 10px;", _href='javascript:;', _id='info'),
                            A("Eliminar",_style="margin-left: 10px;", _href='javascript:;',_id='eraseLink'),
                            _id='actions'
                        )
                    ),
                    _class="w2p_fw"
                )
                sampleId = DIV(
                    recordId,
                    _style='display: none;',
                    _id='muestreoId'
                )
                form[0].insert(5, info)
                form[0].insert(8, sampleId)
            else:
                pass

            inputTrack = DIV(
                    INPUT(
                        _type='text',
                        _name='trackFileName',
                        _value=trackName,
                        _style='display: none;'
                    ),
                    _id='trackFileName'
            )

            uploader = TR(
                    TD(
                        DIV(LABEL('Track (.gpx):')),
                        _class="w2p_fl"
                    ),
                    TD(
                        DIV(_id="fineUploader"),
                        _class="w2p_fw"
                    )
            )

            fakeSave = TR(
                    TD(
                        BUTTON(
                            T("Save"),
                            _id="fakeSave",
                            _style="width:200px;"
                        ),
                        _class="w2p_fw",
                        _colspan=2,
                        _style="text-align:right;"
                    )
            )

            form[0].insert(7, inputTrack)
            form[0].insert(5, uploader)
            form[0].insert(9, fakeSave)

            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.Distancias.muestreo==session.muestreoId).select().first()
                trackName = ''
                if request.post_vars['trackFileName']:
                    trackName = request.post_vars['trackFileName']
                if row != None:
                    if trackName == '':
                        trackName = row.track
                    print "Distancias.update.trackName: %s" % trackName
                    row.update_record(muestreo=form.vars.muestreo, carreteraCaminoVecinal = form.vars.carreteraCaminoVecinal, caminoVecinalCaminoAcceso=form.vars.caminoVecinalCaminoAcceso,caminoAccesoPuntoGPS=form.vars.caminoAccesoPuntoGPS, puntoGPSCentroParcela=form.vars.puntoGPSCentroParcela, rumboCaminoCentroParcela=form.vars.rumboCaminoCentroParcela, track=trackName)
                    response.flash = T("Successfully modified")
                else:
                    print "Distancias.insert.trackName: %s" % trackName
                    db.Distancias.insert(
                        muestreo = form.vars.muestreo,
                        carreteraCaminoVecinal = form.vars.carreteraCaminoVecinal,
                        caminoVecinalCaminoAcceso = form.vars.caminoVecinalCaminoAcceso,
                        caminoAccesoPuntoGPS = form.vars.caminoAccesoPuntoGPS,
                        puntoGPSCentroParcela = form.vars.puntoGPSCentroParcela,
                        rumboCaminoCentroParcela = form.vars.rumboCaminoCentroParcela,
                        track = trackName
                    )
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("distancias", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T('Fill in the data of distances')
            return dict(form=form, menuL = sideMenu(), selected=2)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def saveTrack():
    """
    Método que guarda el archivo del Track en la carpeta uploads para su posterior análisis
    """
    import qqfileuploader as fu
    allowedExtension = [".gpx"]
    sizeLimit = 6144000
    uploader = fu.qqFileUploader(request, allowedExtension, sizeLimit)
    return uploader.handleUpload()


def link_handler_track():
    """
    Método que devuelve el archivo del Track para que sea verificado
    """
    if request.vars.id:
        import os
        distRow = db(db.Distancias.id == request.vars.id).select().first()
        filePath = os.path.join(request.folder, "uploads","gpx", distRow.track)
        print filePath
        response.headers['Content-Disposition']='attachment; filename=%s' % distRow.track
        return response.stream(filePath, chunk_size=64*1024)


def eraseTrack():
    """
    Método que elimina el Track del muestreo seleccionado
    """
    if request.vars.id:
        distRow = db(db.Distancias.id == request.vars.id).select().first()
        distRow.update_record(track='')


def parseTrack():
    """
    Método que verifica la validez del Track y devuelve información del mismo
    """
    if request.get_vars['fileName']:
        fileName = request.get_vars['fileName']
        #Director gpxpy is in appfolder/modules
        import gpxpy
        import os

        gpx_file = open( os.path.join(request.folder, "uploads", "gpx", fileName), 'r')
        gpx = gpxpy.parse(gpx_file)

        times = {}
        boundings = {}
        names = {}

        for i in range(0, len(gpx.tracks)):
            try:
                times[i] = gpx.tracks[i].get_time_bounds()
            except:
                times[i] = ''
            try:
                boundings[i] = gpx.tracks[i].get_bounds()
            except:
                boundings[i] = ''
            try:
                names[i] = gpx.tracks[i].name
            except:
                names[i] = ''

        gpxRead = u"<p>El archivo es válido!</p>"
        gpxRead += "</hr>"
        for j in boundings.keys():
            if names[j] != '':
                gpxRead +=u"<p>El track de nombre: %s</>" % names[j]
            if times[j].start_time != None and times[j].end_time != None:
                gpxRead += u"<p>Se realizó desde %d/%d/%d hasta %d/%d/%d</p>" % (times[j].start_time.day, times[j].start_time.month, times[j].start_time.year, times[j].end_time.day, times[j].end_time.month, times[j].end_time.year)
            if boundings[j] != '':
                gpxRead += u"<p>El bounding box es: (%f,%f,%f,%f)</p>" % (boundings[j].min_latitude, boundings[j].max_latitude, boundings[j].min_longitude, boundings[j].max_longitude)
            gpxRead += "</hr>"
        return gpxRead


@auth.requires_membership('digitador')
def coordenadasParcela():
    """
    Página que permite el ingreso de datos de las coordenadas del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.CoordenadasParcela.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.CoordenadasParcela, record=recordId, showid = False, fields=['sur', 'oeste', 'altitud'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.CoordenadasParcela.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.CoordenadasParcela.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("coordenadasParcela", vars=dict(m=session.muestreoId)))
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of the coordinates of the parcel")
            return dict(form=form, menuL = sideMenu(), selected=4)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

@auth.requires_membership('digitador')
def plantacion():
    """
    Página que permite el ingreso de datos sobre los detalles de la plantación del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            radioVal = 'T'
            checked = ''
            disabled = 'disabled'
            valCantF = ''
            valDistS = ''
            valDens = ''
            recordId = db(db.Plantacion.muestreo==session.muestreoId).select().first()
            if recordId != None:
                if not recordId.parcelaRegular:
                    radioVal = 'F'
                    checked = ''
                    disabled = ''
                    valCantF = recordId.cantidadFilas
                    valDistS = recordId.distanciaSilvopastoreo
                    valX = 100 / recordId.distanciaEntreFila
                    valY = 100 / (valDistS + recordId.distanciaFila * (valCantF - 1))
                    valDens = valX * valCantF * valY
                else:
                    valDens = 10000 / (recordId.distanciaFila * recordId.distanciaEntreFila)
                    checked = 'checked'
                recordId = recordId.id
            form = SQLFORM(db.Plantacion, record=recordId, showid = False, fields=['genero','especie','rangoEdad','raleo','tienePoda','alturaPoda','parcelaRegular','distanciaFila','distanciaEntreFila','adaptacionEspecie','regimen','estadoGeneral'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            poda = TR(
                TD(LABEL("Tiene Poda:"), _class="w2p_fl"),
                TD(
                    DIV(
                        BUTTON("Si", _id="poda-Si", _class="toggle-btn", _type= "button", _onclick="changePodaRadio(1);"),
                        BUTTON("No", _id="poda-No", _class="toggle-btn", _type= "button", _onclick="changePodaRadio(0);"),
                        _id="toggle-button-div-poda",
                        _class="btn-group"
                    )
                )
            )
            radioBParcela = TR(
                            TD(LABEL("Parcela Regular:"), _class="w2p_fl"),
                            TD(DIV(BUTTON("Si", _id="parcelaR-Si", _class="toggle-btn", _type= "button", _onclick="changeRadio(1);"),BUTTON("No", _id="parcelaR-No", _class="toggle-btn", _type= "button", _onclick="changeRadio(0);"),_id="toggle-button-div-parcelaR", _class="btn-group"))
                            )
            cantFilas = TR(TD(LABEL('Cantidad de filas:'), _class="w2p_fl"), TD(INPUT(_name='cantFilas', _id='cantFilas', _class="integer", _value=valCantF), _class="w2p_fw"), TD("Cantidad de filas de árboles agrupados", _class="w2p_fc"), _class="irregular " + disabled)
            distSilvo = TR(TD(LABEL('Distancia Silvopastoreo (m):'), _class="w2p_fl"), TD(INPUT(_name='distSilvo', _id='distSilvo',  _class="double", _value=valDistS), _class="w2p_fw"), TD("Distancia en metros de silvopastoreo", _class="w2p_fc"), _class="irregular " + disabled)
            densidad = TR(TD(LABEL('Densidad calculada:'), _class="w2p_fl"), TD(INPUT(_name='densidad', _id='densidad',  _class="double", _disabled="disabled", _value=valDens), _class="w2p_fw"))
            form[0].insert(5, poda)
            form[0].insert(7, radioBParcela)
            form[0].insert(11, cantFilas)
            form[0].insert(12, distSilvo)
            form[0].insert(13, densidad)
            if request.post_vars['cantFilas']:
                form.vars.cantidadFilas = int(request.post_vars['cantFilas'])
            if request.post_vars['distSilvo']:
                form.vars.distanciaSilvopastoreo = float(request.post_vars['distSilvo'])
            if form.validate():
                row = db(db.Plantacion.muestreo==session.muestreoId).select().first()
                cantidadFilas = form.vars.cantidadFilas if form.vars.cantidadFilas != None else 0
                distanciaSilvopastoreo = form.vars.distanciaSilvopastoreo if form.vars.distanciaSilvopastoreo != None else 0.0
                if row != None:

                    if form.vars.tienePoda == False:
                        form.vars.alturaPoda = 0.0
                    row.update_record(genero=form.vars.genero,especie=form.vars.especie,rangoEdad=form.vars.rangoEdad,raleo=form.vars.raleo,tienePoda=form.vars.tienePoda,alturaPoda=form.vars.alturaPoda,parcelaRegular=form.vars.parcelaRegular, distanciaFila=form.vars.distanciaFila,distanciaEntreFila=form.vars.distanciaEntreFila,cantidadFilas=cantidadFilas,distanciaSilvopastoreo=distanciaSilvopastoreo,adaptacionEspecie=form.vars.adaptacionEspecie,regimen=form.vars.regimen,estadoGeneral=form.vars.estadoGeneral)
                    response.flash = T("Successfully modified")
                    recordId = row.id
                else:
                    recordId = db.Plantacion.insert(
                        muestreo=form.vars.muestreo,
                        genero=form.vars.genero,
                        especie=form.vars.especie,
                        rangoEdad=form.vars.rangoEdad,
                        raleo=form.vars.raleo,
                        tienePoda=form.vars.tienePoda,
                        alturaPoda=form.vars.alturaPoda,
                        parcelaRegular=form.vars.parcelaRegular,
                        distanciaFila=form.vars.distanciaFila,
                        distanciaEntreFila=form.vars.distanciaEntreFila,
                        cantidadFilas=cantidadFilas,
                        distanciaSilvopastoreo=distanciaSilvopastoreo,
                        adaptacionEspecie=form.vars.adaptacionEspecie,
                        regimen=form.vars.regimen,
                        estadoGeneral=form.vars.estadoGeneral
                    )
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                session.GeneroPlantado = generoPlantacion(session.muestreoId)
                redirect(URL("plantacion", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = form.vars
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of plantation")
            return dict(form=form, menuL = sideMenu(), selected=5)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def generoPlantacion(muestreoId):
    """
    Retorna el género que se encuentra plantado en el punto muestral
    """
    genero = ""
    rowP = db(db.Plantacion.muestreo == muestreoId).select().first()
    if rowP != None:
        rowGenero = db(db.TipoGenero.id == rowP.genero).select().first()
        if rowGenero != None:
            genero = rowGenero.genero
    return genero


@auth.requires_membership('digitador')
def equipoTrabajo():
    """
    Página que permite el ingreso de datos del equipo de trabajo el cual trabajó en el punto muestral
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            form = SQLFORM(db.EquipoTrabajo, showid = False, fields = ['cargo','nombre'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.accepts(request.vars, session):
                session.muestreoPorcentaje = returnPercentage()
                response.flash = T("Successfully saved")
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                response.flash = T("Fill in the data of the working crew")
            return dict(form=form, menuL = sideMenu(), selected=6)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def tableEquipo():
    muestreo = request.get_vars['m']
    headers = ['Cargo', 'Nombre','Acciones']
    rows = []
    equipo = db(db.EquipoTrabajo.muestreo==muestreo).select()
    for r in equipo:
        cell = {'cargo':r.cargo, 'nombre':r.nombre, 'id':r.id}
        rows.append(cell)
    return dict(equipo = [rows,headers])


@auth.requires_membership('digitador')
def observaciones():
    """
    Página que permite el ingreso de observaciones del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.Observaciones.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.Observaciones, record=recordId, showid = False, fields = ['observacion'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.Observaciones.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully modified")
                else:
                    db.Observaciones.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("observaciones", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of observations")
            return dict(form=form, menuL = sideMenu(), selected=7)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def widget(field, value):
    """
    Widget utilizado para incluír los botones de si y no donde se encontraban checkboxes
    """
    activeYes = 'noToggle'
    activeNo = 'active'
    container = DIV()
    wrapper = DIV(
        _class="btn-group",
        _id="toggle-button-div-%s-%s" % (field._tablename,field.name),
        **{'_data-toggle':'buttons-radio'}
        )
    attributes = {'_id': "%s_%s" % (field._tablename, field.name),
        '_class': 'boolean',
        '_value': value,
        'requires': field.requires,
        '_name': '%s' % (field.name),
        '_style':"display:none;",
        '_type': "checkbox"}
    if value:
        activeYes = 'active'
        activeNo = 'snoToggle'
        attributes['_checked'] = 'checked'
    inp = INPUT(**attributes)
    btnYes = BUTTON(
        T("Yes"),
        _class="toggle-btn btn %s" % (activeYes),
        _id="%s_Yes" % (field.name),
        _onclick="document.getElementById('%s_%s').checked = true;" % (field._tablename, field.name),
        _type="button"
    )
    btnNo = BUTTON(
        T("No"),
        _class="toggle-btn btn %s" % (activeNo),
        _id="%s_No" % (field.name),
        _onclick="document.getElementById('%s_%s').checked = false;" % (field._tablename, field.name),
        _type="button"
    )
    wrapper.components.extend( [btnYes, btnNo] )
    container.components.extend( [inp, wrapper] )
    return container


@auth.requires_membership('digitador')
def agua():
    """
    Página que permite el ingreso de datos de agua del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        muestreo = int(request.get_vars['m'])
        agua = tieneAgua(muestreo)
        if True:
            session.menuL_enabled = True
            # load afluents row id
            db.Agua.manejo.widget = widget
            db.Agua.acuacultura.widget = widget
            rowTipoCaudal = db(db.TipoCaudal.id > 0).select()
            for row in rowTipoCaudal:
                if row.tipo == "Río":
                    rowRio = row.id
                elif row.tipo == "Arroyo":
                    rowArroyo = row.id
                elif row.tipo == "Embalse":
                    rowEmbalse = row.id
                elif row.tipo == "Canal de Riego":
                    rowCanal = row.id
                elif row.tipo == "Cañada":
                    rowCanada = row.id
                elif row.tipo == "Represa":
                    rowRepresa = row.id
                elif row.tipo == "Tajamar":
                    rowTajamar = row.id
                elif row.tipo == "Laguna":
                    rowLaguna = row.id
                elif row.tipo == "Lago":
                    rowLago = row.id
                elif row.tipo == "Océano":
                    rowOceano = row.id
            if __hasGeneralData(session.muestreoId):
                recordId = db(db.Agua.muestreo==session.muestreoId).select().first()
                update = "False";
                rio = ""
                arroyo = ""
                canada = ""
                embalse = ""
                canal = ""
                represa = ""
                tajamar = ""
                laguna = ""
                lago = ""
                oceano = ""
                distRio = ""
                distArroyo = ""
                distEmbalse = ""
                distCanal = ""
                distCanada = ""
                distRepresa = ""
                distTajamar = ""
                distLaguna = ""
                distLago = ""
                distOceano = ""
                if recordId != None:
                    recordId = recordId.id
                    names = db(db.NombreAfluentes.muestreo == session.muestreoId).select()
                    for name in names:
                        tipoCaudal = db(db.TipoCaudal.id == name.tipo).select().first().tipo
                        if tipoCaudal == "Río":
                            rio = name.nombre
                            distRio = name.distancia
                        elif tipoCaudal == "Arroyo":
                            arroyo = name.nombre
                            distArroyo = name.distancia
                        elif tipoCaudal == "Embalse":
                            embalse = name.nombre
                            distEmbalse = name.distancia
                        elif tipoCaudal == "Canal de Riego":
                            canal = name.nombre
                            distCanal = name.distancia
                        elif tipoCaudal == "Cañada":
                            canada = name.nombre
                            distCanada = name.distancia
                        elif tipoCaudal == "Represa":
                            represa = name.nombre
                            distRepresa = name.distancia
                        elif tipoCaudal == "Tajamar":
                            tajamar = name.nombre
                            distTajamar = name.distancia
                        elif tipoCaudal == "Laguna":
                            laguna = name.nombre
                            distLaguna = name.distancia
                        elif tipoCaudal == "Lago":
                            lago = name.nombre
                            distLago = name.distancia
                        elif tipoCaudal == "Océano":
                            oceano = name.nombre
                            distOceano = name.distancia
                form = SQLFORM(
                    db.Agua,
                    record=recordId,
                    showid = False,
                    fields = ['tipoCaudal','manejo', 'frecuencia', 'acuacultura', 'gradoContaminacion'],
                    submit_button=T('Save')
                )
                trRio = TR(
                    TD(
                        LABEL("Nombre Río: ", _id="label1"), _class="w2p_fl"
                    ),
                    TD(
                        INPUT(_type="text",_name="Rio", _id="Rio", _value=rio),
                        _id="div"+str(rowRio), _class="w2p_fw"
                    ),
                    _id="row"+str(rowRio),
                    _style = "display: none;"
                )
                trRioDist = TR(
                    TD(
                        LABEL("Distancia al Río (m): "),
                        _class="w2p_fl"
                    ),
                    TD(
                        INPUT(_type="text", _class='double',_name="distRio", _id="distRio", _value=distRio),
                        _id="div"+str(rowRio) +"Dist", _class="w2p_fw"
                    ),
                    _id="row"+str(rowRio) +"Dist",
                    _style = "display: none;"
                )
                trArroyo = TR(
                    TD(
                        LABEL("Nombre Arroyo: ", _id="label2"), _class="w2p_fl"
                    ),
                    TD(
                        INPUT(_type="text",_name="Arroyo", _id="Arroyo", _value=arroyo),
                        _id="div"+str(rowArroyo),
                        _class="w2p_fw"), _id="row"+str(rowArroyo),
                        _style = "display: none;"
                )
                trArroyoDist = TR(TD(LABEL("Distancia al Arroyo (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distArroyo", _id="distArroyo", _value=distArroyo),_id="div"+str(rowArroyo) +"Dist", _class="w2p_fw"), _id="row"+str(rowArroyo) +"Dist", _style = "display: none;")
                trCanada = TR(TD(LABEL("Nombre Cañada: ", _id="label3"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Canada", _id="Canada", _value=canada),_id="div"+str(rowCanada), _class="w2p_fw"), _id="row"+str(rowCanada), _style = "display: none;")
                trCanadaDist = TR(TD(LABEL("Distancia a la Cañada (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distCanada", _id="distCanada", _value=distCanada),_id="div"+str(rowCanada) +"Dist", _class="w2p_fw"), _id="row"+str(rowCanada) +"Dist", _style = "display: none;")
                trEmbalse = TR(TD(LABEL("Nombre Embalse: ", _id="label4"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Embalse", _id="Embalse", _value=embalse),_id="div"+str(rowEmbalse), _class="w2p_fw"), _id="row"+str(rowEmbalse), _style = "display: none;")
                trEmbalseDist = TR(TD(LABEL("Distancia al Embalse (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distEmbalse", _id="distEmbalse", _value=distEmbalse),_id="div"+str(rowEmbalse) +"Dist", _class="w2p_fw"), _id="row"+str(rowEmbalse) +"Dist", _style = "display: none;")
                trCanal = TR(TD(LABEL("Nombre Canal de Riego: ", _id="label5"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Canalderiego", _id="Canalderiego", _value=canal),_id="div"+str(rowCanal), _class="w2p_fw"), _id="row"+str(rowCanal), _style = "display: none;")
                trCanalDist = TR(TD(LABEL("Distancia al Canal de Riego (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distCanalderiego", _id="distCanalderiego", _value=distCanal),_id="div"+str(rowCanal) +"Dist", _class="w2p_fw"), _id="row"+str(rowCanal) +"Dist", _style = "display: none;")
                trRepresa = TR(TD(LABEL("Nombre Represa: ", _id="label6"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Represa", _id="Represa", _value=represa),_id="div"+str(rowRepresa), _class="w2p_fw"), _id="row"+str(rowRepresa), _style = "display: none;")
                trRepresaDist = TR(TD(LABEL("Distancia a la Represa (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distRepresa", _id="distRepresa", _value=distRepresa),_id="div"+str(rowRepresa) +"Dist", _class="w2p_fw"), _id="row"+str(rowRepresa) +"Dist", _style = "display: none;")
                trTajamar = TR(TD(LABEL("Nombre Tajamar: ", _id="label7"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Tajamar", _id="Tajamar", _value=tajamar),_id="div"+str(rowTajamar), _class="w2p_fw"), _id="row"+str(rowTajamar), _style = "display: none;")
                trTajamarDist = TR(TD(LABEL("Distancia al Tajamar (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distTajamar", _id="distTajamar", _value=distTajamar),_id="div"+str(rowTajamar) +"Dist", _class="w2p_fw"), _id="row"+str(rowTajamar) +"Dist", _style = "display: none;")
                trLaguna = TR(TD(LABEL("Nombre Laguna: ", _id="label8"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Laguna", _id="Laguna", _value=laguna),_id="div"+str(rowLaguna), _class="w2p_fw"), _id="row"+str(rowLaguna), _style = "display: none;")
                trLagunaDist = TR(TD(LABEL("Distancia a la Laguna (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distLaguna", _id="distLaguna", _value=distLaguna),_id="div"+str(rowLaguna) +"Dist", _class="w2p_fw"), _id="row"+str(rowLaguna) +"Dist", _style = "display: none;")
                trLago = TR(TD(LABEL("Nombre Lago: ", _id="label9"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Lago", _id="Lago", _value=lago),_id="div"+str(rowLago), _class="w2p_fw"), _id="row"+str(rowLago), _style = "display: none;")
                trLagoDist = TR(TD(LABEL("Distancia al Lago (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distLago", _id="distLago", _value=distLago),_id="div"+str(rowLago) +"Dist", _class="w2p_fw"), _id="row"+str(rowLago) +"Dist", _style = "display: none;")
                trOceano = TR(TD(LABEL("Nombre Océano: ", _id="label10"), _class="w2p_fl"),TD(INPUT(_type="text",_name="Oceano", _id="oceano", _value=oceano),_id="div"+str(rowOceano), _class="w2p_fw"), _id="row"+str(rowOceano), _style = "display: none;")
                trOceanoDist = TR(TD(LABEL("Distancia al Océano (m): "), _class="w2p_fl"),TD(INPUT(_type="text", _class='double',_name="distOceano", _id="distOceano", _value=distOceano),_id="div"+str(rowOceano) +"Dist", _class="w2p_fw"), _id="row"+str(rowOceano) +"Dist", _style = "display: none;")
                form[0].insert(1,trRio)
                form[0].insert(2,trRioDist)
                form[0].insert(3,trArroyo)
                form[0].insert(4,trArroyoDist)
                form[0].insert(5,trCanada)
                form[0].insert(6,trCanadaDist)
                form[0].insert(7,trEmbalse)
                form[0].insert(8,trEmbalseDist)
                form[0].insert(9,trCanal)
                form[0].insert(10,trCanalDist)
                form[0].insert(11,trRepresa)
                form[0].insert(12,trRepresaDist)
                form[0].insert(13,trTajamar)
                form[0].insert(14,trTajamarDist)
                form[0].insert(15,trLaguna)
                form[0].insert(16,trLagunaDist)
                form[0].insert(17,trLago)
                form[0].insert(18,trLagoDist)
                form[0].insert(19,trOceano)
                form[0].insert(20,trOceanoDist)
                form.vars.muestreo = session.muestreoId
                if form.validate(keepvalues=True):
                    recordId = form.vars.id
                    row = db(db.Agua.muestreo==session.muestreoId).select().first()
                    first = True
                    names = ['Rio','Arroyo','Canada','Embalse','Canalderiego','Represa','Tajamar','Laguna','Oceano']
                    nombres = ""
                    for name in names:
                        if request.post_vars[name] != "":
                            if first:
                                nombres = name + ":" + request.post_vars[name] + "|"+ request.post_vars["dist"+name]
                                first = False
                            else:
                                nombres = nombres + "," + name + ":" + request.post_vars[name] + "|"+ request.post_vars["dist"+name]
                    saveWaterNames(session.muestreoId, nombres)
                    if row != None:
                        row.update_record(muestreo = session.muestreoId, tipoCaudal = form.vars.tipoCaudal, manejo = form.vars.manejo, frecuencia = form.vars.frecuencia, acuacultura = form.vars.acuacultura, gradoContaminacion = form.vars.gradoContaminacion)
                        response.flash = T("Successfully modified")
                    else:
                        db.Agua.insert(
                            muestreo = session.muestreoId,
                            tipoCaudal = form.vars.tipoCaudal,
                            manejo = form.vars.manejo,
                            frecuencia = form.vars.frecuencia,
                            acuacultura = form.vars.acuacultura,
                            gradoContaminacion = form.vars.gradoContaminacion
                        )
                        session.muestreoPorcentaje = returnPercentage()
                        response.flash = T("Successfully saved")
                    redirect(URL("agua", vars=dict(m=session.muestreoId)))
                elif form.errors:
                    response.flash = T("There are errors. Please correct them")
                else:
                    if recordId != None:
                        response.flash = T("Modify the data")
                    else:
                        response.flash = T("Fill in the data of water")
                return dict(form=form, update=update, m= session.muestreoId, menuL = sideMenu(), selected=8, agua = agua)
            else:
                redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def undoAgua():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneAgua = False)
    db(db.Agua.muestreo == muestreo).delete()

def undoFauna():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneFauna = False)
    db(db.Fauna.muestreo == muestreo).delete()

def undoEspeciesInvasoras():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneEspeciesInvasoras = False)
    db(db.EspeciesInvasoras.muestreo == muestreo).delete()

def siPresenciaFauna():
    muestreo = session.muestreoId
    db(
        db.TieneDatos.muestreo == muestreo
    ).update(
        tieneFauna = True
    )

def siPresenciaAgua():
    muestreo = session.muestreoId
    db(
        db.TieneDatos.muestreo == muestreo
    ).update(
        tieneAgua = True
    )

def siPresenciaEspecies():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneEspeciesInvasoras = True)

def siPresenciaFlora():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneFlora = True)

def undoFlora():
    muestreo = session.muestreoId
    db(db.TieneDatos.muestreo == muestreo).update(tieneFlora = False)
    db(db.Flora.muestreo == muestreo).delete()
    db(db.FloraDelSuelo.muestreo == muestreo).delete()

def saveWaterNames(m, names):
    """
    Método que inserta en la base de datos los nombres de los afluentes
    """
    muestreo = m
    db(db.NombreAfluentes.muestreo == muestreo).delete()
    nombres = (str(names)).split(',')
    for nombre in nombres:
        value = nombre.split(':')

        tipoCaudal = value[0]
        if value[0] == "Oceano":
            tipoCaudal = "Océano"
        if value[0] == "Rio":
            tipoCaudal = "Río"
        if value[0] == "Canalderiego":
            tipoCaudal = "Canal de Riego"
        if value[0] == "Canada":
            tipoCaudal = "Cañada"
        tipo = db(db.TipoCaudal.tipo == tipoCaudal).select().first()
        if tipo != None:
            data = value[1].split('|')
            nombreCaudal = data[0] if data[0] != "" else "Ninguno"
            distancia = float(data[1]) if data[1] != "" else 0.0
            db.NombreAfluentes.insert(muestreo = muestreo, nombre = nombreCaudal, tipo = tipo.id, distancia = distancia)

def tieneAgua(muestreo):
    tieneAguaFila = db(db.TieneDatos.muestreo == muestreo).select(db.TieneDatos.ALL).first()
    tieneDatos = False
    if tieneAguaFila:
        if tieneAguaFila.tieneAgua:
            tieneDatos = True
    return tieneDatos

@auth.requires_membership('digitador')
def tieneAguaForm():
    if __hasPermission(request.get_vars["m"]):
        db.TieneDatos.tieneAgua.widget = widget
        recordId = db(db.TieneDatos.muestreo==request.get_vars["m"]).select().first()
        form = SQLFORM(db.TieneDatos, record = recordId, showid = False, fields = ['tieneAgua'], submit_button='Guardar')
        form.vars.muestreo = request.get_vars["m"]
        session.menuL_enabled = True
        if form.accepts(request.vars, session):
            if form.vars.tieneAgua:
                redirect(URL('agua', vars=dict(m=request.get_vars["m"])))
        return dict(form = form, menuL = sideMenu(), selected=8)

def tieneFauna(muestreo):
    if __hasPermission(muestreo):
        tieneFaunaFila = db(db.TieneDatos.muestreo == muestreo).select(db.TieneDatos.ALL).first()
        tieneDatos = False
        if tieneFaunaFila:
            if tieneFaunaFila.tieneFauna:
                tieneDatos = True
        return tieneDatos

@auth.requires_membership('digitador')
def tieneFaunaForm():
    if __hasPermission(request.get_vars["m"]):
        db.TieneDatos.tieneFauna.widget = widget
        recordId = db(db.TieneDatos.muestreo==request.get_vars["m"]).select().first()
        form = SQLFORM(db.TieneDatos, record = recordId, showid = False, fields = ['tieneFauna'], submit_button='Guardar')
        form.vars.muestreo = request.get_vars["m"]
        session.menuL_enabled = True
        if form.accepts(request.vars, session):
            if form.vars.tieneFauna:
                redirect(URL('fauna', vars=dict(m=request.get_vars["m"])))
        return dict(form = form, menuL = sideMenu(), selected=9)

def tieneFlora(muestreo):
    if __hasPermission(muestreo):
        tieneFloraFila = db(db.TieneDatos.muestreo == muestreo).select(db.TieneDatos.ALL).first()
        tieneDatos = False
        if tieneFloraFila:
            if tieneFloraFila.tieneFlora:
                tieneDatos = True
        return tieneDatos

@auth.requires_membership('digitador')
def tieneFloraForm():
    if __hasPermission(request.get_vars["m"]):
        db.TieneDatos.tieneFlora.widget = widget
        recordId = db(db.TieneDatos.muestreo==request.get_vars["m"]).select().first()
        form = SQLFORM(db.TieneDatos, record = recordId, showid = False, fields = ['tieneFlora'], submit_button='Guardar')
        form.vars.muestreo = request.get_vars["m"]
        session.menuL_enabled = True
        if form.accepts(request.vars, session):
            if form.vars.tieneFlora:
                redirect(URL('flora', vars=dict(m=request.get_vars["m"])))
        return dict(form = form, menuL = sideMenu(), selected=14)

@auth.requires_membership('digitador')
def fauna():
    """
    Página que permite el ingreso de datos de la fauna existente en el punto muestral
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            fauna = tieneFauna(session.muestreoId)
            opts = []
            rows = db(db.TipoClase.id > 0).select()
            for row in rows:
                opts.append(OPTION(row.tipo, _value=row.id))
            form = FORM(TABLE(
                        TR(
                            TD(LABEL("Clase:"), _class="w2p_fl"), TD(SELECT(opts, _name='clase', _id='clase'),_class="w2p_fw"), TD("La clase del individuo observado", _class="w2p_fc")),
                        TR(
                            TD(LABEL("Nombre Científico:"),_class="w2p_fl"),TD(INPUT(_type='text', _name="nomCientifico", _id ="nomCientifico", _autocomplete="off",  _onkeyup="getData(this.value,0);", requires=IS_NOT_EMPTY()),_class="w2p_fw"), TD("Nombre científico del individuo", _class="w2p_fc")),
                        TR(
                            TD(LABEL("")),TD(DIV("", _id="cientificos", _class = "ajaxresults"))),
                        TR(
                            TD(LABEL("Nombre Común:"), _class="w2p_fl"),TD(INPUT(_type='text', _id ="nomComun", _name ="nomComun", _autocomplete="off", _onkeyup="getData(this.value,1);"),_class="w2p_fw"), TD("Nombre común del individuo", _class="w2p_fc")),
                        TR(
                            TD(LABEL("")),TD(DIV("", _id="comunes", _class = "ajaxresults"))),
                        TR(
                            TD(LABEL("Frecuencia:"),_class="w2p_fl"),TD(INPUT(_type='text',_name = "frecuencia", _id ="frecuencia", _value="0", _onKeyPress="return numbersonly(this, event)", requires = IS_INT_IN_RANGE(0,500)),_class="w2p_fw"), TD("Cantidad de individuos observados", _class="w2p_fc")),
                        TR(
                            TD(_class = "w2p_fl"),TD(INPUT(_type = "submit", _value= "Guardar"),_class = "w2p_fw"),
                            _id="submit_record__row"
                        )
                    ), _method = 'POST')
            form.vars.muestreo = session.muestreoId
            if request.post_vars['nomCientifico'] and request.post_vars['clase']:
                idEspecie = db(db.TipoNombreCientificoClase.clase == int(request.post_vars['clase']))(db.TipoNombreCientificoClase.nomCientifico == request.post_vars['nomCientifico']).select().first()
                if idEspecie != None:
                    form.vars.especie = idEspecie
            if form.accepts(request.vars, session):
                frecuencia = int(request.post_vars['frecuencia'])
                alreadyAdded = db(db.Fauna.especie == idEspecie)(db.Fauna.muestreo == session.muestreoId).select(db.Fauna.id).first()
                if alreadyAdded != None:
                    aux = db(db.Fauna.id == alreadyAdded).select(db.Fauna.frec).first()
                    db(db.Fauna.id == alreadyAdded).update(frec = aux.frec + frecuencia)
                else:
                    db.Fauna.insert(muestreo = session.muestreoId, especie = idEspecie, frec = frecuencia)
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                response.flash = T("Fill in the data of wildlife")
            return dict(form=form, menuL = sideMenu(), selected=9, fauna = fauna)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def faunaNames():
    """
    Método utilizado para hacer el auto completado de la fauna
    """
    partialstr = request.get_vars['partialstr']
    clase = request.get_vars["clase"]
    common = int(request.get_vars["comun"])
    if(common == 0):
        query = db.TipoNombreCientificoClase.nomCientifico.like(partialstr+'%')
        nombres = db(query)(db.TipoNombreCientificoClase.clase == clase).select(db.TipoNombreCientificoClase.nomCientifico, orderby=db.TipoNombreCientificoClase.nomCientifico)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nomCientifico, _id="res%s"%i, _onclick="copyToBox($('#res%s').html(),0)"%i, _style="cursor: pointer"), _id="nomCientifico"))
        return TAG[''](*items)
    else:
        query = db.TipoNombreComun.nombreComun.like(partialstr+'%')
        nombres = db(query)(db.TipoNombreCientificoClase.clase == clase)(db.TipoNombreComun.especie == db.TipoNombreCientificoClase.id).select(db.TipoNombreComun.nombreComun, orderby=db.TipoNombreComun.nombreComun)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nombreComun, _id="resCom%s"%i, _onclick="copyToBox($('#resCom%s').html(),1)"%i, _style="cursor: pointer"), _id="nombreComun"))
        return TAG[''](*items)


def faunaCommonNames():
    """
    Método que retorna el nombre común del nombre científico
    """
    if request.get_vars['nomCientifico']:
        row = db(db.TipoNombreCientificoClase.id == db.TipoNombreComun.especie)(db.TipoNombreCientificoClase.nomCientifico == request.get_vars['nomCientifico']).select().first()
        if row != None:
            return row.TipoNombreComun.nombreComun
        else:
            return ""

def faunaCientificNames():
    """
    Método que retorna el nombre científico a partir del nombre común
    """
    if request.get_vars['nomComun']:
        row = db(db.TipoNombreCientificoClase.id == db.TipoNombreComun.especie)(db.TipoNombreComun.nombreComun == request.get_vars['nomComun']).select().first()
        if row != None:
            return row.TipoNombreCientificoClase.nomCientifico
        else:
            return ""


def tableFauna():
    headers = ['Tipo','Nombre Cientifico', 'Nombre Comun', 'Frecuencia', 'Acciones']
    rows = []
    fauna = db(db.TipoClase.id == db.TipoNombreCientificoClase.clase)(db.TipoNombreComun.especie == db.TipoNombreCientificoClase.id)(db.Fauna.especie == db.TipoNombreCientificoClase.id)(db.Fauna.muestreo == session.muestreoId).select()
    for r in fauna:
        cell = {'tipo':r.TipoClase.tipo, 'nomCient':r.TipoNombreCientificoClase.nomCientifico, 'nomCom':r.TipoNombreComun.nombreComun, 'frec':r.Fauna.frec, 'id':r.Fauna.id}
        rows.append(cell)
    return dict(fauna = [rows,headers])


@auth.requires_membership('digitador')
def relieve():
    """
    Página que permite el ingreso de datos del relieve en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.Relieve.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.Relieve, record=recordId, showid = False, fields = ['ubicacion','exposicion','pendiente', 'formaPendiente'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.Relieve.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.Relieve.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("relieve", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of the contour")
            return dict(form=form, menuL = sideMenu(), selected=10)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

@auth.requires_membership('digitador')
def suelo():
    """
    Página que permite el ingreso de datos del suelo en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.Suelo.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            db.Suelo.impedimento.widget = widget
            db.Suelo.olor.widget = widget
            db.Suelo.micorrizas.widget = widget
            db.Suelo.faunaSuelo.widget = widget
            if session.plant == True:
                form = SQLFORM(db.Suelo, record=recordId, showid = False, fields = ['grupoConeat','usoTierra','usoPrevio','tipoLabranza','gradoErosion', 'tipoErosion','profundidadPrimerHorizonte','profundidadMantillo','profundidadHumus','color','textura','estructura','drenaje','infiltracion','impedimento','olor','humedad','pedregosidad','rocosidad','micorrizas','faunaSuelo', 'raices'], submit_button='Guardar')
            else:
                form = SQLFORM(db.Suelo, record=recordId, showid = False, fields = ['grupoConeat','usoTierra','usoPrevio','gradoErosion', 'tipoErosion','profundidadPrimerHorizonte','profundidadMantillo','profundidadHumus','color','textura','estructura','drenaje','infiltracion','impedimento','olor','humedad','pedregosidad','rocosidad','micorrizas','faunaSuelo', 'raices'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.Suelo.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.Suelo.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("suelo", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of the soil")
            return dict(form=form, menuL = sideMenu(), selected=11)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


@auth.requires_membership('digitador')
def coberturaVegetal():
    """
    Página que permite el ingreso de datos de la cobertura vegetal en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.CoberturaVegetal.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.CoberturaVegetal, record=recordId, showid = False, fields = ['gradoCoberturaCopas', 'gradoSotobosque', 'coberturaHerbacea','coberturaResiduosPlantas','coberturaResiduosCultivos'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.CoberturaVegetal.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.CoberturaVegetal.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("coberturaVegetal", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of vegetation")
            return dict(form=form, menuL = sideMenu(), selected=12)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

@auth.requires_membership('digitador')
def productosNoMadereros():
    """
    Página que permite el ingreso de datos de los productos no madereros del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.ProductosNoMadereros.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            db.ProductosNoMadereros.produccionApicola.widget = widget
            db.ProductosNoMadereros.sombra.widget = widget
            db.ProductosNoMadereros.rompeVientos.widget = widget
            db.ProductosNoMadereros.recoleccionHongos.widget = widget
            db.ProductosNoMadereros.aceitesEsenciales.widget = widget
            db.ProductosNoMadereros.obtencionSemillas.widget = widget
            db.ProductosNoMadereros.actividadesRecreacion.widget = widget
            db.ProductosNoMadereros.actividadesCasaPesca.widget = widget
            db.ProductosNoMadereros.estudiosCientificos.widget = widget
            db.ProductosNoMadereros.fijacionCarbono.widget = widget
            form = SQLFORM(db.ProductosNoMadereros, record=recordId, showid = False, fields = ['tipoGanado','intensidadPastoreo','sistemasProduccion','produccionApicola','sombra','rompeVientos','recoleccionHongos','aceitesEsenciales','obtencionSemillas','actividadesCasaPesca','actividadesRecreacion','estudiosCientificos','fijacionCarbono'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.ProductosNoMadereros.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.ProductosNoMadereros.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("productosNoMadereros", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of non-timber products")
            return dict(form=form, menuL = sideMenu(), selected=13)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


@auth.requires_membership('digitador')
def flora():
    """
    Página que permite el ingreso de datos de la flora existente en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        if __hasGeneralData(session.muestreoId):
            checkNewRepSel()
            flora= tieneFlora(session.muestreoId)
            recordId = db(db.Flora.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.Flora, record=recordId, showid = False, fields = ['tipoSotobosque','alturaSotobosque'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            floraForm = getFloraSueloForm()
            if form.validate(keepvalues=True):
                row = db(db.Flora.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(muestreo=form.vars.muestreo, tipoSotobosque=form.vars.tipoSotobosque, alturaSotobosque=form.vars.alturaSotobosque)
                    response.flash = T("Successfully modified")
                else:
                    db.Flora.insert(muestreo=form.vars.muestreo, tipoSotobosque=form.vars.tipoSotobosque, alturaSotobosque=form.vars.alturaSotobosque)
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("flora", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of the flora")
            return dict(form=form, floraForm = floraForm, menuL = sideMenu(), selected=14, flora = flora)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def addFloraSuelo():
    nombreCientifico = request.get_vars['nomCientifico']
    frecuencia = request.get_vars['frec']
    idNomCient = db(db.TipoFloraNombreCientifico.tipo == nombreCientifico).select(db.TipoFloraNombreCientifico.id).first()
    if idNomCient:
        db.FloraDelSuelo.insert(muestreo=session.muestreoId, nombreCientifico=idNomCient, frecuencia = frecuencia)
        return 'Se guardo con exito!'
    else:
        return 'El nombre cientifico es incorrecto'


def getFloraSueloForm():
    opts = []
    rows = db().select(db.TipoFrecuenciaFloraDelSuelo.ALL)
    for row in rows:
        opts.append(OPTION(row.tipo, _value=row.id))
    form = FORM(
            TABLE(
                TR(
                    TD(LABEL("Nombre Científico:"),_class="w2p_fl"),
                    TD(
                        INPUT(_type='text', _name="nomCientifico", _id ="nomCientifico", _autocomplete="off", _onkeyup="getData(this.value,0);",requires=IS_NOT_EMPTY()),
                        _class="w2p_fw"
                    ),
                    TD("Nombre científico de la flora del suelo", _class="w2p_fc")
                ),
                TR(
                    TD(LABEL("")),
                    TD(DIV("", _id="cientificos", _class = "ajaxresults"))
                ),
                TR(
                    TD(LABEL("Nombre Común:"),_class="w2p_fl"),
                    TD(
                        INPUT(_type='text', _name="nombreComun", _id ="nombreComun", _autocomplete="off", _onkeyup="getData(this.value,1);"),
                        _class="w2p_fw"
                    ),
                    TD("Nombre común de la flora del suelo", _class="w2p_fc")
                ),
                TR(
                    TD(LABEL("")),
                    TD(DIV("", _id="comunes", _class = "ajaxresults"))
                ),
                TR(
                    TD(LABEL("Frecuencia:"),_class="w2p_fl"),
                    TD(SELECT(opts, _name='frec', _id='frec'),_class="w2p_fw"),
                    TD("Frecuencia de la flora del suelo", _class="w2p_fc")
                )
            )
    )
    form.vars.muestreo = session.muestreoId
    return form


def tableFloraSuelo():
    headers = ['Nombre Cientifico', 'Nombre Comun', 'Frecuencia', 'Acciones']
    rows = []
    floraSuelo = db(db.FloraDelSuelo.muestreo==session.muestreoId)(db.FloraDelSuelo.nombreCientifico==db.TipoFloraNombreCientifico.id)(db.FloraDelSuelo.frecuencia == db.TipoFrecuenciaFloraDelSuelo.id).select()
    for r in floraSuelo:
        nomComun = db(r.TipoFloraNombreCientifico.id == db.TipoFloraNombreComun.nombreCientifico).select(db.TipoFloraNombreComun.nombreComun).first()
        if nomComun != None:
            nombreComun = nomComun.nombreComun
        else:
            nombreComun = ""
        cell = {
            'nomCient':r.TipoFloraNombreCientifico.tipo,
            'nomCom':nombreComun,
            'frec':r.TipoFrecuenciaFloraDelSuelo.tipo,
            'id':r.FloraDelSuelo.id
        }
        rows.append(cell)
    return dict(flora = [rows,headers])

def floraNames():
    """
    Método que se utiliza para el auto completado de los nombres de la flora del suelo
    """
    partialstr = request.get_vars['partialstr']
    common = int(request.get_vars["comun"])
    if(common == 0):
        query = db.TipoFloraNombreCientifico.tipo.like(partialstr+'%')
        nombres = db(query).select(db.TipoFloraNombreCientifico.tipo, orderby=db.TipoFloraNombreCientifico.tipo)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.tipo, _id="res%s"%i, _onclick="copyToBox($('#res%s').html(),0)"%i, _style="cursor: pointer"), _id="nomCientifico"))
        return TAG[''](*items)
    else:
        query = db.TipoFloraNombreComun.nombreComun.like(partialstr+'%')
        nombres = db(query)(db.TipoFloraNombreComun.nombreCientifico == db.TipoFloraNombreCientifico.id).select(db.TipoFloraNombreComun.nombreComun, orderby=db.TipoFloraNombreComun.nombreComun)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nombreComun, _id="resCom%s"%i, _onclick="copyToBox($('#resCom%s').html(),1)"%i, _style="cursor: pointer"), _id="nombreComun"))
        return TAG[''](*items)


def floraCommonNames():
    """
    Método que retorna el nombre común de la especie de flora teniendo el nombre científico
    """
    if request.get_vars['nomCientifico']:
        row = db(db.TipoFloraNombreCientifico.id == db.TipoFloraNombreComun.nombreCientifico)(db.TipoFloraNombreCientifico.tipo == request.get_vars['nomCientifico']).select().first()
        if row != None:
            return row.TipoFloraNombreComun.nombreComun
        else:
            return ""

def floraCientificNames():
    """
    Método que devuelve el nombre científico de la flora del suelo a partir del nombre común
    """
    if request.get_vars['nomComun']:
        row = db(db.TipoFloraNombreCientifico.id == db.TipoFloraNombreComun.nombreCientifico)(db.TipoFloraNombreComun.nombreComun == request.get_vars['nomComun']).select().first()
        return row.TipoFloraNombreCientifico.tipo

@auth.requires_membership('digitador')
def problemasAmbientales():
    """
    Página que permite el ingreso de datos de los problemas ambientales en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.ProblemasAmbientales.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            db.ProblemasAmbientales.pobreCalidadAgua.widget = widget
            db.ProblemasAmbientales.polucionAire.widget = widget
            db.ProblemasAmbientales.perdidaFertilidad.widget = widget
            db.ProblemasAmbientales.invasionEspecies.widget = widget
            db.ProblemasAmbientales.presenciaPesticidas.widget = widget
            form = SQLFORM(db.ProblemasAmbientales, record=recordId, showid = False, fields = ['pobreCalidadAgua','polucionAire','perdidaFertilidad','invasionEspecies','presenciaPesticidas'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.ProblemasAmbientales.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.ProblemasAmbientales.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("problemasAmbientales", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of the environmental problems")
            return dict(form=form, menuL = sideMenu(), selected=16)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

@auth.requires_membership('digitador')
def ForestacionMantenimientoEstructura():
    """
    Página que permite el ingreso de datos de la forestación, el mantenimiento y estructura del punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.ForestacionMantenimientoEstructura.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            db.ForestacionMantenimientoEstructura.planManejo.widget = widget
            db.ForestacionMantenimientoEstructura.manejoSilvicultural.widget = widget
            form = SQLFORM(db.ForestacionMantenimientoEstructura, record=recordId, showid = False,fields = ['origenPlantacion','estructura','propiedadTierra','planManejo','gradoIntervencion','destinoMadera','manejoSilvicultural','tecnologiaExplotacion'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if form.validate(keepvalues=True):
                recordId = form.vars.id
                row = db(db.ForestacionMantenimientoEstructura.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.ForestacionMantenimientoEstructura.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("ForestacionMantenimientoEstructura", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of structure maintenance and forestation")
            return dict(form=form, menuL = sideMenu(), selected=17)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

@auth.requires_membership('digitador')
def fuego():
    """
    Página que permite el ingreso de datos de fuego en el punto muestral
    """
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            recordId = db(db.Fuego.muestreo==session.muestreoId).select().first()
            if recordId != None:
                recordId = recordId.id
            form = SQLFORM(db.Fuego, record=recordId, showid = False,fields = ['evidenciaFuego','tipoFuego','propositoFuego'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId

            if form.validate(keepvalues=True):
                row = db(db.Fuego.muestreo==session.muestreoId).select().first()
                if row != None:
                    row.update_record(**dict(form.vars))
                    response.flash = T("Successfully modified")
                else:
                    db.Fuego.insert(**dict(form.vars))
                    session.muestreoPorcentaje = returnPercentage()
                    response.flash = T("Successfully saved")
                redirect(URL("fuego", vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if recordId != None:
                    response.flash = T("Modify the data")
                else:
                    response.flash = T("Fill in the data of fire")
            return dict(form=form, menuL = sideMenu(), selected=18)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def tieneEspeciesInvasoras(muestreo):
    if __hasPermission(muestreo):
        tieneEspeciesInvasorasFila = db(db.TieneDatos.muestreo == muestreo).select(db.TieneDatos.ALL).first()
        tieneDatos = False
        if tieneEspeciesInvasorasFila:
            if tieneEspeciesInvasorasFila.tieneEspeciesInvasoras:
                tieneDatos = True
        return tieneDatos

@auth.requires_membership('digitador')
def tieneEspeciesInvasorasForm():
    if __hasPermission(request.get_vars["m"]):
        db.TieneDatos.tieneEspeciesInvasoras.widget = widget
        recordId = db(db.TieneDatos.muestreo==request.get_vars["m"]).select().first()
        form = SQLFORM(db.TieneDatos, record = recordId, showid = False, fields = ['tieneEspeciesInvasoras'], submit_button='Guardar')
        form.vars.muestreo = request.get_vars["m"]
        session.menuL_enabled = True
        if form.accepts(request.vars, session):
            if form.vars.tieneEspeciesInvasoras:
                redirect(URL('especiesInvasoras', vars=dict(m=request.get_vars["m"])))
        return dict(form = form, menuL = sideMenu(), selected=19)


@auth.requires_membership('digitador')
def especiesInvasoras():
    """
    Página que permite el ingreso de datos sobre las especies invasoras presentes en el punto muestral
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            especies = tieneEspeciesInvasoras(session.muestreoId)
            form = SQLFORM(
                db.EspeciesInvasoras,
                showid = False,
                fields = ['severidad'],
                submit_button='Guardar'
            )
            form.vars.muestreo = session.muestreoId
            nombreCientificoInput = TR(
                TD(LABEL("Nombre Científico:"),_class="w2p_fl"),
                TD(
                    INPUT(_type='text', _name="nomCientifico", _id ="nomCientifico", _autocomplete="off", _onkeyup="getData(this.value,0);",requires=IS_NOT_EMPTY())
                    ,_class="w2p_fw"
                ),
                TD("Nombre científico de la especie invasora", _class="w2p_fc")
            )
            ajaResCientificos = TR(
                TD(LABEL("")),
                TD(DIV("", _id="cientificos", _class = "ajaxresults"))
            )
            nombreComunInput = TR(
                TD(LABEL("Nombre Común:"),_class="w2p_fl"),
                TD(
                    INPUT(_type='text', _name="nombreComun", _id ="nombreComun", _autocomplete="off", _onkeyup="getData(this.value,1);",requires=IS_NOT_EMPTY()),
                    _class="w2p_fw"
                ),
                TD("Nombre común de la especie invasora", _class="w2p_fc")
            )
            ajaxResComunes = TR(
                TD(LABEL("")),
                TD(DIV("", _id="comunes", _class = "ajaxresults"))
            )
            categoriaInput = TR(
                TD(LABEL("Categoría:"), _class="w2p_fl"),
                TD(
                    INPUT(_type="text",_name="categoria", _id="categoria", _value="", _disabled="disabled"),
                    _class="w2p_fw")
            )
            form[0].insert(0, nombreCientificoInput)
            form[0].insert(1, ajaResCientificos)
            form[0].insert(2, nombreComunInput)
            form[0].insert(3, ajaxResComunes)
            form[0].insert(-1, categoriaInput)
            if request.post_vars['nomCientifico']:
                row = db(db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico == request.post_vars['nomCientifico']).select().first()
                if row != None:
                    form.vars.nombreCientifico = row.id
            if form.accepts(request.vars, session):
                response.flash = T("Successfully saved")
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                response.flash = T("Fill in the data of invasive species")
            return dict(form=form, menuL = sideMenu(), selected=19, especies = especies)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def tableEspeciesInvasoras():
    headers = ['Nombre Cientifico', 'Nombre Comun', 'Severidad', 'Categoria', 'Acciones']
    rows = []
    especiesInvasoras = db(db.EspeciesInvasoras.muestreo==session.muestreoId)(db.EspeciesInvasoras.severidad == db.TipoSeveridad.id)(db.EspeciesInvasoras.nombreCientifico==db.TipoNombreCientificoEspeciesInvasoras.id)(db.TipoCategoriaEspeciesInvasoras.id==db.TipoNombreCientificoEspeciesInvasoras.categoria)(db.TipoNombreCientificoEspeciesInvasoras.id == db.TipoNombreComunEspeciesInvasoras.nombreCientifico).select()
    for r in especiesInvasoras:
        cell = {
            'nomCient':r.TipoNombreCientificoEspeciesInvasoras.nombreCientifico,
            'nomCom':r.TipoNombreComunEspeciesInvasoras.nombreComun,
            'sev':r.TipoSeveridad.tipo,
            'cat':r.TipoCategoriaEspeciesInvasoras.tipo,
            'id':r.EspeciesInvasoras.id
        }
        rows.append(cell)
    return dict(especies = [rows,headers])

def especiesInvasorasNames():
    """
    Método utilizado para el auto completado de los nombres de las especies invasoras
    """
    partialstr = request.get_vars['partialstr']
    common = int(request.get_vars["comun"])
    if(common == 0):
        query = db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico.like(partialstr+'%')
        nombres = db(query).select(db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico, orderby=db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nombreCientifico, _id="res%s"%i, _onclick="copyToBox($('#res%s').html(),0)"%i, _style="cursor: pointer"), _id="nomCientifico"))
        return TAG[''](*items)
    else:
        query = db.TipoNombreComunEspeciesInvasoras.nombreComun.like(partialstr+'%')
        nombres = db(query)(db.TipoNombreComunEspeciesInvasoras.nombreCientifico == db.TipoNombreCientificoEspeciesInvasoras.id).select(db.TipoNombreComunEspeciesInvasoras.nombreComun, orderby=db.TipoNombreComunEspeciesInvasoras.nombreComun)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nombreComun, _id="resCom%s"%i, _onclick="copyToBox($('#resCom%s').html(),1)"%i, _style="cursor: pointer"), _id="nombreComun"))
        return TAG[''](*items)


def especiesInvasorasCommonNames():
    """
    Método que retorna el nombre común de la especie invasora a partir del nombre científico
    """
    if request.get_vars['nomCientifico']:
        row = db(db.TipoNombreCientificoEspeciesInvasoras.id == db.TipoNombreComunEspeciesInvasoras.nombreCientifico)(db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico == request.get_vars['nomCientifico']).select().first()
        if row != None:
            return row.TipoNombreComunEspeciesInvasoras.nombreComun

def especiesInvasorasCientificNames():
    """
    Método que retorna el nombre científico de la especie invasora a partir del nombre común
    """
    if request.get_vars['nomComun']:
        """row = db(db.TipoNombreCientificoClase.id == db.TipoNombreComun.especie)(db.TipoNombreComun.nombreComun == request.get_vars['nomComun']).select().first()"""
        row = db(db.TipoNombreCientificoEspeciesInvasoras.id == db.TipoNombreComunEspeciesInvasoras.nombreCientifico)(db.TipoNombreComunEspeciesInvasoras.nombreComun == request.get_vars['nomComun']).select().first()
        return row.TipoNombreCientificoEspeciesInvasoras.nombreCientifico

def especiesInvasorasCategory():
    """
    Método que retorna la categoría de la especie invasora seleccionada
    """
    if request.get_vars['nomCientifico']:
        row = db(db.TipoNombreCientificoEspeciesInvasoras.nombreCientifico == request.get_vars['nomCientifico'])(db.TipoCategoriaEspeciesInvasoras.id == db.TipoNombreCientificoEspeciesInvasoras.categoria).select().first()
        if row!= None:
            return row.TipoCategoriaEspeciesInvasoras.tipo

@auth.requires_membership('digitador')
def SanidadEucalipto():
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            muestreo = request.get_vars['m']
            from plugin_dm.datamanager import DataManager
            dm=DataManager(database=db, muestreo=muestreo)
            query=(
                (db.EnfermedadesEucalyptus.id > 0) &
                (db.TipoEnfermedadEucalyptus.id==db.EnfermedadesEucalyptus.tipo_enfermedad) &
                (db.TipoOpcionParaEnfermedadEucalyptus.id==db.EnfermedadesEucalyptus.opcion_id)
                )
            dm.gQuery( query )
            dm.gOrder(db.EnfermedadesEucalyptus.numArbol)
            dm.actionTableName('EnfermedadesEucalyptus')
            dm.gFieldId('id')
            dm.gFields( [
                ('EnfermedadesEucalyptus','numArbol'),
                ('TipoEnfermedadEucalyptus','tipo_enfermedad'),
                ('TipoOpcionParaEnfermedadEucalyptus','opcion'),
                ] )
            dm.gShowId(False)
            grid = dm.grid()
            return dict(toolbar=dm.toolBar(), grid=grid, muestreo = muestreo, menuL = sideMenu(), selected=24)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def getAvailableTreesE():
    muestreo = request.post_vars.muestreo
    arboles = db(db.ParcelasBosquePlantado.muestreo == muestreo).select(db.ParcelasBosquePlantado.numArbol)
    return dict(arboles = arboles)

def subSelectDataSanidadE():
    """
    Retorna las opciones de sub especie dependiendo del género seleccionado
    """
    if request.get_vars['id']:
        idParent = int(request.get_vars['id'])
        rows = db(db.TipoOpcionParaEnfermedadEucalyptus.enfermedad_id == idParent).select(db.TipoOpcionParaEnfermedadEucalyptus.ALL, orderby=db.TipoOpcionParaEnfermedadEucalyptus.id)
        ret = dict()
        for row in rows:
            ret[row.id] = row.opcion
        import gluon.contrib.simplejson
        return gluon.contrib.simplejson.dumps(ret)
    else:
        pass

def getRemainingDiseasesEucalyptus():
    numArbol = str(request.get_vars['numArbol'])
    ret = dict()
    if validateIfTreeExists(int(numArbol)):
        query = """SELECT TipoEnfermedadEucalyptus.*
                   FROM TipoEnfermedadEucalyptus
                   WHERE TipoEnfermedadEucalyptus.id NOT IN
                   (
                        SELECT TipoEnfermedadEucalyptus.id
                        FROM TipoEnfermedadEucalyptus, EnfermedadesEucalyptus
                        WHERE TipoEnfermedadEucalyptus.id = EnfermedadesEucalyptus.tipo_enfermedad AND
                              EnfermedadesEucalyptus.numArbol = %s

                   )
                """ % numArbol
        query_results = db.executesql(query)
        for result in query_results:
            ret[result[0]] = result[1]
    else:
        ret["error"] = "Numero de Arbol erroneo"
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(ret)

def validateIfTreeExists(tree_number):
    arboles = db(db.ParcelasBosquePlantado.numArbol == tree_number).select(db.ParcelasBosquePlantado.ALL)
    exists = False
    if len(arboles) > 0:
        exists = True
    return exists

@auth.requires_membership('digitador')
def SanidadPino():
    if __hasPermission(request.get_vars["m"]):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            muestreo = request.get_vars['m']
            from plugin_dm.datamanager import DataManager
            dm=DataManager(database=db, muestreo=muestreo)
            query=(
                (db.EnfermedadesPino.id > 0) &
                (db.TipoEnfermedadPino.id==db.EnfermedadesPino.tipo_enfermedad) &
                (db.TipoOpcionParaEnfermedadPino.id==db.EnfermedadesPino.opcion_id)
                )
            dm.gQuery( query )
            dm.gOrder(db.EnfermedadesPino.numArbol)
            dm.actionTableName('EnfermedadesPino')
            dm.gFieldId('id')
            dm.gFields( [
                ('EnfermedadesPino','numArbol'),
                ('TipoEnfermedadPino','tipo_enfermedad'),
                ('TipoOpcionParaEnfermedadPino','opcion'),
                ] )
            dm.gShowId(False)
            grid = dm.grid()
            return dict(toolbar=dm.toolBar(), grid=grid, muestreo = muestreo, menuL = sideMenu(), selected=24)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def getAvailableTreesP():
    muestreo = request.post_vars.muestreo
    arboles = db(db.ParcelasBosquePlantado.muestreo == muestreo).select(db.ParcelasBosquePlantado.numArbol)
    return dict(arboles = arboles)

def subSelectDataSanidadP():
    """
    Retorna las opciones de sub especie dependiendo del género seleccionado
    """
    if request.get_vars['id']:
        idParent = int(request.get_vars['id'])
        rows = db(db.TipoOpcionParaEnfermedadPino.enfermedad_id == idParent).select(db.TipoOpcionParaEnfermedadPino.ALL, orderby=db.TipoOpcionParaEnfermedadPino.id)
        ret = dict()
        for row in rows:
            ret[row.id] = row.opcion
        import gluon.contrib.simplejson
        return gluon.contrib.simplejson.dumps(ret)
    else:
        pass

def getRemainingDiseasesPino():
    numArbol = str(request.get_vars['numArbol'])
    ret = dict()
    if validateIfTreeExists(int(numArbol)):
        query = """SELECT TipoEnfermedadPino.*
                   FROM TipoEnfermedadPino
                   WHERE TipoEnfermedadPino.id NOT IN
                   (
                        SELECT TipoEnfermedadPino.id
                        FROM TipoEnfermedadPino, EnfermedadesPino
                        WHERE TipoEnfermedadPino.id = EnfermedadesPino.tipo_enfermedad AND
                              EnfermedadesPino.numArbol = %s

                   )
                """ % numArbol
        query_results = db.executesql(query)
        for result in query_results:
            ret[result[0]] = result[1]
    else:
        ret["error"] = "Numero de Arbol erroneo"
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(ret)

@auth.requires_membership('digitador')
def parcelaBosqueNatural():
    """
    Página que permite el ingreso de datos de la parcela de bosque natural
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            form = SQLFORM(
                db.ParcelasBosqueNatural,
                showid = False,
                fields = [
                    'numArbol',
                    'dap1',
                    'dap2',
                    'rangoEdad',
                    'ht',
                    'estrato',
                    'observaciones'
                    ],
                submit_button='Guardar'
            )
            form.vars.muestreo = session.muestreoId
            nombreCientificoInput = TR(
                TD(
                    LABEL("Nombre Científico:"),
                   _class="w2p_fl"
                ),
                TD(
                    INPUT(
                        _type='text',
                        _name="nomCientifico",
                        _id ="nomCientifico",
                        _autocomplete="off",
                        _onkeyup="getData(this.value,0);",
                        requires=IS_NOT_EMPTY()
                    ),
                    _class="w2p_fw"
                ),
                TD(
                    "Nombre científico de la especie invasora",
                    _class="w2p_fc"
                )
            )
            ajaResCientificos = TR(TD(LABEL("")),TD(DIV("", _id="cientificos", _class = "ajaxresults")))
            nombreComunInput = TR(TD(LABEL("Nombre Común:"),_class="w2p_fl"),TD(INPUT(_type='text', _name="nombreComun", _id ="nombreComun", _autocomplete="off", _onkeyup="getData(this.value,1);"),_class="w2p_fw"), TD("Nombre común de la especie invasora", _class="w2p_fc"))
            ajaxResComunes = TR(TD(LABEL("")),TD(DIV("", _id="comunes", _class = "ajaxresults")))
            form[0].insert(3, nombreCientificoInput)
            form[0].insert(4, ajaResCientificos)
            form[0].insert(5, nombreComunInput)
            form[0].insert(6, ajaxResComunes)
            if request.post_vars['nomCientifico']:
                row = db(db.TipoBNNombreCientifico.tipo == request.post_vars['nomCientifico']).select().first()
                if row != None:
                    form.vars.nombreCientifico = row.id
            if form.accepts(request.vars, session):
                response.flash = T("Successfully saved")
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                response.flash = T("Fill in the data of the trees")
            return dict(form=form, menuL = sideMenu(), selected=25)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))

def bnNames():
    """
    Método utilizado para el auto completado de los nombres de los árboles presentes en una parcela de bosque natural
    """
    partialstr = request.get_vars['partialstr']
    common = int(request.get_vars["comun"])
    if(common == 0):
        query = db.TipoBNNombreCientifico.tipo.like(partialstr+'%')
        nombres = db(query).select(db.TipoBNNombreCientifico.tipo, orderby=db.TipoBNNombreCientifico.tipo)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.tipo, _id="res%s"%i, _onclick="copyToBox($('#res%s').html(),0)"%i, _style="cursor: pointer"), _id="nomCientifico"))
        return TAG[''](*items)
    else:
        query = db.TipoBNNombreComun.nombreComun.like(partialstr+'%')
        nombres = db(query)(db.TipoBNNombreComun.nombreCientifico == db.TipoBNNombreCientifico.id).select(db.TipoBNNombreComun.nombreComun, orderby=db.TipoBNNombreComun.nombreComun)
        items = []
        for (i,nombre) in enumerate(nombres):
            items.append(DIV(LI(nombre.nombreComun, _id="resCom%s"%i, _onclick="copyToBox($('#resCom%s').html(),1)"%i, _style="cursor: pointer"), _id="nombreComun"))
        return TAG[''](*items)


def bnCommonNames():
    """
    Método que retorna el nombre común, si existe, a partir del nombre científico de una especie de bosque nativo
    """
    if request.get_vars['nomCientifico']:
        row = db(db.TipoBNNombreCientifico.id == db.TipoBNNombreComun.nombreCientifico)(db.TipoBNNombreCientifico.tipo == request.get_vars['nomCientifico']).select().first()
        if row != None:
            return row.TipoBNNombreComun.nombreComun
        else:
            return ""

def bnCientificNames():
    """
    Método que devuelve el nombre científico de la especie de bosque nativo a partir del nombre común
    """
    if request.get_vars['nomComun']:
        row = db(db.TipoBNNombreCientifico.id == db.TipoBNNombreComun.nombreCientifico)(db.TipoBNNombreComun.nombreComun == request.get_vars['nomComun']).select().first()
        return row.TipoBNNombreCientifico.tipo

def tableParcelasBosqueNatural():
    rows = []
    headers = ['Arbol', 'DAP1', 'DAP2', 'Nombre Cientifico', 'Nombre Comun', 'Edad', 'HT', 'Estrato', 'Observaciones', 'Acciones']
    parcelas = db(db.ParcelasBosqueNatural.muestreo==session.muestreoId)(db.ParcelasBosqueNatural.nombreCientifico == db.TipoBNNombreCientifico.id)(db.ParcelasBosqueNatural.estrato==db.TipoEstrato.id)(db.ParcelasBosqueNatural.rangoEdad == db.TipoRangoEdadNativo.id).select()
    for r in parcelas:
        nombreComun = db(db.TipoBNNombreCientifico.id == db.TipoBNNombreComun.nombreCientifico)(db.TipoBNNombreCientifico.id == r.TipoBNNombreCientifico.id).select(db.TipoBNNombreComun.ALL).first()
        if not nombreComun:
            nombreComun = "No tiene"
        else:
            nombreComun = nombreComun.nombreComun
        cell = {'arbol':r.ParcelasBosqueNatural.numArbol, 'dap1':r.ParcelasBosqueNatural.dap1, 'dap2':r.ParcelasBosqueNatural.dap2,
                'nomCient':r.TipoBNNombreCientifico.tipo, 'nomCom':nombreComun, 'edad':r.TipoRangoEdadNativo.tipo,
                'ht':r.ParcelasBosqueNatural.ht, 'estr':r.TipoEstrato.tipo, 'obs':r.ParcelasBosqueNatural.observaciones, 'id':r.ParcelasBosqueNatural.id}
        rows.append(cell)
    return dict(parcelas = [rows,headers])

@auth.requires_membership('digitador')
def parcelaBosquePlantado():
    """
    Página que permite el ingreso de datos de los árboles de una parcela de bosque plantado
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            form = SQLFORM(db.ParcelasBosquePlantado, showid = False, fields = ['numArbol','dap1','dap2','distancia','direccionRumbo','ht','hc','hPoda','forma','espesorCorteza', 'observaciones'], submit_button='Guardar')
            form.vars.muestreo = session.muestreoId
            if request.get_vars['c']:
                if int(request.get_vars['c']) == 1:
                    session.BosquePlantadoCont = 1
                    session.BosquePlantadoR = 6
                    form.vars.radio = 6
                elif int(request.get_vars['c']) == 2:
                    session.BosquePlantadoCont = 2
                    session.BosquePlantadoR = 10
                    form.vars.radio = 10
                elif int(request.get_vars['c']) == 3:
                    session.BosquePlantadoCont = 3
                    session.BosquePlantadoR = 14
                    form.vars.radio = 14
                elif int(request.get_vars['c']) == 4:
                    session.BosquePlantadoCont = 4
                    session.BosquePlantadoR = 18
                    form.vars.radio = 18
            else:
                session.BosquePlantadoCont = 1
                form.vars.radio = 6
            if form.accepts(request.vars, session, onvalidation=_checkHeights):
                session.muestreoPorcentaje = returnPercentage()
                response.flash = T("Successfully saved")
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                if int(request.get_vars['c']) > 4:
                    redirect(URL("index"))
                else:
                    response.flash = T("Fill in the data of the trees")
            return dict(form=form,cont = session.BosquePlantadoCont+1, radio=str(form.vars.radio), menuL = sideMenu(), selected=19 + session.BosquePlantadoCont)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def _checkHeights(form):
    """
    Método que verifica las restricciones de los árboles a ingresar en las parcelas de bosque plantado
    """
    rows = db(db.ParcelasBosquePlantado.muestreo == session.muestreoId)(db.ParcelasBosquePlantado.radio != form.vars.radio).select()
    error = False
    for row in rows:
        if form.vars.numArbol == row.numArbol:
            error = True
    if error:
        form.errors.numArbol = T("Trees can not be duplicates of other trees in other radios")
    if form.vars.hc > form.vars.ht:
        form.errors.hc = T("This height can not exceed the total height of the tree")
    if form.vars.hPoda > form.vars.ht:
        form.errors.hPoda = T("This height can not exceed the total height of the tree")
    dap = (form.vars.dap1 + form.vars.dap2) / 2.0
    if form.vars.radio == 6:
        if form.vars.ht < 1.30:
            form.errors.ht = T("This tree is to small to be measured")
        if dap >= 0.10:
            form.errors.dap1 = T("The average diameter of this tree has to be smaller than 0.10 m")
            form.errors.dap2 = T("The average diameter of this tree has to be smaller than 0.10 m")
    if form.vars.radio == 10:
        if dap < 0.10 or dap >= 0.25:
            form.errors.dap1 = T("The average diameter of this tree has to be between 0.10 and 0.25 m")
            form.errors.dap2 = T("The average diameter of this tree has to be between 0.10 and 0.25 m")
    if form.vars.radio == 14:
        if dap < 0.25 or dap >= 0.35:
            form.errors.dap1 = T("The average diameter of this tree has to be between 0.25 and 0.35 m")
            form.errors.dap2 = T("The average diameter of this tree has to be between 0.25 and 0.35 m")
    if form.vars.radio == 18:
        if dap < 0.35:
            form.errors.dap1 = T("The average diameter of this tree has to be greater than 0.35 m")
            form.errors.dap2 = T("The average diameter of this tree has to be greater than 0.35 m")

def tableParcelaBosquePlantado():
    rows = []
    headers = ['Arbol', 'DAP1', 'DAP2', 'Distancia', 'Rumbo', 'HC', 'HT', 'HPoda', 'Forma', 'Espesor Corteza', 'Observaciones', 'Acciones']
    parcelas = db(db.ParcelasBosquePlantado.muestreo==session.muestreoId)(db.ParcelasBosquePlantado.forma == db.TipoForma.id)(db.ParcelasBosquePlantado.radio == session.BosquePlantadoR).select()
    for r in parcelas:
        cell = {'arb':r.ParcelasBosquePlantado.numArbol,
                'dap1':r.ParcelasBosquePlantado.dap1,
                'dap2':r.ParcelasBosquePlantado.dap2,
                'dist':r.ParcelasBosquePlantado.distancia,
                'rum':r.ParcelasBosquePlantado.direccionRumbo,
                'hc':r.ParcelasBosquePlantado.hc,
                'ht':r.ParcelasBosquePlantado.ht,
                'hp':r.ParcelasBosquePlantado.hPoda,
                'tipo':r.TipoForma.tipo,
                'esp':r.ParcelasBosquePlantado.espesorCorteza,
                'obs':r.ParcelasBosquePlantado.observaciones,
                'id':r.ParcelasBosquePlantado.id}
        rows.append(cell)
    return dict(arboles = [rows,headers])


@auth.requires_membership('digitador')
def delete():
    """Borra datos de campo y tabla
    """
    table = request.get_vars['table']
    field = request.get_vars['field']
    val = request.get_vars['val']
    db( db[table][field] == val ).delete()


@auth.requires_membership('digitador')
def deleteFotos():
    """Borra datos y archivos de fotos
    """
    import os
    table = "Fotos"
    field = request.get_vars['field']
    val = request.get_vars['val']
    # Get filenames
    toDel = db(
        db[table][field] == val
    ).select(
        db[table]['foto']
    )
    fNames=[]
    for r in toDel:
        fNames.append( r['foto'] )
    # Delete record
    db( db[table][field] == val ).delete()
    # Delete files
    basePath = os.path.join(request.env.web2py_path,
                "applications", request.application, "uploads")
    for f in fNames:
        os.unlink( os.path.join(basePath, "images", f)  )
        os.unlink( os.path.join(basePath, "images", "thumbs", f)  )
        os.unlink( os.path.join(basePath, "images", "optim", f)  )


@auth.requires_membership('digitador')
def fotos():
    """
    Página que permite el ingreso de fotos del punto muestral
    """
    try:
        optSample = request.env['http_referer'].split("?")
        optSampleId = optSample[1].split("=")[1]
    except:
        optSampleId = -1
    if __hasPermission(request.get_vars["m"]) or __hasPermission(optSampleId):
        checkNewRepSel()
        if __hasGeneralData(session.muestreoId):
            form = SQLFORM(
                db.Fotos,
                showid = False,
                fields = ['tipoFoto', 'descr', 'lat', 'lon'],
                submit_button='Guardar',
                upload=URL('download')
            )
            uploader = TR(
                TD(
                    DIV(
                        LABEL('Foto:')
                    ),
                    _class="w2p_fl"
                ),
                TD(
                    DIV(_id="fineUploader"),
                    _class="w2p_fw",
                    _colspan=2
                ),
                TD(_class="w2p_fc"),
                _id="Fotos_foto__row"
            )
            form[0].insert(4, uploader)
            form.vars.muestreo = session.muestreoId
            if request.vars.foto != None:
                if request.vars.foto != "":
                    form.vars.foto = request.vars.foto
            if form.accepts(request.vars, session, onvalidation=hasImage):
                response.flash = T("Successfully saved")
                session.muestreoPorcentaje = returnPercentage()
                redirect(URL('fotos', vars=dict(m=session.muestreoId)))
            elif form.errors:
                response.flash = T("There are errors. Please correct them")
            else:
                response.flash = T("Fill in with the fotos")
            return dict(form=form, fotos = fotos, menuL = sideMenu(), selected=3)
        else:
            redirect(URL('datosGenerales', vars=dict(m=session.muestreoId)))
    else:
        redirect(URL('index'))


def hasImage(form):
    """
    Validación del formulario para que se ingrese una imagen
    """
    if form.vars.foto == None:
        form.errors.descr = T("You have to select a photo")


@auth.requires_membership('digitador')
def tableFoto():
    muestreo = request.get_vars['m']
    rows = []
    headers = [
        'Tipo de Foto',
        'Descripcion',
        'Latitud',
        'Longitud',
        'Acciones'
    ]
    fotos = db(
        (db.Fotos.muestreo==muestreo) &
        (db.Fotos.tipoFoto==db.TipoFoto.id)
    ).select()
    for r in fotos:
        cell = {
            'tipoFoto':r.TipoFoto.tipo,
            'descr':r.Fotos.descr,
            'foto':r.Fotos.foto,
            'lat':r.Fotos.lat,
            'lon':r.Fotos.lon,
            'id':r.Fotos.id
        }
        rows.append(cell)
    return dict(fotos = [rows,headers],muestreo=muestreo)


@auth.requires_membership('digitador')
def saveImage():
    """
    Método utilizado para guardar la imagen en disco
    """
    import qqfileuploader as fu
    allowedExtension = [".jpg",'.gif','.png']
    sizeLimit = 6144000
    uploader = fu.qqFileUploader(request, allowedExtension, sizeLimit)
    return uploader.handleUpload()


@auth.requires_membership('digitador')
def processImage():
    """
    Método que busca en los datos EXIF de la imagen para encontrar si cuenta con datos geográficos
    """
    import os
    fileName = ''
    import gluon.contrib.simplejson
    if request.get_vars['fileName']:
        fileName = request.get_vars['fileName']
    if fileName != '':
        from applications.lifn import EXIF
        # curDir = request.folder
        f = open( os.path.join(request.folder, 'uploads', "images", fileName), 'rb')
        tags = EXIF.process_file(f)
        if tags != {}:
            try:
                if not tags['GPS GPSLatitude'] or not tags['GPS GPSLongitude'] or not tags['GPS GPSLatitudeRef'] or not tags['GPS GPSLongitudeRef']:
                    return gluon.contrib.simplejson.dumps({'res': 'None',})
                else:
                    lat_dms = tags['GPS GPSLatitude'].values
                    lon_dms = tags['GPS GPSLongitude'].values
                    latitude = DmsToDecimal(
                        lat_dms[0].num, lat_dms[0].den,
                        lat_dms[1].num, lat_dms[1].den,
                        lat_dms[2].num, lat_dms[2].den
                    )
                    longitude = DmsToDecimal(
                        lon_dms[0].num, lon_dms[0].den,
                        lon_dms[1].num, lon_dms[1].den,
                        lon_dms[2].num, lon_dms[2].den
                    )
                    if tags['GPS GPSLatitudeRef'].printable == 'S': latitude *= -1
                    if tags['GPS GPSLongitudeRef'].printable == 'W': longitude *= -1
                    return gluon.contrib.simplejson.dumps({'res': 'Foto', 'lat':latitude, 'lon':longitude})
            except:
                return gluon.contrib.simplejson.dumps({'res': 'None',})
        else:
            return gluon.contrib.simplejson.dumps({'res': 'None',})
    else:
        return gluon.contrib.simplejson.dumps({'res': 'None',})


def DmsToDecimal(degree_num, degree_den, minute_num, minute_den,
                 second_num, second_den):
    """
    Método que convierte los grados en decimales
    """
    degree = float(degree_num)/float(degree_den)
    minute = float(minute_num)/float(minute_den)/60
    second = float(second_num)/float(second_den)/3600
    return degree + minute + second


@auth.requires_membership('administrador')
def sendData():
    """
    Página que permite el envío de los puntos muestrales completados para su ingreso en el sistema de la DGF
    """
    session.menuL_enabled = False
    session.show_title = False
    opts = []
    optsAll = []
    rows = db(db.MuestreoUsuario.id > 0).select()
    for row in rows:
        if checkIfFinished(row.muestreo):
            idMuestreo = db(db.Muestreo.punto == db.Punto.id)(db.Muestreo.id == row.muestreo)(db.MuestreoUsuario.muestreo == db.Muestreo.id)(db.MuestreoTipoReporte.muestreo == db.MuestreoUsuario.muestreo)(db.MuestreoTipoReporte.tipo == db.TipoReporte.id).select().first()
            aux = "%s | %s" % (idMuestreo.Punto.nombre, idMuestreo.TipoReporte.tipo)
            opts.append(OPTION(aux, _value=idMuestreo.Muestreo.id))
    form = FORM(TABLE(
                        TR (
                            TD(
                                LABEL("Muestreos Terminados:",_class = "table-th")
                            ),
                            TD(""),
                            TD(
                                LABEL("Muestreos para Enviar:", _class = "table-th")
                            )
                        ),
                        TR (
                            TD(
                                DIV(
                                    SELECT(opts, _name='todos', _id='todos', _multiple= "multiple", _size = "10"),
                                    _id="formTodos",
                                    _style = "display: inline-block; margin-top: -10px;"
                                )
                            ),
                            TD(
                                DIV(
                                    DIV(
                                        INPUT(_type = "button", _name = "selectAll", _value = ">>")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "selectOneOrMultiple", _value = "=>")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "deselectOneOrMultiple", _value = "<=")
                                    ),
                                    DIV(
                                        INPUT(_type = "button", _name = "deselectAll", _value = "<<")
                                    ),
                                    _id="buttons",
                                    _style="float:left; margin-top: 10px;"
                                )
                            ),
                            TD(DIV(SELECT(optsAll, _name='asignados', _id='asignados', _multiple= "multiple", _size = "10"), _id="formAsignados", _style = "display: inline-block; margin-top: -10px;"))
                        ),
                        TR (
                            TD(
                                DIV(
                                    LABEL("Internet", _style="display: inline;"),
                                    INPUT(_type='radio', _name='radio', value='yes', _value='yes', _disabled='disabled'),
                                    LABEL("Magnetico", _style="display: inline;"),
                                    INPUT(_type='radio', _name='radio', value='yes', _value='yes'),
                                ),
                                _colspan=3,
                                _style="float: right;"
                            )
                        ),
                        TR (
                            TD(
                                DIV(
                                    INPUT(_type="button",_value="Exportar a .zip", _id = "accept", _disabled="disabled"),
                                    _style="float: right;"
                                ),
                                _colspan=3
                            )
                        ), _style="margin-left: auto; margin-right: auto;"
                    )
                )
    if form.accepts(request, session, keepvalues=True):
        response.flash = request
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = "Seleccione los muestreos"
    return dict(form=form)

def sendOverInternet():
    """
    Método a realizar
    """
    pass

def datosZip():
    """
    Método que devuelve el archivo comprimido con los datos de los puntos muestrales seleccionados
    """
    muestreos = ( str(request.get_vars['m']) ).split(',')
    for muestreo in muestreos:
        evento = db(db.TipoAccion.tipo == "Muestreo enviado").select().first().id
        aux = db(db.EventosAsignacion.muestreo == muestreo)(db.EventosAsignacion.accion == evento).select().first()
        if aux == None:
            import datetime
            db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = auth.user.id, accion = evento, muestreo = muestreo)
        else:
            evento = db(db.TipoAccion.tipo == "Muestreo reenviado").select().first().id
            import datetime
            db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = auth.user.id, accion = evento, muestreo = muestreo)
    from gluon.contenttype import contenttype
    import datetime, os
    sTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    __exportZip(muestreos, sTime)
    admin = db(
        (db.auth_user.id == db.auth_membership.user_id) &
        (db.auth_membership.group_id == db.auth_group.id) &
        (db.auth_group.role == "administrador")
    ).select().first()
    filename= sTime + "_" + admin.auth_user.last_name + "_" + admin.auth_user.first_name + ".zip"
    response.headers['Content-Disposition']='attachment; filename='+filename
    response.headers['Content-Type'] = contenttype('.zip')
    return response.stream(request.folder+ os.sep + 'backup'+ os.sep+sTime+'.zip', chunk_size=64*1024)


def __exportZip(muestreos, filename):
    """
    Método interno que genera el archivo comprimido con los datos de los puntos muestrales seleccionados
    """
    import os
    import zipfile
    import shutil

    oldDir = os.getcwd()
    curDir = request.folder
    bacDir = os.path.join(request.folder, "backup")
    expDir = os.path.join(request.folder, "export")
    if not os.path.exists(bacDir):
        os.makedirs(bacDir)
    if not os.path.exists(expDir):
        os.makedirs(expDir)
    zf=""
    try:
        # Set current dir. Path are relatives!
        os.chdir(curDir)
        uploads = []
        # Generate types and muestreos XML (export/filename/datosDB.xml)
        typesToXML(muestreos,filename)
        for m in muestreos:
            zf = zipfile.ZipFile( os.path.join(bacDir, "%s.zip" % filename), mode='w')
            # Generate info XML for this muestreo (export/filename/NombreDelPunto/XXXXXXX.xml)
            muestreoToXML(m,filename)
            # Copy gpxs and images to folder
            # Get path of gpx and image to copy
            uploads = fileNamesInFolder( os.path.join(curDir, 'uploads'), m )
            # Get nombre
            punto = db(
                (db.Muestreo.id == m) &
                (db.Muestreo.punto == db.Punto.id)
            ).select().first()
            nombre = punto.Punto.nombre
            for fp in uploads:
                # Copy file to directory
                shutil.copy(
                    fp,
                    os.path.join(curDir, 'export', filename, nombre, '')
                )
        parent_folder = 'export'
        contents = os.walk('export' + os.sep + filename)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zf.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zf.write(absolute_path, relative_path)
    finally:
        os.chdir(oldDir)
        if zf != "":
            zf.close()

def copyUpload(src, dst):
    """
    Método para copiar ficheros en el sistema de archivos
    """
    import shutil, errno
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        shutil.copy(src, dst)
        """if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise"""

def fileNamesInFolder(basePath, muestreoId):
    """
    Método que devuelve los nombres de los archivos en el directorio pasado por parámetro
    """
    import os
    fileNames = []
    fotos = []
    tracks = []
    ## TODO: (RFPV) Vulnerable for changes in images path and track path
    imaPath = os.path.join(basePath, "images")
    gpxPath = os.path.join(basePath, "gpx")
    # Get tracks
    dbtracks = db(db.Distancias.muestreo == muestreoId).select()
    for row in dbtracks:
        track = row.track
        fp = os.path.join(gpxPath,track)
        if os.path.exists(fp):
            tracks.append(fp)
        else:
            ## TODO: (RFPV) Send warning!
            pass
    # Get fotos
    dbfotos = db(db.Fotos.muestreo == muestreoId).select()
    for row in dbfotos:
        foto = row.foto
        fp = os.path.join(imaPath,foto)
        if os.path.exists(fp):
            tracks.append(fp)
        else:
            ## TODO: (RFPV) Send warning!
            pass
    return fotos + tracks

def returnPercentage():
    """
    Método que retorna el porcentaje de completado del punto muestral, calculado a partir de los campos completados sobre el número total de camplos
    """
    muestreo = request.get_vars['m']
    percentage = completedPercentage(muestreo)
    if percentage > 0 and percentage <= 100:
        accionAsignar = db(
            (db.TipoAccion.tipo == 'Muestreo comenzado')
        ).select().first().id
        yaAgregado = db(
            (db.EventosAsignacion.muestreo == muestreo) &
            (db.EventosAsignacion.accion == accionAsignar)
        ).select().first()
        if yaAgregado == None:
            import datetime
            db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = auth.user.id, accion = accionAsignar, muestreo = muestreo)
    if percentage == 100:
        accionAsignar = db(db.TipoAccion.tipo == "Muestreo completado").select().first().id
        yaAgregado = db(db.EventosAsignacion.muestreo == muestreo)(db.EventosAsignacion.accion == accionAsignar).select().first()
        if yaAgregado == None:
            import datetime
            db.EventosAsignacion.insert(fecha = datetime.datetime.now(), usuario = auth.user.id, accion = accionAsignar, muestreo = muestreo)
    return str(percentage)

def sampleName():
    """
    Método que retorna el nombre del muestreo para ser mostrado
    """
    muestreo = request.get_vars['m']
    mRow = db(
        (db.Muestreo.id == muestreo) &
        (db.Punto.id == db.Muestreo.punto)
    ).select().first()
    if mRow != None:
        return mRow.Punto.nombre
    else:
        return "Error"


# ToDo
def completedPercentage(muestreo):
    """
    Método que calcula el porcentaje de completado del punto muestral, calculado a partir de los campos completados sobre el número total de camplos
    """
    plant = db(
        (db.DatosGenerales.muestreo == muestreo)
    ).select().first()
    idPlant = db(
        (db.TipoBosque.tipo == "Plantación")
    ).select().first()
    idEuca = db(
        (db.TipoGenero.genero == "Eucalyptus")
    ).select().first().id
    idPinus = db(
        (db.TipoGenero.genero == "Pinus")
    ).select().first().id
    statusM = db(
        (db.MuestreoTipoReporte.muestreo == muestreo) &
        (db.MuestreoTipoReporte.tipo == db.TipoReporte.id)
    ).select().first()
    tieneDatos = db(
        (db.TieneDatos.muestreo == muestreo)
    ).select(db.TieneDatos.ALL).first()
    if statusM == None:
        return 0
    else:
        if statusM.TipoReporte.id == CON_INFORMACION:
            if plant != None:
                totalFields = 0
                fieldsCompleted = 0
                import re
                tableNames = [
                    "^auth",
                    "^Tipo",
                    "^SubTipo",
                    "Punto",
                    "^Muestreo",
                    "NombreAfluentes",
                    "EventosAsignacion",
                    "EspeciesInvasoras",
                    "Informacion",
                    "Version",
                    "Observaciones",
                    "TieneDatos"
                ]
                if not tieneDatos.tieneAgua:
                    tableNames.append('Agua');
                if not tieneDatos.tieneFauna:
                    tableNames.append('Fauna');
                if not tieneDatos.tieneFlora:
                    tableNames.append('Flora');
                if not tieneDatos.tieneEspeciesInvasoras:
                    tableNames.append('EspeciesInvasoras');
                plantTables = [
                    "Plantacion",
                    "ForestacionMantenimientoEstructura",
                    "ProductosNoMadereros",
                    "EnfermedadesEucalyptus",
                    "EnfermedadesPino",
                    "ParcelasBosquePlantado",
                    "Especie"
                ]
                bNTables =["Especie","ParcelasBosqueNatural"]
                if int(plant.tipoDeBosque) == int(idPlant.id):
                    # Plantacion
                    rowP = db(db.Plantacion.muestreo == muestreo).select().first()
                    generoPlant = -1
                    if rowP != None:
                        generoPlant = rowP.genero
                    if generoPlant == idEuca:
                        bNTables.append("EnfermedadesPino")
                    elif generoPlant == idPinus:
                        bNTables.append("EnfermedadesEucalyptus")
                    else:
                        bNTables.append("EnfermedadesPino")
                        bNTables.append("EnfermedadesEucalyptus")
                    tableNames.extend(bNTables)
                    pattern = ""
                    for name in tableNames:
                        pattern += name + "|"
                    pattern = pattern[:-1]
                    prog = re.compile(pattern)
                    for table_name in db.tables():
                        if prog.match(table_name) == None:
                            table = db[table_name]
                            name = table_name.__str__()
                            row = db(table.muestreo == muestreo).select().first()
                            fields = table.fields()
                            for field in fields:
                                if not "id" == field:
                                    totalFields = totalFields + 1
                                    if row != None:
                                        if row[field] != None:
                                            fieldsCompleted = fieldsCompleted + 1
                                    #else:
                                        #print field.__str__()
                else:
                    # Bosque Nativo
                    tableNames.extend(plantTables)
                    pattern = ""
                    for name in tableNames:
                        pattern += name + "|"
                    pattern = pattern[:-1]
                    prog = re.compile(pattern)
                    for table_name in db.tables():
                        if prog.match(table_name) == None:
                            table = db[table_name]
                            name = table_name.__str__()
                            row = db(table.muestreo == muestreo).select().first()
                            fields = table.fields()
                            for field in fields:
                                if not "id" == field:
                                    totalFields = totalFields + 1
                                    if row != None:
                                        if row[field] != None:
                                            fieldsCompleted = fieldsCompleted + 1
                                    #else:
                                        #print field.__str__()
                percentage = int((float(fieldsCompleted)/float(totalFields))*100)
                rowMU = db(db.MuestreoUsuario.muestreo == muestreo).select().first()
                if rowMU != None:
                    if percentage == 100:
                        if not rowMU.realizado:
                            rowMU.update_record(realizado=True)
                    else:
                        if rowMU.realizado:
                            rowMU.update_record(realizado=False)
                if percentage >= 98:
                    percentage = 100
                return percentage
            else:
                rowMU = db(db.MuestreoUsuario.muestreo == muestreo).select().first()
                if rowMU != None:
                    if rowMU.realizado:
                        rowMU.update_record(realizado=False)
                return 0
        else:
            rowMU = db(db.MuestreoUsuario.muestreo == muestreo).select().first()
            if rowMU != None:
                if not rowMU.realizado:
                    rowMU.update_record(realizado=True)
            return 100

def missingFields():
    muestreo = request.get_vars['m']
    plant = db(db.DatosGenerales.muestreo == muestreo).select().first()
    idPlant = db(db.TipoBosque.tipo == "Plantación").select().first()
    idEuca = db(db.TipoGenero.genero == "Eucalyptus").select().first().id
    idPinus = db(db.TipoGenero.genero == "Pinus").select().first().id
    statusM = db(db.MuestreoTipoReporte.muestreo == muestreo)(db.MuestreoTipoReporte.tipo == db.TipoReporte.id).select().first()
    tieneDatos = db(db.TieneDatos.muestreo == muestreo).select(db.TieneDatos.ALL).first()
    import re
    notCompletedFields = []
    notCompletedTables = []
    tableNames = ["^auth","^Tipo","^SubTipo","Punto","^Muestreo","NombreAfluentes", "EventosAsignacion", "FloraDelSuelo", "EspeciesInvasoras", "Informacion","Version","Observaciones"]
    if tieneDatos:
        if not tieneDatos.tieneAgua:
            tableNames.append('Agua');
        if not tieneDatos.tieneFauna:
            tableNames.append('Fauna');
        if not tieneDatos.tieneEspeciesInvasoras:
            tableNames.append('EspeciesInvasoras');
        if not tieneDatos.tieneFlora:
            tableNames.append('Flora');
    plantTables = ["Plantacion","ForestacionMantenimientoEstructura","ProductosNoMadereros","ParcelasBosquePlantado","Especie"]
    bNTables =["Especie","ParcelasBosqueNatural"]
    if int(plant.tipoDeBosque) == int(idPlant.id):
        # Plantacion
        rowP = db(db.Plantacion.muestreo == muestreo).select().first()
        generoPlant = -1
        if rowP != None:
            generoPlant = rowP.genero
        if generoPlant == idEuca:
            bNTables.append("EnfermedadesPino")
        elif generoPlant == idPinus:
            bNTables.append("EnfermedadesEucalyptus")
        else:
            bNTables.append("EnfermedadesEucalyptus")
            bNTables.append("EnfermedadesPino")
        tableNames.extend(bNTables)
        pattern = ""
        for name in tableNames:
            pattern += name + "|"
        pattern = pattern[:-1]
        prog = re.compile(pattern)
        for table_name in db.tables():
            if prog.match(table_name) == None:
                table = db[table_name]
                name = table_name.__str__()
                row = db(table.muestreo == muestreo).select().first()
                fields = table.fields()
                if row != None:
                    for field in fields:
                        if not "id" == field:
                            if row[field] == None:
                                notCompletedFields.append({'tabla':name, 'campo':field.__str__()})
                else:
                    notCompletedTables.append(name)
    else:
        # Bosque Nativo
        tableNames.extend(plantTables)
        pattern = ""
        for name in tableNames:
            pattern += name + "|"
        pattern = pattern[:-1]
        prog = re.compile(pattern)
        for table_name in db.tables():
            if prog.match(table_name) == None:
                table = db[table_name]
                name = table_name.__str__()
                row = db(table.muestreo == muestreo).select().first()
                fields = table.fields()
                if row != None:
                    for field in fields:
                        if not "id" == field:
                            if row[field] == None:
                                notCompletedFields.append({'tabla':name, 'campo':field.__str__()})
                else:
                    notCompletedTables.append(name)
    return dict(array = [notCompletedTables, notCompletedFields])


def checkIfFinished(muestreo):
    """
    Método que verifica si un muestreo está completado
    """
    plant = db(db.DatosGenerales.muestreo == muestreo).select().first()
    idPlant = db(db.TipoBosque.tipo == "Plantación").select().first()
    idEuca = db(db.TipoGenero.genero == "Eucalyptus").select().first().id
    idPinus = db(db.TipoGenero.genero == "Pinus").select().first().id
    statusM = db(db.MuestreoTipoReporte.muestreo == muestreo)(db.MuestreoTipoReporte.tipo == db.TipoReporte.id).select().first()
    if statusM == None:
        return False
    else:
        if statusM.TipoReporte.id == CON_INFORMACION:
            if plant != None:
                import re
                tableNames = [
                    "^auth",
                    "^Tipo",
                    "^SubTipo",
                    "Punto",
                    "^Muestreo",
                    "NombreAfluentes",
                    "EventosAsignacion",
                    "FloraDelSuelo",
                    "Flora",
                    "EspeciesInvasoras",
                    "Informacion",
                    "Version",
                    "Observaciones",
                    "Agua",
                    "Fauna",
                    "EspeciesInvasoras",
                    "TieneDatos"
                ]
                plantTables = [
                    "Plantacion",
                    "ForestacionMantenimientoEstructura",
                    "ProductosNoMadereros",
                    "EnfermedadesEucalyptus",
                    "EnfermedadesPino",
                    "ParcelasBosquePlantado",
                    "Especie"
                ]
                bNTables =["Especie","ParcelasBosqueNatural"]
                if int(plant.tipoDeBosque) == int(idPlant.id):
                    # Plantacion
                    rowP = db(db.Plantacion.muestreo == muestreo).select().first()
                    generoPlant = -1
                    if rowP != None:
                        generoPlant = rowP.genero
                    if generoPlant == idEuca:
                        bNTables.append("EnfermedadesPino")
                    elif generoPlant == idPinus:
                        bNTables.append("EnfermedadesEucalyptus")
                    else:
                        bNTables.append("EnfermedadesPino")
                        bNTables.append("EnfermedadesEucalyptus")
                    tableNames.extend(bNTables)
                    pattern = ""
                    for name in tableNames:
                        pattern += name + "|"
                    pattern = pattern[:-1]
                    prog = re.compile(pattern)
                    tables = db.tables()
                    for table_name in tables:
                        if prog.match(table_name) == None:
                            table = db[table_name]
                            row = db(table.muestreo == muestreo).select().first()
                            if row == None:
                                return False
                else:
                    # Bosque Nativo
                    tableNames.extend(plantTables)
                    pattern = ""
                    for name in tableNames:
                        pattern += name + "|"
                    pattern = pattern[:-1]
                    prog = re.compile(pattern)
                    tables = db.tables()
                    for table_name in tables:
                        if prog.match(table_name) == None:
                            table = db[table_name]
                            row = db(table.muestreo == muestreo).select().first()
                            if row == None:
                                return False
                return True
            else:
                return False
        else:
            return True



def muestreoToXML(muestreo, filename):
    """
    Metodo que genera un XML con la informacion asociada al muestreo pasado por parametro
    """
    from xml.etree.ElementTree import Element, ElementTree, SubElement
    import os
    import re
    xml = Element('xml')
    pattern = ""
    tableNames = [
        "^auth",
        "^Tipo",
        "^SubTipo",
        "MuestreoUsuario$",
        "EventosAsignacion",
        "Informacion",
        "TieneDatos"
    ]
    for name in tableNames:
        pattern += name + "|"
    pattern = pattern[:-1]
    prog = re.compile(pattern)
    idHasData = db(
        ( db.TipoReporte.id == CON_INFORMACION )
    ).select().first()
    sampleHasData = db(
        ( db.MuestreoTipoReporte.muestreo == int(muestreo) ) &
        ( db.MuestreoTipoReporte.tipo == int(idHasData.id) )
    ).select().first()

    if sampleHasData != None:
        for table_name in db.tables():
            if table_name != "Version":
                if prog.match(table_name) == None:
                    if table_name != "Punto" and table_name != "Muestreo":
                        table = db[table_name]
                        tableTag = SubElement(xml, 'table', name=table.__str__())
                        rows = db(table.muestreo == int(muestreo)).select()
                        #print table_name
                        for row in rows:
                            fields = table.fields()
                            rowTag = SubElement(tableTag, 'row')
                            for field in fields:
                                if "id" == field:
                                    rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                                else:
                                    fieldTag = SubElement(rowTag, field.__str__())
                                    text = unicode(sanitizier(str(row[field])), 'utf8')
                                    fieldTag.text = text
                    else:
                        if table_name == "Punto":
                            table = db[table_name]
                            tableTag = SubElement(xml, 'table', name=table.__str__())
                            rows = db(table.id == db.Muestreo.punto)(db.Muestreo.id == int(muestreo)).select(db.Punto.ALL)
                            for row in rows:
                                fields = table.fields()
                                rowTag = SubElement(tableTag, 'row')
                                for field in fields:
                                    if "id" == field:
                                        rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                                    else:
                                        fieldTag = SubElement(rowTag, field.__str__())
                                        text = unicode(sanitizier(str(row[field])), 'utf8')
                                        fieldTag.text = text
                        elif table_name == "Muestreo":
                            table = db[table_name]
                            tableTag = SubElement(xml, 'table', name=table.__str__())
                            rows = db(db.Muestreo.id == int(muestreo)).select()
                            for row in rows:
                                fields = table.fields()
                                rowTag = SubElement(tableTag, 'row')
                                for field in fields:
                                    if "id" == field:
                                        rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                                    else:
                                        fieldTag = SubElement(rowTag, field.__str__())
                                        text = unicode(sanitizier(str(row[field])), 'utf8')
                                        fieldTag.text = text
    else:
        table = db.MuestreoTipoReporte
        tableTag = SubElement(xml, 'table', name=table.__str__())
        rows = db(table.muestreo == int(muestreo)).select()
        for row in rows:
            fields = table.fields()
            rowTag = SubElement(tableTag, 'row')
            for field in fields:
                if "id" == field:
                    rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                else:
                    fieldTag = SubElement(rowTag, field.__str__())
                    text = unicode(sanitizier(str(row[field])), 'utf8')
                    fieldTag.text = text
    curDir = request.folder
    row = db(db.Muestreo.id == muestreo)(db.Muestreo.punto == db.Punto.id).select().first()
    rowEmpresa = db(db.Informacion.id > 0).select().first()
    if rowEmpresa != None:
        empTag = SubElement(xml, "empresa")
        empTag.text = rowEmpresa.empresa
    if row != None:
        yearTag = SubElement(xml, "anio")
        yearTag.text = str(row.Muestreo.anioMuestreo)

    outDir = os.path.join(request.folder, "export", filename, row.Punto.nombre, '')
    outFile = os.path.join(outDir, "muestreo.xml")
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    else:
        ## TODO: (RFPV) Directory must be cleaned????
        pass
    f = open(outFile, 'a')
    ElementTree(xml).write(f)

def typesToXML(muestreos,filename):
    """
    Metodo que genera un XML con:
        * tipos de datos que se encuentran en la base de datos;
        * muestreos.
    Los guarda en export/filename/datosDB.xml
    """
    import os
    from xml.etree.ElementTree import Element, ElementTree, SubElement, Comment, tostring
    xml = Element('xml')
    for table_name in db.tables():
        ## TODO: (RFPV) Optimize code
        if ((table_name.__str__().startswith("Tipo")) or ("Punto" in table_name.__str__())):
            table = db[table_name]
            tableTag = SubElement(xml, 'table', name=table.__str__())
            rows = db(table.id > 0).select()
            fields = table.fields()
            for row in rows:
                rowTag = SubElement(tableTag, 'row')
                for field in fields:
                    if "id" == field:
                        rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                    else:
                        fieldTag = SubElement(rowTag, field.__str__())
                        text = unicode(sanitizier(str(row[field])), 'utf8')
                        fieldTag.text = text
        elif "Muestreo" == table_name.__str__():
            table = db[table_name]
            tableTag = SubElement(xml, 'table', name=table.__str__())
            rows = db(
                db.Muestreo.id.belongs(muestreos)
            ).select()
            fields = table.fields()
            for row in rows:
                rowTag = SubElement(tableTag, 'row')
                for field in fields:
                    if "id" == field:
                        rowTag.attrib['id'] =  unicode(sanitizier(str(row[field])), 'utf8')
                    else:
                        fieldTag = SubElement(rowTag, field.__str__())
                        text = unicode(sanitizier(str(row[field])), 'utf8')
                        fieldTag.text = text
    # Prepare and write the file
    outDir = os.path.join(request.folder, "export", filename, '')
    outFile = os.path.join(outDir, "datosDB.xml")
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    else:
        ## TODO: (RFPV) Directory must be cleaned????
        pass
    f = open(outFile, 'w')
    ElementTree(xml).write(f)


def call():
    return service()

def sanitizier(text):
    """
    Método que convierte cadenas de caracteres ilegales a su versión sin caracteres ilegales
    """
    newText = text
    if "<" in text:
        newText = text.replace("<", "&lt")
        return str(newText)
    elif ">" in text:
        newText = text.replace(">", "&gt")
        return str(newText)
    elif "&" in text:
        newText = text.replace("&", "&amp")
        return str(newText)
    elif "'" in text:
        newText = text.replace("'", "&apos")
        return str(newText)
    elif "\"" in text:
        newText = text.replace("\"", "&quot")
        return str(newText)
    return newText

@auth.requires_membership('administrador')
def loadNewSamples():
    """
    Página que permite el ingreso de nuevos puntos muestrales al sistema
    """
    session.show_title = False
    session.menuL_enabled = False
    html = TABLE(
        TR(
            TD( DIV(_id="file-uploader") )
        ),
        TR(
            TD( INPUT(_type="submit",_value=T("Save"), _class="custom-submit"), _id="submit_record__row" ),
            _style="height: 60px;"
        )
    )
    form = FORM( html )
    if form.validate():
        #print "loadNewSamples=%s" % session.uploadFile
        if not checkXMLHasUpdates(session.uploadFile):
            loadXMLSamples(session.uploadFile)
            response.flash = T("Success!")
        else:
            redirect(URL('xmlHasUpdates'))
    elif form.errors:
        response.flash = T("Form has errors")
    else:
        response.flash = T("Load an XML file with the samples")
    return dict(form=form)

def processSamples():
    """
    Método que procesa los nuevos puntos muestrales a ingresar
    """
    import os
    fileName = ''
    if request.get_vars['fn']:
        fileName = request.get_vars['fn']
    if fileName != '':
        from xml.dom.minidom import parse
        try:
            curDir = request.folder
            dom = parse( os.path.join(request.folder, 'uploads', 'xml', fileName) )
            session.uploadFile = fileName
            puntos = dom.getElementsByTagName('puntos')[0].getElementsByTagName('punto')
            return "Se van a cargar %s puntos nuevos" % len(puntos)
        except Exception, e:
            print "processSamples=%s" % e

def saveSamples():
    """
    Método que guarda los nuevos puntos muestrales
    """
    import os
    try:
        import qqfileuploader as fu
        allowedExtension = [".xml"]
        sizeLimit = 6144000
        uploader = fu.qqFileUploader(request, allowedExtension, sizeLimit)
        return uploader.handleUpload()
    except Exception, e:
        print "saveSamples: Error: %s" % e


def copy(fp, folder='xml'):
    """
    Método que copia ficheros a la carpeta pasada por parámetro
    """
    import os

    try: # Windows needs stdio set for binary mode.
        import msvcrt
        msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
        msvcrt.setmode (1, os.O_BINARY) # stdout = 1
    except ImportError:
        pass
    # A nested FieldStorage instance holds the file
    fileitem = fp
    curDir = request.folder
    # Test if the file was uploaded
    filename = ""
    if fileitem.filename:

       # strip leading path from file name to avoid directory traversal attacks
       fn = os.path.basename(fileitem.filename)
       if not os.path.exists(curDir+folder+ os.sep):
                os.makedirs(curDir+folder+ os.sep)
       open(curDir + folder+ os.sep + fn, 'wb').write(fileitem.file.read())
       filename = fn
    return filename

@auth.requires_membership('administrador')
def checkXMLHasUpdates(xmlFileName):
    """
    Método que verifica si el XML contiene modificaciones sobre los puntos ingresados previamente
    """
    from xml.dom.minidom import parse
    try:
        hasUpdates = False
        import os
        curDir = request.folder
        dom = parse( os.path.join(request.folder, 'uploads', 'xml', xmlFileName) )

        puntos = dom.getElementsByTagName('puntos')[0].getElementsByTagName('punto')
        for punto in puntos:
            nombre = punto.getElementsByTagName('nombre')[0].childNodes[0].nodeValue
            latitud = punto.getElementsByTagName('lat')[0].childNodes[0].nodeValue
            longitud = punto.getElementsByTagName('lon')[0].childNodes[0].nodeValue
            rowPunto = db(db.Punto.nombre == nombre).select().first()
            if rowPunto != None:
                if (rowPunto.lat != float(latitud) or rowPunto.lon != float(longitud)):
                    hasUpdates = True
        return hasUpdates
    except Exception, e:
        print e

@auth.requires_membership('administrador')
def loadXMLSamples(xmlFileName):
    """
    Método que inserta los nuevos puntos muestrales en la base de datos
    """
    import os
    from xml.dom.minidom import parse
    try:
        curDir = request.folder
        dom = parse( os.path.join(request.folder, 'uploads', 'xml', xmlFileName) )
        empresa = dom.getElementsByTagName('empresa')[0].childNodes[0].nodeValue
        puntos = dom.getElementsByTagName('puntos')[0].getElementsByTagName('punto')
        #print "empresa=%s" % empresa

        for punto in puntos:
            muestreo = punto.getElementsByTagName('muestreo')[0].childNodes[0].nodeValue
            nombre = punto.getElementsByTagName('nombre')[0].childNodes[0].nodeValue
            latitud = punto.getElementsByTagName('lat')[0].childNodes[0].nodeValue
            longitud = punto.getElementsByTagName('lon')[0].childNodes[0].nodeValue
            anioMuestreo = punto.getElementsByTagName('anio')[0].childNodes[0].nodeValue
            idPunto = punto.getElementsByTagName('puntoid')[0].childNodes[0].nodeValue
            rowPunto = db(db.Punto.nombre == nombre).select().first()
            if rowPunto == None:
                db.Punto.insert(id=int(idPunto), lat=float(latitud), lon=float(longitud), nombre=nombre)
                db.Muestreo.insert(id=int(muestreo), punto=idPunto, anioMuestreo=anioMuestreo)
                db.TieneDatos.insert(muestreo = int(muestreo))
            else:
                rowPunto.update_record(lat=float(latitud), lon=float(longitud))
            rowInf = db(db.Informacion.empresa == empresa).select().first()
            if rowInf == None:
                db.Informacion.insert(empresa=empresa, admin=auth.user.first_name + " " + auth.user.last_name)
    except Exception, e:
        print "loadXMLSamples=%s" % e


@auth.requires_membership('administrador')
def xmlHasUpdates():
    """
    Método que valida si realmente se quieren sobreescribir los puntos muestrales, de los cuales se han encontrado que se modificarían
    """
    if request.post_vars['resp']:
        if request.post_vars['resp'] == '1':
            loadXMLSamples(session.pointsXMLFilename)
            redirect(URL('loadNewSamples'))
        else:
            redirect(URL('index'))
    else:
        return dict()

def kml():
    session.show_title = False
    rowPuntos = db(db.Muestreo.punto == db.Punto.id).select()
    if len(rowPuntos) > 0:
        exportKml()
        exported = True
    else:
        exported = False
    return dict(exported=exported)

def exportKml():
    """
    Método que genera un archivo KML que se puede abrir con el programa Google Earth que localiza los puntos muestrales y les asigna un color
    dependiendo de su estado (realizado o no realizado)
    """
    from simplekml import Kml, Style
    kml = Kml()
    kml.document.name = "Puntos Muestrales"
    redstyle = Style()
    redstyle.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
    redstyle.iconstyle.color = 'ff0000ff'
    greenstyle = Style()
    greenstyle.iconstyle.color = 'ff00ff00'
    greenstyle.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
    folRealizados = kml.newfolder(name='Realizados')
    folNoRealizados = kml.newfolder(name='No realizados')
    rowPuntos = db(db.Muestreo.punto == db.Punto.id).select()
    for row in rowPuntos:
        rowM = db(db.MuestreoTipoReporte.muestreo == row.Muestreo.id).select().first()
        if rowM != None:
            point = folRealizados.newpoint(name=row.Punto.nombre, coords=[(row.Punto.lon, row.Punto.lat)])
            point.style = greenstyle
        else:
            point = folNoRealizados.newpoint(name=row.Punto.nombre, coords=[(row.Punto.lon, row.Punto.lat)])
            point.style = redstyle
    curDir = request.folder

    import datetime
    from gluon.contenttype import contenttype
    sTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename= sTime + "_PuntosMuestrales.kml"
    import os
    if not os.path.exists(curDir+"kml"):
        os.makedirs(curDir+"kml")
    kml.save(curDir+ "kml" + os.sep + filename)
    response.headers['Content-Disposition']='attachment; filename='+filename
    response.headers['Content-Type'] = contenttype('.kml')
    return response.stream(curDir + os.sep + 'kml'+ os.sep+filename, chunk_size=64*1024)

def waterIds():
    """
    Método que retorna los ids de los tipos de caudales que se encuentran en la base de datos
    """
    ids = db().select(db.TipoCaudal.id)
    ret = []
    for waterid in ids:
        ret.append(waterid.id)
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps({'ids': ret})


@auth.requires_membership('administrador')
def updates():
    """
    Página que muestra la opción de verificar si existen actualizaciones en el servidor de los tipos de datos
    """
    session.show_title = False
    form = DIV( BUTTON("Ver", _id="ver", _class="toggle-btn", _type= "button"), BUTTON("Descargar e instalar", _id="descargar", _class="toggle-btn", _type= "button"))
    return dict(form=form)


@auth.requires_membership('administrador')
def seeUpdates():
    """
    Método que muestra las nuevas actualizaciones que se pueden incorporar al sistema
    """
    session.show_title = False
    result = checkForUpdates()
    inserts = []
    if result != []:
        for res in result:
            tokens = res['sql'].split("INTO")[1]
            tablePart = tokens.split("VALUES")[0]
            tableName = tablePart.split("(")[0]
            valuePart = tokens.split("VALUES")[1]
            value = valuePart.split(",'")[1]
            value = value[:-4]
            aux = {}
            aux['table'] = tableName
            aux['value'] = value
            inserts.append(aux)
    return dict(inserts=inserts)


@auth.requires_membership('administrador')
def checkForUpdates():
    from gluon.contrib.pysimplesoap.client import SoapClient, SoapFault
    # create a SOAP client
    client = SoapClient(wsdl="http://192.168.20.149:8888/ifn/webservice/call/soap?WSDL")
    # call SOAP method
    info = db(db.Version.id > 0).select().first()
    if info != None:
        dateString = info.db_version.strftime("%Y-%m-%d|%H:%M:%S")
        try:
            response = client.Updates(date=dateString)
            result = response['result']
        except SoapFault:
            result = []
    else:
        result = []
    return result

@auth.requires_membership('administrador')
def downloadUpdates():
    """
    Método que obtiene los nuevos cambios de la base de datos de la DGF y los inserta en la base de datos local
    """
    session.show_title = False
    result = checkForUpdates()
    empty = True
    executed = False
    error = False
    if result != []:
        empty = False

        for res in result:
            try:
                db.executesql(res['sql'])
            except:
                error = True
        executed = True
        if executed and not error:
            versionRow = db(db.Version.id > 0).select().first()
            if versionRow != None:
                import datetime
                versionRow.update_record(db_version=datetime.datetime.now())

    return dict(empty=empty, executed=executed, error=error)


def toggleFooter():
    if request.post_vars['action']:
        if request.post_vars['action'] == 'show':
            session.showFooter = True
        elif request.post_vars['action'] == 'hide':
            session.showFooter = False

