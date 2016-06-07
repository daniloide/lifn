# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 12:21:28 2012

@author: geus
"""

db.define_table('TipoBosque',
    Field('tipo', type='string',
          label='Tipo de Bosque', unique=True, notnull=True),
    format='%(tipo)s'
)

db.define_table('TipoGrupoConeat',
    Field('tipo', type='string',
          label='Tipo de Grupo Coneat', unique=True, notnull=True)
)

db.define_table('TipoSubBosque',
    Field('tipo', db.TipoBosque,
          label='Tipo de Bosque'),
    Field('nombre', type='string',
          label='Nombre', unique=True, notnull=True),
    format='%(nombre)s'
)

db.define_table('TipoFacilidadProgresion',
    Field('tipo', type='string',
          label='Facilidad de Progresion', unique=True, notnull=True)
)

db.define_table('TipoRaleo',
    Field('tipo', type='string',
          label='Tipo de Raleo', unique=True, notnull=True)
)

db.define_table('TipoAdaptacionEspecie',
    Field('tipo', type='string',
          label='Tipo de Adaptacion de la Especie', unique=True, notnull=True)
)

db.define_table('TipoRegimenBosquePlantado',
    Field('tipo', type='string',
          label='Tipo de Regimen de Bosque Plantado', unique=True, notnull=True)
)

db.define_table('TipoFrecuenciaFloraDelSuelo',
    Field('tipo', type='string',
          label='Tipo de Frecuencia', unique=True, notnull=True)
)

db.define_table('TipoEstadoGeneralBosquePlantado',
    Field('tipo', type='string',
          label='Tipo de Estado General de Bosque Plantado', unique=True, notnull=True)
)

db.define_table('TipoCaudal',
    Field('tipo', type='string',
          label='Tipo de Caudal', unique=True, notnull=True)
)

db.define_table('TipoFrecuencia',
    Field('tipo', type='string',
          label='Tipo de Frecuencia', unique=True, notnull=True)
)

db.define_table('TipoGradoContaminacion',
    Field('tipo', type='string',
          label='Tipo de Grado de Contaminacion', unique=True, notnull=True)
)

db.define_table('TipoUbicacion',
    Field('tipo', type='string',
          label='Tipo de Ubicacion', unique=True, notnull=True)
)

db.define_table('TipoExposicion',
    Field('tipo', type='string',
          label='Tipo de Exposicion', unique=True, notnull=True)
)

db.define_table('TipoFormaPendiente',
    Field('tipo', type='string',
          label='Tipo de Forma de la Pendiente', unique=True, notnull=True)
)

db.define_table('TipoUsoTierra',
    Field('tipo', type='string',
          label='Tipo de Uso de la Tierra', unique=True, notnull=True)
)

db.define_table('TipoUsoPrevio',
    Field('tipo', type='string',
          label='Tipo de Uso Previo', unique=True, notnull=True)
)

db.define_table('TipoLabranza',
    Field('tipo', type='string',
          label='Tipo de Labranza', unique=True, notnull=True)
)

db.define_table('TipoGradoErosion',
    Field('tipo', type='string',
          label='Tipo de Grado de Erosion', unique=True, notnull=True)
)

db.define_table('TipoErosion',
    Field('tipo', type='string',
          label='Tipo de Erosion', unique=True, notnull=True)
)

db.define_table('TipoProfundidadPrimerHorizonte',
    Field('tipo', type='string',
          label='Tipo de Profundidad del Primer Horizonte', unique=True, notnull=True)
)

db.define_table('TipoProfundidadMantillo',
    Field('tipo', type='string',
          label='Tipo de Profundidad del Mantillo', unique=True, notnull=True)
)

db.define_table('TipoProfundidadHumus',
    Field('tipo', type='string',
          label='Tipo de Profundidad Humus', unique=True, notnull=True)
)

db.define_table('TipoColor',
    Field('tipo', type='string',
          label='Tipo de Color', unique=True, notnull=True)
)

db.define_table('TipoTextura',
    Field('tipo', type='string',
          label='Tipo de Textura', unique=True, notnull=True)
)

db.define_table('TipoGradoCoberturaCopas',
    Field('tipo', type='string',
          label='Porcentaje', unique=True, notnull=True),
    Field('descripcion', type='string',
          label='Descripción', unique=True, notnull=True)
)

db.define_table('TipoGradoSotobosque',
    Field('tipo', type='string',
          label='Porcentaje', unique=True, notnull=True),
    Field('descripcion', type='string',
          label='Descripción', unique=True, notnull=True)
)

db.define_table('TipoCoberturaHerbacea',
    Field('tipo', type='string',
          label='Porcentaje', unique=True, notnull=True),
    Field('descripcion', type='string',
          label='Descripción', unique=True, notnull=True)
)

db.define_table('TipoCoberturaResiduosPlantas',
    Field('tipo', type='string',
          label='Porcentaje', unique=True, notnull=True),
    Field('descripcion', type='string',
          label='Descripción', unique=True, notnull=True)
)

db.define_table('TipoCoberturaResiduosCultivos',
    Field('tipo', type='string',
          label='Porcentaje', unique=True, notnull=True),
    Field('descripcion', type='string',
          label='Descripción', unique=True, notnull=True)
)

db.define_table('TipoEstructuraSuelo',
    Field('tipo', type='string',
          label='Tipo de Estructura del Suelo', unique=True, notnull=True)
)

db.define_table('TipoDrenaje',
    Field('tipo', type='string',
          label='Tipo de Drenaje', unique=True, notnull=True)
)

db.define_table('TipoInfiltracion',
    Field('tipo', type='string',
          label='Tipo de Infiltracion', unique=True, notnull=True)
)

db.define_table('TipoHumedad',
    Field('tipo', type='string',
          label='Tipo de Humedad', unique=True, notnull=True)
)

db.define_table('TipoRaices',
    Field('tipo', type='string',
          label='Tipo de Raices', unique=True, notnull=True)
)

db.define_table('TipoGanado',
    Field('tipo', type='string',
          label='Tipo de Ganado', unique=True, notnull=True)
)

db.define_table('TipoIntensidadPastoreo',
    Field('tipo', type='string',
          label='Tipo de Intesidad de Pastoreo', unique=True, notnull=True)
)

db.define_table('TipoSistemasProduccion',
    Field('tipo', type='string',
          label='Tipo de Sistemas de Produccion', unique=True, notnull=True)
)

db.define_table('TipoSotobosque',
    Field('tipo', type='string',
          label='Tipo de Sotobosque', unique=True, notnull=True)
)

db.define_table('TipoOrigenPlantacion',
    Field('tipo', type='string',
          label='Tipo de Origen de Plantacion', unique=True, notnull=True)
)

db.define_table('TipoEstructuraForestacion',
    Field('tipo', type='string',
          label='Tipo de Estructura de la Forestacion', unique=True, notnull=True)
)

"""
db.define_table('TipoPropiedadTierra',
    Field('tipo', type='string',
          label='Tipo de Propiedad de la Tierra', unique=True, notnull=True)
)
"""

db.define_table('TipoGradoIntervencion',
    Field('tipo', type='string',
          label='Tipo de Grado de Intervencion', unique=True, notnull=True)
)

db.define_table('TipoDestinoMadera',
    Field('tipo', type='string',
          label='Tipo de Destino de la Madera', unique=True, notnull=True)
)

db.define_table('TipoTecnologiaExplotacion',
    Field('tipo', type='string',
          label='Tipo de Tecnologia de Explotacion', unique=True, notnull=True)
)

db.define_table('TipoEvidenciasFuego',
    Field('tipo', type='string',
          label='Tipo de Evidencias de Fuego', unique=True, notnull=True)
)

db.define_table('TipoFuego',
    Field('tipo', type='string',
          label='Tipo de Fuego', unique=True, notnull=True)
)

db.define_table('TipoFuegoSanidad',
    Field('tipo', type='string',
          label='Tipo de Fuego', unique=True, notnull=True)
)

db.define_table('TipoPropositoFuego',
    Field('tipo', type='string',
          label='Tipo de Proposito del Fuego', unique=True, notnull=True)
)

db.define_table('TipoRangoEdadNativo',
    Field('tipo', type = 'string',
          label = 'Rango', unique=True, notnull=True)
)

db.define_table('TipoRangoEdadPlantado',
    Field('tipo', type = 'string',
          label = 'Rango', unique=True, notnull=True)

)

db.define_table('TipoSeveridad',
    Field('tipo', type = 'string',
          label = 'Severidad', unique=True, notnull=True)
)

db.define_table('TipoCategoriaEspeciesInvasoras',
    Field('tipo', type = 'string',
          label = 'Categoria', unique=True, notnull=True)
)

db.define_table('TipoForma',
    Field('tipo', type = 'string',
          label = 'Forma', unique=True, notnull=True)
)

"""
db.define_table('TipoCategoriaEucalipto',
    Field('tipo', type = 'string',
          label = 'Categoria', unique=True, notnull=True)
)

