# -*- coding: utf-8 -*-
"""En este modulo se establece el menu de la aplicacion
"""

def createMenu():
    """Crea el menu de la aplicacion en base a estrucutra de listas"""
    mType = -1
    if auth.is_logged_in() and auth.has_membership('administrador',auth.user.id):
        return menuAdmin
    elif auth.is_logged_in():
        return menuUser
    else:
        return menuPublic

menuAdmin = [
    ( T('Home'), URL('default','index')==URL, URL('default','index'),[] ),
    ( T('Administration'), URL('default','index')==URL(),A(T('Administration'), _href="#"),
        [
            ( T('Load Samples'), URL('default','loadNewSamples')==URL, URL('default','loadNewSamples'),[] ),
            ( T('Asign Samples'), URL('default','muestreoUsuarios')==URL, URL('default','muestreoUsuarios'),[] ),
            ( T('Send Data'), URL('default','sendData')==URL, URL('default','sendData'),[] ),
            ( T('Export KML'), URL('default','kml')==URL(), URL('default','kml'),[] ),
            ( T('Users'), URL('admin','users')==URL(), URL('admin','users'), [] ),
            ( T('Check For Updates'), URL('default','updates')==URL(), URL('default','updates'), [] )
            
            
        ]
    ),
    ( T('About'), URL('default','about')==URL, URL('default','about'),[] ),
    ( T('Help'), URL('help','index')==URL(), A(T('Help'), _href="#"),
        [
            ( T('App manual'), URL('help','appmanual')==URL(), URL('help','appmanual'),[] ),
        ]
    ),
]

menuUser = [
    ( T('Home'), URL('default','index')==URL, URL('default','index'),[] ),
    ( T('About'), URL('default','about')==URL, URL('default','about'),[] ),
    ( T('Help'), URL('default','index')==URL(), A(T('Help'), _href="#"),
        [
            ( T('App manual'), URL('help','appmanual')==URL(), URL('help','appmanual'),[] ),
        ]
    ),
]

menuPublic = [
    ( T('Home'), URL('default','index')==URL, URL('default','index'),[] ),
    ( T('About'), URL('default','about')==URL, URL('default','about'),[] ),
    ( T('Help'), URL('default','index')==URL(), URL(),
        [
            ( T('Basic help'), URL('help','appbasic')==URL(), URL('help','appbasic'),[] ),
        ]
    ),
]

response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = createMenu()
