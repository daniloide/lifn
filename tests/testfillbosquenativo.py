#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import os

HOME = os.path.expanduser("~")
WEB2PY_PATH=os.path.join( HOME, "workspace", "web2py" )

PROTO = "http"
HOST = "127.0.0.1"
PORT = 8000
APP_NAME = "lifn"
APP_PATH = os.path.join( HOME, "workspace", APP_NAME )

BASE_URL = "%s://%s:%s/%s" % (PROTO, HOST, PORT, APP_NAME)


class TestFillBosqueNativo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = BASE_URL
        self.verificationErrors = []
        self.accept_next_alert = True

    def _test_fill_noinfo(self):
        driver = self.driver

        # login
        driver.get(self.base_url + "/default/user/login")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("auth_user_remember").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual(self.base_url + "/default/index", driver.current_url)

        ### Begin No data
        # Ausencia de bosque
        driver.find_element_by_link_text("Inicio").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//tr[@id='2057']/td[12]/a/i").click()
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[1]/li").click()
        driver.find_element_by_id("bAusenciaBosque").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Bosque cortado
        driver.find_element_by_link_text("Inicio").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//tr[@id='2060']/td[12]/a/i").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[1]/li").click()
        driver.find_element_by_id("bBosqueCortado").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # No se peude ingresar
        driver.find_element_by_link_text("Inicio").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//tr[@id='2061']/td[12]/a/i").click()
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[1]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("bNoSePuedeIngresar").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)


    def test_fill_bosquenativo(self):
        driver = self.driver

        # login
        driver.get(self.base_url + "/default/user/login")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("auth_user_remember").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual(self.base_url + "/default/index", driver.current_url)

        ### Begin: Bosque nativo
        driver.find_element_by_link_text("Inicio").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//tr[@id='2062']/td[12]/a/i").click()
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[1]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("comentario").clear()
        driver.find_element_by_id("comentario").send_keys("Este es el comentario")
        driver.find_element_by_id("bInfoRelevada").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Datos generales
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[2]/li").click()
        """
        from selenium.webdriver.support.ui import Select
        select = Select(driver.find_element_by_name(‘name’))
        select.select_by_index(index)
        select.select_by_visible_text(“text”)
        select.select_by_value(value)
        """
        select = Select( driver.find_element_by_id("DatosGenerales_tipoDeBosque") )
        select.select_by_visible_text("Bosque Nativo");
        select = Select( driver.find_element_by_id("subbosque") )
        select.select_by_visible_text("Galería");
        driver.find_element_by_id("DatosGenerales_fecha").clear()
        driver.find_element_by_id("DatosGenerales_fecha").send_keys("16/06/2013")
        select = Select( driver.find_element_by_id("DatosGenerales_facilidadProgresion") )
        select.select_by_visible_text("Fácil");
        select = Select( driver.find_element_by_id("DatosGenerales_departamento") )
        select.select_by_visible_text("Artigas");
        driver.find_element_by_id("DatosGenerales_propietario").clear()
        driver.find_element_by_id("DatosGenerales_propietario").send_keys("El Propietario del Predio")
        driver.find_element_by_id("DatosGenerales_predio").clear()
        driver.find_element_by_id("DatosGenerales_predio").send_keys("El Nombre del Predio")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Distancias
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[3]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("Distancias_carreteraCaminoVecinal").clear()
        driver.find_element_by_id("Distancias_carreteraCaminoVecinal").send_keys("5")
        driver.find_element_by_id("Distancias_caminoVecinalCaminoAcceso").click()
        driver.find_element_by_id("Distancias_caminoVecinalCaminoAcceso").clear()
        driver.find_element_by_id("Distancias_caminoVecinalCaminoAcceso").send_keys("2")
        driver.find_element_by_id("Distancias_caminoAccesoPuntoGPS").click()
        driver.find_element_by_id("Distancias_caminoAccesoPuntoGPS").clear()
        driver.find_element_by_id("Distancias_caminoAccesoPuntoGPS").send_keys("600")
        driver.find_element_by_id("Distancias_puntoGPSCentroParcela").click()
        driver.find_element_by_id("Distancias_puntoGPSCentroParcela").clear()
        driver.find_element_by_id("Distancias_puntoGPSCentroParcela").send_keys("20")
        driver.find_element_by_id("Distancias_rumboCaminoCentroParcela").click()
        driver.find_element_by_id("Distancias_rumboCaminoCentroParcela").clear()
        driver.find_element_by_id("Distancias_rumboCaminoCentroParcela").send_keys("5")
        fileInput = driver.find_element_by_xpath("//input[@name='file' and @type='file']")
        fileInput.send_keys( os.path.abspath( os.path.join("gpx", "test1_small.gpx") ) )
        time.sleep(5)
        driver.find_element_by_id("fakeSave").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Fotos
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[4]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        select = Select( driver.find_element_by_id("Fotos_tipoFoto") )
        select.select_by_visible_text("Carretera a Camino Vecinal");
        driver.find_element_by_id("Fotos_descr").click()
        driver.find_element_by_id("Fotos_descr").clear()
        driver.find_element_by_id("Fotos_descr").send_keys(u"Descripción 1")
        driver.find_element_by_id("Fotos_lat").click()
        driver.find_element_by_id("Fotos_lat").clear()
        driver.find_element_by_id("Fotos_lat").send_keys("-33.3333333")
        driver.find_element_by_id("Fotos_lon").click()
        driver.find_element_by_id("Fotos_lon").clear()
        driver.find_element_by_id("Fotos_lon").send_keys("-55.5555555")
        fileInput = driver.find_element_by_xpath("//input[@name='file' and @type='file']")
        fileInput.send_keys( os.path.abspath( os.path.join("images", "test1_big_noGPS.jpg") ) )
        time.sleep(5)
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//input[@value='View all']").click()
        driver.find_element_by_xpath("//div[@class='galleria-image-nav-left']").click()
        driver.find_element_by_xpath("//body").click()

        # Coordenadas parcela
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[5]/li").click()
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[5]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("CoordenadasParcela_sur").clear()
        driver.find_element_by_id("CoordenadasParcela_sur").send_keys("-33.2283")
        driver.find_element_by_id("CoordenadasParcela_oeste").click()
        driver.find_element_by_id("CoordenadasParcela_oeste").clear()
        driver.find_element_by_id("CoordenadasParcela_oeste").send_keys("-55.0578")
        driver.find_element_by_id("CoordenadasParcela_altitud").click()
        driver.find_element_by_id("CoordenadasParcela_altitud").clear()
        driver.find_element_by_id("CoordenadasParcela_altitud").send_keys("10")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Equipo tabajo
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[6]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("EquipoTrabajo_cargo").clear()
        driver.find_element_by_id("EquipoTrabajo_cargo").send_keys("Encargado de grupo")
        driver.find_element_by_id("EquipoTrabajo_nombre").click()
        driver.find_element_by_id("EquipoTrabajo_nombre").clear()
        driver.find_element_by_id("EquipoTrabajo_nombre").send_keys("El Encargado")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Observacioens
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[7]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("Observaciones_observacion").clear()
        driver.find_element_by_id("Observaciones_observacion").send_keys("Las observaciones")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Agua
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[8]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("haveDataYes").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        self.setSelect("Agua_tipoCaudal", "Arroyo")
        driver.find_element_by_id("Rio").clear()
        driver.find_element_by_id("Rio").send_keys("Cuareim")
        driver.find_element_by_id("distRio").clear()
        driver.find_element_by_id("distRio").send_keys("500")
        driver.find_element_by_id("manejo_Yes").click()
        self.setSelect("Agua_frecuencia", "Permanente")
        driver.find_element_by_id("acuacultura_Yes").click()
        self.setSelect("Agua_gradoContaminacion", "Bajo")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Fauna
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[9]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("haveDataYes").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("T")
        driver.find_element_by_id("res0").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("A")
        driver.find_element_by_id("res0").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("C")
        driver.find_element_by_id("res0").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)


        # Relieve
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[10]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        self.setSelect("Relieve_ubicacion", "Plano")
        self.setSelect("Relieve_exposicion", "Plano")
        driver.find_element_by_id("Relieve_pendiente").clear()
        driver.find_element_by_id("Relieve_pendiente").send_keys("2")
        self.setSelect("Relieve_formaPendiente", "Convexa")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)


        # Suelo
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[11]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        self.setSelect("Suelo_grupoConeat", "1.10a")
        self.setSelect("Suelo_usoTierra", "Forestal")
        self.setSelect("Suelo_usoPrevio", "Pradera")
        self.setSelect("Suelo_gradoErosion", "Ligera")
        self.setSelect("Suelo_tipoErosion", "Laminar")
        self.setSelect("Suelo_profundidadPrimerHorizonte", "Superficial")
        self.setSelect("Suelo_grupoConeat", "1.10a")
        self.setSelect("Suelo_grupoConeat", "1.10a")
        self.setSelect("Suelo_grupoConeat", "1.10a")

        driver.find_element_by_id("impedimento_Yes").click()
        driver.find_element_by_id("olor_Yes").click()
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_id("Suelo_pedregosidad").click()
        driver.find_element_by_id("Suelo_pedregosidad").clear()
        driver.find_element_by_id("Suelo_pedregosidad").send_keys("2")
        driver.find_element_by_id("Suelo_rocosidad").click()
        driver.find_element_by_id("Suelo_rocosidad").clear()
        driver.find_element_by_id("Suelo_rocosidad").send_keys("5")
        driver.find_element_by_id("faunaSuelo_Yes").click()
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Cobertura vegetal
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[12]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[13]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=ProductosNoMadereros_tipoGanado | label=Vacuno]]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=ProductosNoMadereros_sistemasProduccion | label=Forrajera]]
        driver.find_element_by_css_selector("#ProductosNoMadereros_sistemasProduccion > option[value=\"5\"]").click()
        driver.find_element_by_id("produccionApicola_Yes").click()
        driver.find_element_by_id("rompeVientos_Yes").click()
        driver.find_element_by_id("aceitesEsenciales_Yes").click()
        driver.find_element_by_id("actividadesCasaPesca_Yes").click()
        driver.find_element_by_id("estudiosCientificos_Yes").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        # Productos no madereros
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[14]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("haveDataYes").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=Flora_tipoSotobosque | label=Leñoso]]
        driver.find_element_by_id("Flora_alturaSotobosque").click()
        driver.find_element_by_id("Flora_alturaSotobosque").clear()
        driver.find_element_by_id("Flora_alturaSotobosque").send_keys("5")
        driver.find_element_by_link_text("Agregar Registro").click()
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("A")
        driver.find_element_by_id("res0").click()
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_id("saveFloraSuelo").click()
        self.assertEqual("Se guardo con exito!", self.close_alert_and_get_its_text())

        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[15]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("pobreCalidadAgua_Yes").click()
        driver.find_element_by_id("perdidaFertilidad_Yes").click()
        driver.find_element_by_id("presenciaPesticidas_Yes").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[16]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        # ERROR: Caught exception [ERROR: Unsupported command [addSelection | id=Fuego_evidenciaFuego | label=Sin Evidencias]]
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[17]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("haveDataYes").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("A")
        driver.find_element_by_id("res0").click()
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)

        driver.find_element_by_xpath("//ul[@id='menuLateral']/a[18]/li").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("ParcelasBosqueNatural_numArbol").clear()
        driver.find_element_by_id("ParcelasBosqueNatural_numArbol").send_keys("1")
        driver.find_element_by_id("ParcelasBosqueNatural_dap1").click()
        driver.find_element_by_id("ParcelasBosqueNatural_dap1").clear()
        driver.find_element_by_id("ParcelasBosqueNatural_dap1").send_keys("0.5")
        driver.find_element_by_id("ParcelasBosqueNatural_dap2").click()
        driver.find_element_by_id("ParcelasBosqueNatural_dap2").clear()
        driver.find_element_by_id("ParcelasBosqueNatural_dap2").send_keys("0.7")
        driver.find_element_by_id("nomCientifico").click()
        driver.find_element_by_id("nomCientifico").clear()
        driver.find_element_by_id("nomCientifico").send_keys("A")
        driver.find_element_by_id("res0").click()
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_id("ParcelasBosqueNatural_ht").click()
        driver.find_element_by_id("ParcelasBosqueNatural_ht").clear()
        driver.find_element_by_id("ParcelasBosqueNatural_ht").send_keys("12")
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_id("ParcelasBosqueNatural_observaciones").click()
        driver.find_element_by_id("ParcelasBosqueNatural_observaciones").clear()
        driver.find_element_by_id("ParcelasBosqueNatural_observaciones").send_keys("las observacioens")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_link_text("Inicio").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        """

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def setSelect(self, selId, selText):
        select = Select( self.driver.find_element_by_id( selId ) )
        select.select_by_visible_text( selText )

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