db.define_table('TipoCategoriaPino',
    Field('tipo', type = 'string',
          label = 'Categoria', unique=True, notnull=True)
)

db.define_table('TipoFuste',
    Field('tipo', type = 'string',
          label = 'Tipo de Fuste', unique=True, notnull=True)
)

db.define_table('TipoPorcentajeCopa',
    Field('tipo', type = 'string',
          label = 'Porcentaje de Copa Presente', unique=True, notnull=True)
)

db.define_table('TipoBrotacionEpicormica',
    Field('tipo', type = 'string',
          label = 'Brotacion Epicormica', unique=True, notnull=True)
)

db.define_table('TipoViento',
    Field('tipo', type = 'string',
          label = 'Viento', unique=True, notnull=True)
)

db.define_table('TipoGranizo',
    Field('tipo', type = 'string',
          label = 'Granizo', unique=True, notnull=True)
)

db.define_table('TipoSequia',
    Field('tipo', type = 'string',
          label = 'Sequia', unique=True, notnull=True)
)


db.define_table('TipoHeladas',
    Field('tipo', type = 'string',
          label = 'Heladas', unique=True, notnull=True)
)

db.define_table('TipoMalezas',
    Field('tipo', type = 'string',
          label = 'Malezas', unique=True, notnull=True)
)

db.define_table('TipoRajaduras',
    Field('tipo', type = 'string',
          label = 'Rajaduras y/o exudados', unique=True, notnull=True)
)

db.define_table('TipoCtenarytaina',
    Field('tipo', type = 'string',
          label = 'Ctenarytaina', unique=True, notnull=True)
)

db.define_table('TipoGonipterus',
    Field('tipo', type = 'string',
          label = 'Gonipterus', unique=True, notnull=True)
)
db.define_table('TipoHormigas',
    Field('tipo', type = 'string',
          label = 'Hormigas', unique=True, notnull=True)
)
db.define_table('TipoPhoracantha',
    Field('tipo', type = 'string',
          label = 'Phoracantha', unique=True, notnull=True)
)
db.define_table('TipoDanioGanado',
    Field('tipo', type = 'string',
          label = 'Danio por Ganado', unique=True, notnull=True)
)
db.define_table('TipoPuccinia',
    Field('tipo', type = 'string',
          label = 'Puccinia', unique=True, notnull=True)
)
db.define_table('TipoHongosFoliares',
    Field('tipo', type = 'string',
          label = 'Hongos Foliares', unique=True, notnull=True)
)
db.define_table('TipoPantoea',
    Field('tipo', type = 'string',
          label = 'Pantoea', unique=True, notnull=True)
)
db.define_table('TipoConiothyrium',
    Field('tipo', type = 'string',
          label = 'Coniothyrium', unique=True, notnull=True)
)

db.define_table('TipoMuerteRegresiva',
    Field('tipo', type = 'string',
          label = 'Muerte Regresiva', unique=True, notnull=True)
)

db.define_table('TipoCarpoforos',
    Field('tipo', type = 'string',
          label = 'Carpoforos', unique=True, notnull=True)
)

db.define_table('TipoChinche',
    Field('tipo', type = 'string',
          label = 'Thaumastocoris', unique=True, notnull=True)
)

db.define_table('TipoMycosphaerella',
    Field('tipo', type = 'string',
          label = 'Mycosphaerella', unique=True, notnull=True)
)

db.define_table('TipoDeficitNutricional',
    Field('tipo', type = 'string',
          label = 'Deficit Nutricional', unique=True, notnull=True)
)

db.define_table('TipoHerbicida',
    Field('tipo', type = 'string',
          label = 'Herbicida', unique=True, notnull=True)
)

db.define_table('TipoCinara',
    Field('tipo', type = 'string',
          label = 'Cinara', unique=True, notnull=True)
)


db.define_table('TipoPissodes',
    Field('tipo', type = 'string',
          label = 'Pissodes', unique=True, notnull=True)
)

db.define_table('TipoSphaeropsis',
    Field('tipo', type = 'string',
          label = 'Sphaeropsis', unique=True, notnull=True)
)

db.define_table('TipoExudados',
    Field('tipo', type = 'string',
          label = 'Exudados', unique=True, notnull=True)
)

db.define_table('TipoSirex',
    Field('tipo', type = 'string',
          label = 'Sirex', unique=True, notnull=True)
)

db.define_table('TipoLeucaspis',
    Field('tipo', type = 'string',
          label = 'Leucaspis', unique=True, notnull=True)
)

db.define_table('TipoEscolitidos',
    Field('tipo', type = 'string',
          label = 'Escolitidos', unique=True, notnull=True)
)

db.define_table('TipoPatogenosAciculas',
    Field('tipo', type = 'string',
          label = 'PatogenosAciculas', unique=True, notnull=True)
)
"""

db.define_table('TipoClase',
    Field('tipo', type = 'string',
          label = 'Tipo', unique=True, notnull=True)
)

db.define_table('TipoNombreCientificoClase',
    Field('nomCientifico', type = 'string',
          label = 'Nombre Científico', unique=True, notnull=True),
    Field('clase', db.TipoClase,
          label = 'Clase')
)

db.define_table('TipoNombreComun',
   Field('especie', db.TipoNombreCientificoClase,
          label = 'Especie'),
   Field('nombreComun', type = 'string',
          label = 'Nombre Común')
)

db.define_table('TipoNombreCientificoEspeciesInvasoras',
    Field('nombreCientifico', type = 'string',
          label = 'Nombre Científico', unique=True, notnull=True),
    Field('categoria',db.TipoCategoriaEspeciesInvasoras,
          label = 'Categoría', comment='Categoría de especies invasivas observados en el terreno'),
)

db.TipoNombreCientificoEspeciesInvasoras.categoria.requires = IS_IN_DB(db, db.TipoCategoriaEspeciesInvasoras.id, '%(tipo)s', orderby=db.TipoCategoriaEspeciesInvasoras.id)

db.define_table('TipoNombreComunEspeciesInvasoras',
    Field('nombreCientifico', db.TipoNombreCientificoEspeciesInvasoras,
          label = 'Nombre Científico'),
    Field('nombreComun', type = 'string',
          label = 'Nombre Común', notnull=True)
)


"""
db.define_table('TipoRhyacionia',
    Field('tipo', type = 'string',
          label = 'Rhyacionia', unique=True, notnull=True)
)

