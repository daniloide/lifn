# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
"""
from gluon.tools import Service
service=Service()

def call():
    return service()
"""

@auth.requires_membership('digitador')
def ufiles():
    """
    Expose files in uploads
    """
    from os.path import join
    from gluon.tools import Expose
    path = join(request.folder,'uploads')
    return dict(files=Expose(path,basename='ufiles'))


# @service.json
def mImages():
    """Get images for a muestreo
    """
    """
    {
        image: 'img1.jpg',
        thumb: 'thumb1.jpg',
        big: 'big1.jpg',
        title: 'my first image',
        description: 'Lorem ipsum caption',
        link: 'http://domain.com'
    }
    """
    if request.env.is_https:
        prot="https";
    else:
        prot="http";
    prev = "%s://%s/%s/files/ufiles/images" % (prot,request.env.http_host,request.application,)
    try:
        muestreo=int(request.post_vars.muestreo)
        rows = []
        fotos = db(
            (db.Fotos.muestreo==muestreo) &
            (db.Fotos.tipoFoto==db.TipoFoto.id)
        ).select()
        for r in fotos:
            cell = {
                'title':r.TipoFoto.tipo,
                'description':r.Fotos.descr,
                'big':"%s/%s" % (prev,r.Fotos.foto),
                'thumb':"%s/%s/%s" % (prev,"thumbs",r.Fotos.foto),
                'image':"%s/%s/%s" % (prev,"optim",r.Fotos.foto),
            }
            rows.append(cell)
        return dict(result=True,rows=rows)
    except Exception as e:
        print "Exception: %s" % e
        return dict(result=False,rows=[])