db.define_table('TipoGlycaspis',
    Field('tipo', type = 'string',
          label = 'Glycaspis', unique=True, notnull=True)
)
"""

db.define_table('TipoEstrato',
    Field('tipo', type = 'string',
          label = 'Estrato', unique=True, notnull=True)
)

db.define_table('TipoFloraNombreCientifico',
    Field('tipo', type = 'string',
          label = 'Nombre Científico', unique=True, notnull=True)
)

db.define_table('TipoFloraNombreComun',
    Field('nombreCientifico', db.TipoFloraNombreCientifico,
          label = 'Nombre Cientifico', notnull=True),
    Field('nombreComun', type='string',
          label='Nombre Común', notnull=True)
)

db.define_table('TipoBNNombreCientifico',
    Field('tipo', type = 'string',
          label = 'Nombre Científico', unique=True, notnull=True)
)

db.define_table('TipoBNNombreComun',
    Field('nombreCientifico', db.TipoBNNombreCientifico,
          label = 'Nombre Cientifico', notnull=True),
    Field('nombreComun', type='string',
          label='Nombre Común', notnull=True)
)

###### TABLAS ########

## field_types = ['boolean', 'string', 'text', 'password', 'blob',
## 'upload', 'integer', 'double', 'decimal', 'date', 'time', 'datetime']

db.define_table('Punto',
    Field('lat', type = 'double',
          label = 'Latitud', comment='Esta es la prueba del comentario de latitud'),
    Field('lon', type = 'double',
          label = 'Longitud'),
    Field('nombre', type = 'string',
          label = 'Nombre', unique=True),
    format='%(nombre)s'
)

#RNE
db.Punto.lat.requires = IS_NOT_EMPTY()
db.Punto.lon.requires = IS_NOT_EMPTY()
db.Punto.nombre.requires = IS_NOT_EMPTY()

db.define_table('Muestreo',
    Field('punto', db.Punto,
          label = 'Punto'),
    Field('anioMuestreo',type = 'integer',
          label = 'Año'),
    format=lambda r: '%s - %s' % (db.Punto[r.punto].nombre, r.anioMuestreo)
)

db.define_table('TipoAccion',
    Field('tipo', type = 'string',
          label = 'Tipo Accion', unique=True, notnull=True)
)

db.define_table('EventosAsignacion',
    Field('fecha', type = 'date',
        label = 'Fecha'),
    Field('usuario', db.auth_user,
          label = 'Hecho Por:'),
    Field('accion', db.TipoAccion,
          label = 'Accion'),
    Field('muestreo', db.Muestreo,
          label = 'Punto')
)

db.define_table('MuestreoUsuario',
    Field('muestreo', db.Muestreo, label = 'Punto de Muestreo', unique = True),
    Field('usuario', db.auth_user, label = 'Asignado'),
    Field('realizado', type='boolean', label = 'Realizado', notnull=True),
    format='%(muestreo)s'
)

#RNE
db.Muestreo.anioMuestreo.requires = IS_INT_IN_RANGE(1940, 2500)

db.define_table('TipoRegion',
    Field('nombre', type = 'string',
          label = 'Nombre', unique=True, notnull=True),
    format='%(nombre)s'
)

db.define_table('TipoDepartamento',
    Field('codigo', type = 'string',
          label = 'Codigo', unique=True, notnull=True),
    Field('nombre', type = 'string',
          label = 'Nombre', unique=True, notnull=True),
    Field('region', db.TipoRegion,
          label = 'Región', unique=False, notnull=True),
    format='%(nombre)s'
)

db.TipoDepartamento.region.requires = IS_IN_DB(db, db.TipoRegion.id, '%(nombre)s')

db.define_table('DatosGenerales',
    Field('muestreo',db.Muestreo,
          label = 'Punto de Muestreo', unique=True),
    Field('tipoDeBosque', db.TipoBosque,
          label = 'Tipo de Bosque', comment='Refiere a las especies que conforman el bosque'),
    Field('subbosque', db.TipoSubBosque,
          label = 'Sub Tipo de Bosque', comment='Subtipo del bosque seleccionado'),
    Field('fecha', type = 'date',
          label = 'Fecha', comment='Fecha de recolección de datos de campo'),
    Field('facilidadProgresion', db.TipoFacilidadProgresion,
          label = 'Facilidad de Progresion', comment='Facilidad con la que se puede acceder al punto de muestreo'),
    Field('departamento', db.TipoDepartamento,
          label = 'Departamento', comment='Departamento en el cual se encuentra localizado el punto de muestreo'),
    Field('propietario', type = 'string',
          label = 'Propietario del establecimiento', comment='Identificación de la empresa o titular de la tierra en la cual se ubica el punto de muestreo'),
    Field('predio', type = 'string',
          label = 'Nombre del predio', comment='Nombre o denominación del predio donde se encuentra ubicado el punto de muestreo')
)


#RNE
db.DatosGenerales.fecha.requires = IS_NOT_EMPTY()
db.DatosGenerales.propietario.requires = IS_NOT_EMPTY()
db.DatosGenerales.predio.requires = IS_NOT_EMPTY()
db.DatosGenerales.tipoDeBosque.requires = IS_IN_DB(db, db.TipoBosque.id, '%(tipo)s')
db.DatosGenerales.subbosque.requires = IS_IN_DB(db, db.TipoSubBosque.id, '%(nombre)s')
db.DatosGenerales.facilidadProgresion.requires = IS_IN_DB(db, db.TipoFacilidadProgresion.id, '%(tipo)s', orderby=db.TipoFacilidadProgresion.id)
db.DatosGenerales.fecha.requires = IS_DATE(format=T('%Y-%m-%d'))
db.DatosGenerales.departamento.requires = IS_IN_DB(db, db.TipoDepartamento.id, '%(nombre)s')


db.define_table('Distancias',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo', unique=True),
    Field('carreteraCaminoVecinal', type = 'double',
          label = 'Carretera a Camino Vecinal (km)', comment='Distancia en kilómetros que se recorre desde carretera o ruta hasta el camino vecinal'),
    Field('caminoVecinalCaminoAcceso', type= 'double',
          label = 'Camino Vecinal a Camino de Acceso (km)', comment='Distancia recorrida en kilómetros transcurridos desde el acceso al camino vecinal al camino de acceso donde se encuentra el punto de muestreo'),
    Field('caminoAccesoPuntoGPS', type = 'double',
          label = 'Camino de Acceso a Punto GPS (m)', comment='Distancia recorrida en metros por el camino de acceso hasta el punto que registra el GPS'),
    Field('puntoGPSCentroParcela', type ='double',
          label = 'Punto GPS a Centro de Parcela (m)', comment='Distancia del punto GPS al centro de la parcela'),
    Field('rumboCaminoCentroParcela', type= 'double',
          label = 'Rumbo Camino a Centro Parcela (grados)', comment='Rumbo camino al centro de la parcela en grados'),
    Field('track', type = 'string', notnull = True,
          label = 'Track (.gpx)', comment='Archivo del track')
)

db.Distancias.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Distancias.carreteraCaminoVecinal.requires = IS_FLOAT_IN_RANGE(0, 300)
db.Distancias.caminoVecinalCaminoAcceso.requires = IS_FLOAT_IN_RANGE(0, 300)
db.Distancias.caminoAccesoPuntoGPS.requires = IS_FLOAT_IN_RANGE(0, 30000)
db.Distancias.puntoGPSCentroParcela.requires = IS_FLOAT_IN_RANGE(0, 30000)
db.Distancias.rumboCaminoCentroParcela.requires = IS_FLOAT_IN_RANGE(0, 360)


db.define_table('CoordenadasParcela',
    Field('sur', type = 'double',
          label = 'Latitud', comment='Latitud en grados decimales. Ej.: -33.2283'),
    Field('oeste', type = 'double',
          label = 'Longitud', comment='Longitud en grados decimales. Ej.: -55.0578'),
    Field('altitud', type = 'double',
          label = 'Altitud (m)', comment='Altura sobre el nivel del mar'),
    Field('muestreo', db.Muestreo,
          label = 'Muestreo', unique=True)
)

db.CoordenadasParcela.sur.requires = IS_FLOAT_IN_RANGE(-35.5, -29.5)
db.CoordenadasParcela.oeste.requires = IS_FLOAT_IN_RANGE(-59.5, -52.5)
db.CoordenadasParcela.altitud.requires = IS_FLOAT_IN_RANGE(0, 600)
db.CoordenadasParcela.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')

db.define_table('Fauna',
    Field('muestreo', db.Muestreo,
          label = 'Punto Muestreo'),
    Field('especie', db.TipoNombreCientificoClase,
          label = 'Especie'),
    Field('frec', type = 'integer',
          label = 'Frecuencia', comment='Cantidad de individuos observados')
)

db.Fauna.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Fauna.especie.requires = IS_IN_DB(db, db.TipoNombreCientificoClase.id, '%(nombreCientifico)s', orderby=db.TipoNombreCientificoClase.id)
db.Fauna.frec.requires = IS_INT_IN_RANGE(0, None)

db.define_table('TipoFoto',
    Field('tipo', type="string")
)

db.define_table('Fotos',
    Field('muestreo', db.Muestreo,
          label='Muestreo'),
    Field('tipoFoto', db.TipoFoto,
          label='Tipo de Foto', comment='Tipo de foto a guardar'),
    Field('descr', type='string',
          label='Descripción', comment='Descripción representativa de la foto'),
    Field('foto', type='string',
          label='Nombre', comment='Nombre de la foto'),
    Field('lat', type='double',
          label='Latitud', comment='Latitud en grados decimales. Ej.: -33.2283'),
    Field('lon', type='double',
          label='Longitud', comment='Longitud en grados decimales. Ej.: -55.0578')
)



db.Fotos.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Fotos.tipoFoto.requires = IS_IN_DB(db, db.TipoFoto.id, '%(tipo)s', orderby=db.TipoFoto.id)
db.Fotos.lat.requires = IS_NOT_EMPTY()
db.Fotos.lat.requires = IS_FLOAT_IN_RANGE(-35.5, -29.5)
db.Fotos.lon.requires = IS_FLOAT_IN_RANGE(-59.5, -52.5)
db.Fotos.lon.requires = IS_NOT_EMPTY()

db.define_table('EquipoTrabajo',
    Field('muestreo', db.Muestreo,
          label = 'Punto de Muestreo'),
    Field('cargo', type = 'string',
          label = 'Cargo', comment='Cargo del integrante del equipo de trabajo'),
    Field('nombre', type = 'string',
          label = 'Nombre', comment='Nombre del integrante del equipo de trabajo')
)



db.EquipoTrabajo.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.EquipoTrabajo.cargo.requires = IS_NOT_EMPTY()
db.EquipoTrabajo.nombre.requires = IS_NOT_EMPTY()

db.define_table('Observaciones',
    Field('muestreo', db.Muestreo,
          label = 'Punto de Muestreo', unique=True),
    Field('observacion', type = 'text',
          label = 'Observaciones')
)



db.Observaciones.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')

db.define_table('TipoGenero',
    Field('codigo', type='string',
          label='Codigo'),
    Field('genero', type='string',
          label='Genero', unique=True)
)

db.TipoGenero.codigo.requires = IS_NOT_EMPTY()
db.TipoGenero.genero.requires = IS_NOT_EMPTY()

db.define_table('TipoEspecie',
    Field('genero', db.TipoGenero,
          label='Genero'),
    Field('codigo', type='string',
          label='Codigo'),
    Field('especie', type='string',
          label='Especie')
)

db.TipoEspecie.genero.requires = IS_IN_DB(db, db.TipoGenero.id, '%(genero)s')
db.TipoEspecie.codigo.requires = IS_NOT_EMPTY()
db.TipoEspecie.especie.requires = IS_NOT_EMPTY()

db.define_table('TipoFamilia',
    Field('tipo', type='string',
          label='Codigo'),
    format = '%(nombre)s'
)

db.TipoFamilia.tipo.requires = IS_NOT_EMPTY()


db.define_table('TipoEspecieNativas',
    Field('nombreCientifico', type='string',
          label='Nombre Científico', unique=True),
    Field('nombre', type='string',
          label='Nombre vulgar'),
    Field('familia', db.TipoFamilia,
          label='Familia')
)

db.TipoEspecieNativas.nombreCientifico.requires = IS_NOT_EMPTY()
db.TipoEspecieNativas.nombre.requires = IS_NOT_EMPTY()
db.TipoEspecieNativas.familia.requires = IS_IN_DB(db, db.TipoFamilia.id, '%(nombre)s', orderby=db.TipoFamilia.id)


db.define_table('Plantacion',
    Field('muestreo', db.Muestreo,
          label='Muestreo'),
    Field('genero', db.TipoGenero,
          label='Genero', comment='Nombre del género de los individuos son predominantes en la parcela'),
    Field('especie', db.TipoEspecie,
          label='Especie', comment='Nombre de la especie de los individuos que son predominantes en la parcela'),
    Field('rangoEdad', db.TipoRangoEdadPlantado,
          label='Rango de Edad', comment='Rango de edad de la plantación'),
    Field('raleo', db.TipoRaleo,
          label='Raleo', comment='Práctica silvicultural que consiste en la cosecha de algunos individuos para privilegiar el crecimiento de los individuos remanentes'),
    Field('tienePoda', type = 'boolean',
          label =  'Poda', comment='Determina si la plantación tiene poda o no'),
    Field('alturaPoda', type='double',
          label='Altura de Poda (m)', default=0.0, comment='Altura en metros de la poda'),
    Field('parcelaRegular', type='boolean',
          label='Parcela regular', comment='Discrimina si es una parcela regular'),
    Field('distanciaFila', type='double',
          label='Distancia de las filas (m)', comment='Distancia en metros de las filas de la plantación'),
    Field('distanciaEntreFila', type='double',
          label='Distancia entre las filas (m)', comment='Distancia en metros entre las filas de la plantación'),
    Field('cantidadFilas', type='integer',
          label='Cantidad de filas', default=0, comment='Cantidad de filas de árboles agrupados'),
    Field('distanciaSilvopastoreo', type='double',
          label='Distancia de silvopastoreo (m)', default=0.0, comment='Distancia en metros de silvopastoreo'),
    Field('adaptacionEspecie', db.TipoAdaptacionEspecie,
          label='Adaptacion de la Especie', comment='Aspecto general que puede observarse en los individuos en cuanto a su crecimiento, desarrollo y estado sanitario'),
    Field('regimen', db.TipoRegimenBosquePlantado,
          label='Regimen', comment='Régimen de la plantación'),
    Field('estadoGeneral', db.TipoEstadoGeneralBosquePlantado,
          label='Estado General', comment='Describe el estado general en el que se encuentra la plantación en cuanto a mantenimiento de cortafuegos, sotobosque, regeneración, malezas, enfermedades, daños causados por animales, hombre o naturaleza y al manejo silvicultural recibido')
)



db.Plantacion.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Plantacion.genero.requires = IS_IN_DB(db, db.TipoGenero.id, '%(genero)s', orderby=db.TipoGenero.id)
db.Plantacion.especie.requires = IS_IN_DB(db, db.TipoEspecie.id, '%(especie)s', orderby=db.TipoEspecie.id)
db.Plantacion.rangoEdad.requires = IS_IN_DB(db, db.TipoRangoEdadPlantado.id, '%(tipo)s', orderby=db.TipoRangoEdadPlantado.id)
db.Plantacion.raleo.requires = IS_IN_DB(db, db.TipoRaleo.id, '%(tipo)s', orderby=db.TipoRaleo.id)
db.Plantacion.alturaPoda.requires = IS_FLOAT_IN_RANGE(0, 100)
db.Plantacion.distanciaFila.requires = IS_FLOAT_IN_RANGE(0, None)
db.Plantacion.distanciaEntreFila.requires = IS_FLOAT_IN_RANGE(0, None)
db.Plantacion.cantidadFilas.requires = IS_INT_IN_RANGE(0, None)
db.Plantacion.distanciaSilvopastoreo.requires = IS_FLOAT_IN_RANGE(0, None)
db.Plantacion.adaptacionEspecie.requires = IS_IN_DB(db, db.TipoAdaptacionEspecie.id, '%(tipo)s', orderby=db.TipoAdaptacionEspecie.id)
db.Plantacion.regimen.requires = IS_IN_DB(db, db.TipoRegimenBosquePlantado.id, '%(tipo)s', orderby=db.TipoRegimenBosquePlantado.id)
db.Plantacion.estadoGeneral.requires = IS_IN_DB(db, db.TipoEstadoGeneralBosquePlantado.id, '%(tipo)s', orderby=db.TipoEstadoGeneralBosquePlantado.id)


db.define_table('Agua',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('tipoCaudal', 'list:reference db.TipoCaudal',
          label='Tipo de Caudal'),
    Field('manejo', type='boolean',
          label='Manejo', comment='Existencia de elementos que permiten regular el recurso hídrico'),
    Field('frecuencia', db.TipoFrecuencia,
          label='Frecuencia', comment='Capacidad de un curos de agua de permanecer o no a lo largo de transcurso del tiempo'),
    Field('acuacultura', type='boolean',
          label='Acuacultura', comment='Es el cultivo de animales y plantas en el agua'),
    Field('gradoContaminacion', db.TipoGradoContaminacion,
          label='Grado de Contaminacion', comment='Presencia de sedimentos, hidrocarburos, pesticidas, residuos orgánicos e inorgánicos en el caudal')
)

db.Agua.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Agua.frecuencia.requires = IS_IN_DB(db, db.TipoFrecuencia.id, '%(tipo)s', orderby=db.TipoFrecuencia.id)
db.Agua.gradoContaminacion.requires = IS_IN_DB(db, db.TipoGradoContaminacion.id, '%(tipo)s', orderby=db.TipoGradoContaminacion.id)
db.Agua.tipoCaudal.requires = IS_IN_DB(db, db.TipoCaudal.id, '%(tipo)s',multiple=True, orderby=db.TipoCaudal.id)

db.define_table('NombreAfluentes',
    Field('muestreo', db.Muestreo,
          label='Muestreo'),
    Field('nombre', type='string',
          label='Nombre del Afluente'),
    Field('tipo', db.TipoCaudal,
          label='Tipo de Caudal'),
    Field('distancia', type='double',
          label='Distancia hasta el afluente (m)')

)

db.NombreAfluentes.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.NombreAfluentes.tipo.requires = IS_IN_DB(db, db.TipoCaudal.id, '%(tipo)s', orderby=db.TipoCaudal.id)
db.NombreAfluentes.distancia.requires = IS_FLOAT_IN_RANGE(0, None)

db.define_table('Relieve',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('ubicacion', db.TipoUbicacion,
          label='Ubicacion', comment='Lugar donde se encuentra la parcela'),
    Field('exposicion', db.TipoExposicion,
          label='Exposicion', comment='Orientación cardinal que tiene el terreno'),
    Field('pendiente', type='double',
          label='Pendiente (%)', comment='La pendiente en un punto del terreno se define como el ángulo existente entre el vector normal a la superficie en ese punto y la vertical'),
    Field('formaPendiente', db.TipoFormaPendiente,
          label='Forma de la Pendiente', comment='Característica de la pendiente con respecto a su desarrollo, pudiendo ser cóncava, convexa o lineal')
)


db.Relieve.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Relieve.ubicacion.requires = IS_IN_DB(db, db.TipoUbicacion.id, '%(tipo)s', orderby=db.TipoUbicacion.id)
db.Relieve.exposicion.requires = IS_IN_DB(db, db.TipoExposicion.id, '%(tipo)s', orderby=db.TipoExposicion.id)
db.Relieve.pendiente.requires = IS_FLOAT_IN_RANGE(0, 100)
db.Relieve.formaPendiente.requires = IS_IN_DB(db, db.TipoFormaPendiente.id, '%(tipo)s', orderby=db.TipoFormaPendiente.id)

db.define_table('Suelo',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('usoTierra', 'list:reference db.TipoUsoTierra',
          label='Uso de la Tierra', comment='Tipo de actividad a la que se le ha dado destino a la tierra en el momento de realizar el muestreo'),
    Field('usoPrevio', db.TipoUsoPrevio,
          label='Uso Previo', comment='Uso que se le daba a la tierra antes de la actividad que se realiza actualmente'),
    Field('tipoLabranza', db.TipoLabranza,
          label='Tipo de Labranza', comment='Laboreo realizado para la implantación de la masa boscosa'),
    Field('gradoErosion', db.TipoGradoErosion,
          label='Grado de Erosion', comment='Pérdida de suelo por agua, viento, hombre, animales'),
    Field('tipoErosion', 'list:reference db.TipoErosion',
          label='Tipo de Erosion', comment='Se debe seleccionar el tipo de erosión según la definición'),
    Field('profundidadPrimerHorizonte', db.TipoProfundidadPrimerHorizonte,
          label='Profundidad del Primer Horizonte', comment='Determinación de la profundidad en centímetros del primer horizonte'),
    Field('profundidadMantillo', db.TipoProfundidadMantillo,
          label='Profundidad del Mantillo', comment='Capa formada por la descomposición de materia orgánica'),
    Field('profundidadHumus', db.TipoProfundidadHumus,
          label='Profundidad Humus', comment='Sustancia compuesta por productos orgánicos, de naturaleza coloidal, que proviene de la descomposición de los restos orgánicos'),
    Field('color', db.TipoColor,
          label='Color', comment='El color muestra propiedades muy importantes de la tierra'),
    Field('textura', 'list:reference db.TipoTextura',
          label='Textura', comment='Distribución porcentual de partículas inorgánicas (arenas, limos y arcillas) de tamaño inferior a 2 mm'),
    Field('estructura', db.TipoEstructuraSuelo,
          label='Estructura', comment='Proceso de unión (ordenada o desordenada), de edafo-constituyentes, coloides, geles, etc., que se desarrolla en el suelo'),
    Field('drenaje', db.TipoDrenaje,
          label='Drenaje', comment='Drenaje consiste en la remoción del exceso de agua de la superficie del suelo y/o del perfil del suelo de terreno por gravedad'),
    Field('infiltracion', db.TipoInfiltracion,
          label='Infiltración', comment='Proceso por el cual el agua penetra desde la superficie del terreno hacia el suelo'),
    Field('impedimento', type='boolean',
          label='Impedimento', comment='Factores que influyen en la infiltración como la agregación, permeabilidad y estructura del suelo que la afectan directamente'),
    Field('olor', type='boolean',
          label='Olor', comment='Presencia o ausencia de olor del suelo'),
    Field('humedad', db.TipoHumedad,
          label='Humedad', comment='Cantidad de agua retenida en el suelo'),
    Field('pedregosidad', type='double',
          label='Pedregosidad (%)', comment='Porcentaje que ocupa en los suelos en los que predominan las gravas o rocas de todos los tamaños'),
    Field('rocosidad', type='double',
          label='Rocosidad (%)', comment='Porcentaje que ocupa en los suelos en los que predominan las rocas'),
    Field('micorrizas', type='boolean',
          label='Micorrizas', comment='Simbiosis mutualistas entre hongos y raíces de plantas superiores'),
    Field('faunaSuelo', type = 'boolean',
          label = 'Fauna del Suelo', comment='Conjunto de animales que viven en el suelo'),
    Field('raices', db.TipoRaices,
          label='Raices', comment='Disposición de raíces en el perfil'),
    Field('grupoConeat', db.TipoGrupoConeat,
          label = 'Grupo CONEAT')

)

db.Suelo.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Suelo.usoTierra.requires = IS_IN_DB(db, db.TipoUsoTierra.id, '%(tipo)s', multiple=True, orderby=db.TipoUsoTierra.id)
db.Suelo.usoPrevio.requires = IS_IN_DB(db, db.TipoUsoPrevio.id, '%(tipo)s', orderby=db.TipoUsoPrevio.id)
db.Suelo.tipoLabranza.requires = IS_IN_DB(db, db.TipoLabranza.id, '%(tipo)s', orderby=db.TipoLabranza.id)
db.Suelo.gradoErosion.requires = IS_IN_DB(db, db.TipoGradoErosion.id, '%(tipo)s', orderby=db.TipoGradoErosion.id)
db.Suelo.grupoConeat.requires = IS_IN_DB(db, db.TipoGrupoConeat.id, '%(tipo)s', orderby=db.TipoGrupoConeat.id)
db.Suelo.tipoErosion.requires = IS_IN_DB(db, db.TipoErosion.id, '%(tipo)s', multiple=True, orderby=db.TipoErosion.id)
"""db.Suelo.grupoConeat.requires = IS_IN_SET(('No se define','1.10a','1.10b','1.11a','1.11b','1.12','1.20','1.21','1.22','1.23','1.24','1.25','2.10','2.11a','2.11b','2.12','2.13','2.14','2.20','2.21','2.22','3.10','3.11','3.12','3.13','3.14','3.15','3.2','3.30','3.31','3.40','3.41','3.50','3.51','3.52','3.53','3.54','03.10','03.11','03.2','03.3','03.40',
'03.41','03.51','03.52','03.6','B03.1','G03.10','G03.11','G03.21','G03.22','G03.3','4.1','4.2','5.01a','5.01b','5.01c','5.02a','5.02b','5.3','5.4','5.5','6.1/1','6.1/2','6.1/3','6.2','6.3','6.4','6.5','6.6','6.7','6.8','6.9','6.10a','6.10b','6.11','6.12','6.13','6.14','6.15','6.16','6.17','7.1','7.2','7.31','7.32','7.33','7.41','7.42','07.1','07.2','8.1','8.02a','8.02b',
'8.3','8.4','8.5','8.6','8.7','8.8','8.9','8.10','8.11','8.12','8.13','8.14','8.15','8.16','9.1','9.2','9.3','9.41','9.42','9.5','9.6','9.7','9.8','9.9','09.1','09.2','09.3','09.4','09.5','S09.10','S09.11','S09.20','S09.21','S09.22','10.1','10.2','10.3','10.4','10.5','10.6a','10.6b','10.7','10.8a','10.8b','10.9','10.10','10.11','10.12','10.13','10.14','10.15','10.16',
'D10.1','D10.2','D10.3','G10.1','G10.2','G10.3','G10.4','G10.5','G10.6a','G10.6b','G10.7','G10.8','G10.9','G10.10','S10.10','S10.11','S10.12','S10.13','S10.20','S10.21','11.1','11.2','11.3','11.4','11.5','11.6','11.7','11.8','11.9','11.10','12.10','12.11','12.12','12.13','12.20','12.21','12.22','13.1','13.2','13.31','13.32','13.4','13.5'))
"""
db.Suelo.profundidadPrimerHorizonte.requires = IS_IN_DB(db, db.TipoProfundidadPrimerHorizonte.id, '%(tipo)s', orderby=db.TipoProfundidadPrimerHorizonte.id)
db.Suelo.profundidadMantillo.requires = IS_IN_DB(db, db.TipoProfundidadMantillo.id, '%(tipo)s', orderby=db.TipoProfundidadMantillo.id)
db.Suelo.profundidadHumus.requires = IS_IN_DB(db, db.TipoProfundidadHumus.id, '%(tipo)s', orderby=db.TipoProfundidadHumus.id)
db.Suelo.color.requires = IS_IN_DB(db, db.TipoColor.id, '%(tipo)s', orderby=db.TipoColor.id)
db.Suelo.textura.requires = IS_IN_DB(db, db.TipoTextura.id, '%(tipo)s', multiple=True, orderby=db.TipoTextura.id)
db.Suelo.estructura.requires = IS_IN_DB(db, db.TipoEstructuraSuelo.id, '%(tipo)s', orderby=db.TipoEstructuraSuelo.id)
db.Suelo.drenaje.requires = IS_IN_DB(db, db.TipoDrenaje.id, '%(tipo)s', orderby=db.TipoDrenaje.id)
db.Suelo.infiltracion.requires = IS_IN_DB(db, db.TipoInfiltracion.id, '%(tipo)s', orderby=db.TipoInfiltracion.id)
db.Suelo.humedad.requires = IS_IN_DB(db, db.TipoHumedad.id, '%(tipo)s', orderby=db.TipoHumedad.id)
db.Suelo.pedregosidad.requires = IS_FLOAT_IN_RANGE(0, 100)
db.Suelo.rocosidad.requires = IS_FLOAT_IN_RANGE(0, 100)
db.Suelo.raices.requires = IS_IN_DB(db, db.TipoRaices.id, '%(tipo)s', orderby=db.TipoRaices.id)


db.define_table('CoberturaVegetal',
    Field('muestreo', db.Muestreo,
          label='Muestreo' , unique=True),
    Field('gradoCoberturaCopas', db.TipoGradoCoberturaCopas,
          label='Grado de Cobertura de Copas', comment='Proyección vertical de las copas de los árboles como porcentaje total del área'),
    Field('gradoSotobosque', db.TipoGradoSotobosque,
          label='Grado de Sotobosque', comment='Proyección vertical de las copas del sotobosque como porcentaje total del área'),
    Field('coberturaHerbacea',db.TipoCoberturaHerbacea,
          label='Cobertura Herbacea', comment='Proyección vertical de las plantas herbáceas como porcentaje total del área'),
    Field('coberturaResiduosPlantas',type='string',
          label='Cobertura de Residuos de Plantas', comment='Proyección vertical de los residuos de plantas como porcentaje total del área'),
    Field('coberturaResiduosCultivos',type='string',
          label='Cobertura de Residuos de Cultivos',comment='Proyección vertical de los residuos de cultivos como porcentaje total del área')
)

db.CoberturaVegetal.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.CoberturaVegetal.gradoCoberturaCopas.requires = IS_IN_DB(db, db.TipoGradoCoberturaCopas.id, '%(tipo)s', orderby=db.TipoGradoCoberturaCopas.id)
db.CoberturaVegetal.gradoSotobosque.requires = IS_IN_DB(db, db.TipoGradoSotobosque.id, '%(tipo)s', orderby=db.TipoGradoSotobosque.id)
db.CoberturaVegetal.coberturaHerbacea.requires = IS_IN_DB(db, db.TipoCoberturaHerbacea.id, '%(tipo)s', orderby=db.TipoCoberturaHerbacea.id)
db.CoberturaVegetal.coberturaResiduosPlantas.requires = IS_IN_DB(db, db.TipoCoberturaResiduosPlantas.id, '%(tipo)s', orderby=db.TipoCoberturaHerbacea.id)
db.CoberturaVegetal.coberturaResiduosCultivos.requires = IS_IN_DB(db, db.TipoCoberturaResiduosCultivos.id, '%(tipo)s', orderby=db.TipoCoberturaHerbacea.id)

db.define_table('ProductosNoMadereros',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('tipoGanado', 'list:reference db.TipoGanado',
          label='Tipo de Ganado', comment='Animales domésticos que se encuentran en el bosque'),
    Field('intensidadPastoreo', db.TipoIntensidadPastoreo,
          label='Intensidad de Pastoreo', comment='Relación entre la cantidad removida y la cantidad inicial de pasto'),
    Field('sistemasProduccion', 'list:reference db.TipoSistemasProduccion',
          label='Sistemas de Producción', comment='Diferentes sistemas de producción que pueden estar asociados a los árboles'),
    Field('produccionApicola', type='boolean',
          label='Producción Apícola', comment='Presencia de cría de abejas asociadas al bosque'),
    Field('sombra', type='boolean',
          label='Sombra', comment='Bosque que permite al ganado estar fuera de las influencias directas del sol, Generalmente de poca extensión y con alta densidad de individuos por hectárea'),
    Field('rompeVientos', type='boolean',
          label='Rompe Vientos', comment='Bosque que tiene por función disminuir la velocidad del viento. Generalmente son largos y de poco ancho, con gran número de individuos por hectárea y con ramas hasta la base'),
    Field('recoleccionHongos', type='boolean',
          label='Recolección de Hongos', comment='Recolección de las setas de los hongos'),
    Field('aceitesEsenciales', type='boolean',
          label='Aceites Esenciales', comment='Aceites que se obtienen por destilación de las hojas de los árboles'),
    Field('obtencionSemillas', type='boolean',
          label='Obtención de Semillas', comment='Se cosechan semillas de los árboles'),
    Field('actividadesCasaPesca', type='boolean',
          label='Actividades de Caza y Pesca', comment='En el bosque se realizan actividades de caza y pesca recreativa'),
    Field('actividadesRecreacion', type='boolean',
          label='Actividades de Recreación', comment='Se realizan actividades recreativas como camping, senderismo, trecking, deportes'),
    Field('estudiosCientificos', type='boolean',
          label='Estudios Científicos', comment='En el bosque se han instalado ensayos científicos'),
    Field('fijacionCarbono', type='boolean',
          label='Fijación de Carbono', comment='El bosque puede estar sometido al régimen de fijación de carbono')
)

db.ProductosNoMadereros.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.ProductosNoMadereros.tipoGanado.requires = IS_IN_DB(db, db.TipoGanado.id, '%(tipo)s', multiple=True, orderby=db.TipoGanado.id)
db.ProductosNoMadereros.intensidadPastoreo.requires = IS_IN_DB(db, db.TipoIntensidadPastoreo.id, '%(tipo)s', orderby=db.TipoIntensidadPastoreo.id)
db.ProductosNoMadereros.sistemasProduccion.requires = IS_IN_DB(db, db.TipoSistemasProduccion.id, '%(tipo)s', multiple=True, orderby=db.TipoSistemasProduccion.id)


db.define_table('Flora',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('tipoSotobosque', "list:reference db.TipoSotobosque",
          label='Tipo de Sotobosque', comment='Tipo de vegetación formada por matas y arbustos que crece bajo los árboles de un bosque'),
    Field('alturaSotobosque', type='double',
          label='Altura del Sotobosque (m)', comment='Altura desde el suelo hasta el tope que desarrolla el sotobosque')
)

db.Flora.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Flora.tipoSotobosque.requires = IS_IN_DB(db, db.TipoSotobosque.id, '%(tipo)s', multiple=True, orderby=db.TipoSotobosque.id)
db.Flora.alturaSotobosque.requires = IS_FLOAT_IN_RANGE(0, 2)

db.define_table('FloraDelSuelo',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('nombreCientifico', db.TipoFloraNombreCientifico,
          label='Flora del Suelo'),
    Field('frecuencia', db.TipoFrecuenciaFloraDelSuelo,
          label='Frecuencia')
)
db.FloraDelSuelo.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.FloraDelSuelo.nombreCientifico.requires = IS_IN_DB(db, db.TipoFloraNombreCientifico.id, '%(nombreCientifico)s', orderby=db.TipoFloraNombreCientifico.id)
db.FloraDelSuelo.frecuencia.requires = IS_IN_DB(db, db.TipoFrecuenciaFloraDelSuelo.id, '%(tipo)s')

db.define_table('ProblemasAmbientales',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('pobreCalidadAgua', type='boolean',
          label='Pobre Calidad del Agua', comment='Evidencias de que el agua no tiene la calidad necesaria de potabilidad'),
    Field('polucionAire', type='boolean',
          label='Polución del Aire', comment='Evidencias de distorsiones causadas por la polución del aire'),
    Field('perdidaFertilidad', type='boolean',
          label='Perdida de Fertilidad', comment='Evidencias de que los nutrientes del suelo se han reducido por cultivos intensivos, uso intensivo de productos químicos, erosión del suelo y prácticas de laboreo inadecuadas'),
    Field('invasionEspecies', type='boolean',
          label='Invasión de Especies', comment='Evidencias de que especies exóticas comienzan a crecer y a afectar las especies nativas en el área'),
    Field('presenciaPesticidas', type='boolean',
          label='Presencia de Agrotóxicos', comment='Evidencias de que los pesticidas afectan las plantas del área')
)

db.ProblemasAmbientales.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')

db.define_table('ForestacionMantenimientoEstructura',
    Field('muestreo', db.Muestreo,
          label='Muestreo', unique=True),
    Field('origenPlantacion', db.TipoOrigenPlantacion,
          label='Origen de Plantación', comment='Fuente de origen de los árboles en el lugar de muestreo'),
    Field('estructura', db.TipoEstructuraForestacion,
          label='Estructura', comment='Características de los individuos de una plantación'),
    Field('propiedadTierra', type='string',
          label='Propietario del Bosque', comment=''),
    Field('planManejo', type='boolean',
          label='Plan de Manejo', comment='Existencia de planes de intervención del bosque'),
    Field('gradoIntervencion', db.TipoGradoIntervencion,
          label='Grado de Intervención humana', comment='Impacto del nivel de la actividad humana en el bosque'),
    Field('destinoMadera', "list:reference db.TipoDestinoMadera",
          label='Destino de la madera', comment='Destino que tiene la producción de la madera del bosque'),
    Field('manejoSilvicultural', type = 'boolean',
          label='Manejo Silvicultural', comment='El bosque presenta manejo silvicultural'),
    Field('tecnologiaExplotacion', db.TipoTecnologiaExplotacion,
          label='Tecnología de cosecha', comment='Forma en que se realiza o realizará la cosecha del bosque'),
)

db.ForestacionMantenimientoEstructura.propiedadTierra.requires=IS_IN_SET(('Particular','Estado'))
db.ForestacionMantenimientoEstructura.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.ForestacionMantenimientoEstructura.origenPlantacion.requires = IS_IN_DB(db, db.TipoOrigenPlantacion.id, '%(tipo)s', orderby=db.TipoOrigenPlantacion.id)
db.ForestacionMantenimientoEstructura.estructura.requires = IS_IN_DB(db, db.TipoEstructuraForestacion.id, '%(tipo)s', orderby=db.TipoEstructuraForestacion.id)
db.ForestacionMantenimientoEstructura.gradoIntervencion.requires = IS_IN_DB(db, db.TipoGradoIntervencion.id, '%(tipo)s', orderby=db.TipoGradoIntervencion.id)
db.ForestacionMantenimientoEstructura.destinoMadera.requires = IS_IN_DB(db, db.TipoDestinoMadera.id, '%(tipo)s', multiple=True, orderby=db.TipoDestinoMadera.id)
db.ForestacionMantenimientoEstructura.tecnologiaExplotacion.requires = IS_IN_DB(db, db.TipoTecnologiaExplotacion.id, '%(tipo)s', orderby=db.TipoTecnologiaExplotacion.id)


db.define_table('Fuego',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo', unique=True),
    Field('evidenciaFuego', "list:reference db.TipoEvidenciasFuego",
          label = 'Evidencias de Fuego', comment='Presencia o ausencia de evidencias de fuego'),
    Field('tipoFuego', "list:reference db.TipoFuego",
          label = 'Tipo de Fuego'),
    Field('propositoFuego', "list:reference db.TipoPropositoFuego",
          label = 'Propósito de Fuego', comment='Objetivo o propósito del fuego')
)

db.Fuego.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.Fuego.tipoFuego.requires = IS_IN_DB(db, db.TipoFuego.id, '%(tipo)s', multiple=True, orderby=db.TipoFuego.id)
db.Fuego.evidenciaFuego.requires = IS_IN_DB(db, db.TipoEvidenciasFuego.id, '%(tipo)s', multiple=True, orderby=db.TipoEvidenciasFuego.id)
db.Fuego.propositoFuego.requires = IS_IN_DB(db, db.TipoPropositoFuego.id, '%(tipo)s', multiple=True, orderby=db.TipoPropositoFuego.id)


db.define_table('EspeciesInvasoras',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo'),
    Field('nombreCientifico', db.TipoNombreCientificoEspeciesInvasoras,
          label = 'Nombre Científico', comment='Nombre científico de la especie invasora'),
    Field('severidad', db.TipoSeveridad,
          label = 'Severidad', comment='Severidad de la invasión')
)

db.EspeciesInvasoras.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')

db.EspeciesInvasoras.nombreCientifico.requires = IS_IN_DB(db, db.TipoNombreCientificoEspeciesInvasoras.id, '%(nombreCientifico)s')
db.EspeciesInvasoras.severidad.requires = IS_IN_DB(db, db.TipoSeveridad.id, '%(tipo)s', orderby=db.TipoSeveridad.id)

db.define_table('ParcelasBosquePlantado',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo'),
    Field('numArbol', type = 'integer',
          label = 'Árbol Número', comment='Número del árbol'),
    Field('dap1', type = 'double',
          label = 'Dap1 (m)', comment='Diámetro del árbol a la altura del pecho'),
    Field('dap2', type = 'double',
          label = 'Dap2 (m)', comment='Diámetro del árbol a la altura del pecho'),
    Field('distancia', type = 'double',
          label = 'Distancia (m)', comment='Distancia del árbol al centro de la parcela'),
    Field('direccionRumbo', type = 'double',
          label = 'Direccion del Rumbo (º)', comment='Valor en grados de la dirección'),
    Field('hc', type = 'double',
          label = 'Altura Comercial (m)', comment='Altura comercial del árbol'),
    Field('ht', type = 'double',
          label = 'Altura Total (m)', comment='Altura total del árbol'),
    Field('hPoda', type = 'double',
          label = 'Altura Poda (m)', comment='Altura de poda del árbol'),
    Field('forma', db.TipoForma,
          label = 'Forma', comment='Forma del árbol'),
    Field('espesorCorteza', type = 'double',
          label = 'Espesor Corteza (cm)', comment='Espesor de la corteza del árbol'),
    Field('observaciones', type = 'text',
          label = 'Observaciones', comment='Observaciones no contempladas en el formulario'),
    Field('radio', type = 'integer',
          label = 'Radio')
)

db.ParcelasBosquePlantado.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.ParcelasBosquePlantado.distancia.requires = IS_FLOAT_IN_RANGE(0, 30000)
db.ParcelasBosquePlantado.direccionRumbo.requires = IS_FLOAT_IN_RANGE(0, 360)
db.ParcelasBosquePlantado.hc.requires = IS_FLOAT_IN_RANGE(0, 6)
db.ParcelasBosquePlantado.ht.requires = IS_FLOAT_IN_RANGE(0, 60)
db.ParcelasBosquePlantado.hPoda.requires = IS_FLOAT_IN_RANGE(0, 200)
db.ParcelasBosquePlantado.forma.requires = IS_IN_DB(db, db.TipoForma.id, '%(tipo)s', orderby=db.TipoForma.id)
db.ParcelasBosquePlantado.espesorCorteza.requires = IS_FLOAT_IN_RANGE(0, 8)
db.ParcelasBosquePlantado.radio.requires = IS_INT_IN_RANGE(0, 20)

db.define_table('ParcelasBosqueNatural',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo'),
    Field('numArbol', type = 'integer',
          label = 'Árbol Número', comment='Número del árbol'),
    Field('dap1', type = 'double',
          label = 'Dap1 (m)', comment='Diámetro del árbol a la altura del pecho'),
    Field('dap2', type = 'double',
          label = 'Dap2 (m)', comment='Diámetro del árbol a la altura del pecho'),
    Field('nombreCientifico', db.TipoBNNombreCientifico,
          label = 'Especie', comment='Especie del árbol'),
    Field('rangoEdad', db.TipoRangoEdadNativo,
          label = 'Rango de edad', comment='Rango de edad del árbol'),
    Field('ht', type = 'double',
          label = 'Altura Total (m)', comment='Altura total del árbol'),
    Field('estrato', db.TipoEstrato,
          label = 'Estrato', comment='Estrato'),
    Field('observaciones', type = 'text',
          label = 'Observaciones', comment='Observaciones no contempladas en el formulario')
)

db.ParcelasBosqueNatural.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.ParcelasBosqueNatural.dap1.requires = IS_FLOAT_IN_RANGE(0, 3)
db.ParcelasBosqueNatural.dap2.requires = IS_FLOAT_IN_RANGE(0, 3)
db.ParcelasBosqueNatural.nombreCientifico.requires = IS_IN_DB(db, db.TipoBNNombreCientifico.id, '%(nombreCientifico)s')
db.ParcelasBosqueNatural.rangoEdad.requires = IS_IN_DB(db, db.TipoRangoEdadNativo.id, '%(tipo)s', orderby=db.TipoRangoEdadNativo.id)
db.ParcelasBosqueNatural.ht.requires = IS_FLOAT_IN_RANGE(0, 30)
db.ParcelasBosqueNatural.estrato.requires = IS_IN_DB(db, db.TipoEstrato.id, '%(tipo)s', orderby=db.TipoEstrato.id)

db.define_table('TipoReporte',
            Field('tipo', type='string',
                  label='Tipo de reporte'),
            Field('descripcion', type='string',
                  label='Descripción'),
            format='%(tipo)s'
)
db.TipoReporte.tipo.requires = IS_NOT_EMPTY()
db.TipoReporte.tipo.descripcion = IS_NOT_EMPTY()

db.define_table('MuestreoTipoReporte',
            Field('muestreo', db.Muestreo,
                  label = 'Muestreo', unique=True),
            Field('tipo', db.TipoReporte,label='Tipo de reporte'),
            Field('comentario', type='text',
                  label='Comentario')
)

db.MuestreoTipoReporte.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')
db.MuestreoTipoReporte.tipo.requires = IS_IN_DB(db, db.TipoReporte.id, '%(tipo)s', orderby=db.TipoReporte.id)

db.define_table('Informacion',
            Field('empresa', type='string',
                  label='Empresa'),
            Field('admin', type='string',
                  label='Administrador')
)

db.define_table('Version',
            Field('db_version', type='datetime',
                  label='Último patch')
)

db.define_table('TieneDatos',
    Field('tieneAgua', label="Presencia", type='boolean', default=False),
    Field('tieneFauna', label="Presencia", type='boolean', default=False),
    Field('tieneFlora', label="Presencia", type='boolean', default=False),
    Field('tieneEspeciesInvasoras', label="Presencia", type='boolean', default=False),
    Field('muestreo', db.Muestreo, label = 'Muestreo', unique=True))

db.TieneDatos.muestreo.requires = IS_IN_DB(db, db.Muestreo.id, '%(punto)s - %(anioMuestreo)s')

#Nuevas tablas para sanidad:

db.define_table('TipoEnfermedadPino',
    Field('tipo_enfermedad', type = 'string',
          label = 'Enfermedad', unique=True, notnull=True)
)

db.define_table('TipoOpcionParaEnfermedadPino',
    Field('enfermedad_id', db.TipoEnfermedadPino,
          label = 'Enfermedad', notnull=True),
    Field('opcion', type='string',
          label='Opcion de la Enfermedad', notnull=True)
)

db.define_table('EnfermedadesPino',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo', unique=True),
    Field('numArbol', type = 'integer',
          label = 'Árbol Número'),
    Field('tipo_enfermedad', db.TipoEnfermedadPino,
          label = 'Enfermedad', notnull=True),
    Field('opcion_id', db.TipoOpcionParaEnfermedadPino,
          label = 'Opcion', notnull=True),
)

db.EnfermedadesPino.opcion_id.requires = IS_IN_DB(db, db.TipoOpcionParaEnfermedadPino.id, '%(opcion)s', orderby=db.TipoOpcionParaEnfermedadPino.id)
db.EnfermedadesPino.tipo_enfermedad.requires = IS_IN_DB(db, db.TipoEnfermedadPino.id, '%(tipo_enfermedad)s', orderby=db.TipoEnfermedadPino.id)

db.define_table('TipoEnfermedadEucalyptus',
    Field('tipo_enfermedad', type = 'string',
          label = 'Enfermedad', unique=True, notnull=True)
)

db.define_table('TipoOpcionParaEnfermedadEucalyptus',
    Field('enfermedad_id', db.TipoEnfermedadEucalyptus,
          label = 'Enfermedad', notnull=True),
    Field('opcion', type='string',
          label='Opcion de la Enfermedad', notnull=True)
)

db.define_table('EnfermedadesEucalyptus',
    Field('muestreo', db.Muestreo,
          label = 'Muestreo', unique=True),
    Field('numArbol', type = 'integer',
          label = 'Árbol Número'),
    Field('tipo_enfermedad', db.TipoEnfermedadEucalyptus,
          label = 'Enfermedad', notnull=True),
    Field('opcion_id', db.TipoOpcionParaEnfermedadEucalyptus,
          label = 'Opcion', notnull=True),
)

db.EnfermedadesEucalyptus.opcion_id.requires = IS_IN_DB(db, db.TipoOpcionParaEnfermedadEucalyptus.id, '%(opcion)s', orderby=db.TipoOpcionParaEnfermedadEucalyptus.id)
db.EnfermedadesEucalyptus.tipo_enfermedad.requires = IS_IN_DB(db, db.TipoEnfermedadEucalyptus.id, '%(tipo_enfermedad)s', orderby=db.TipoEnfermedadEucalyptus.id)
