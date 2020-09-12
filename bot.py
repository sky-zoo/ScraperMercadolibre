from selenium.webdriver import Firefox
from time import sleep
from datetime import datetime as dt
from datetime import date

class Scraper:

    driver = Firefox(executable_path="bin/geckodriver.exe")

    def __init__(self, url):    
        self.url = url
        self.driver.get(self.url)
    
    def buscar(self, busqueda):
        """
            Busca algo en la pagina de mercadolibre.
            Precondicion: se debe ingresar el objeto a buscar, el valor ingresado debe ser un string.
        """
        sleep(2)
        buscador = self.driver.find_element_by_xpath("/html/body/header/div/form/input")
        buscador.send_keys(busqueda)
        boton_buscar = self.driver.find_element_by_xpath("/html/body/header/div/form/button")
        boton_buscar.click()
    
    def conseguirInfo(self):
        """
            Obtiene titulo y precio de las publicaciones, las publicaciones se encuentran en capital federal.
            Postcondicion: devuelve un diccionario con los datos de todas las publicaciones.
        """
        # sleep(2)
        filtradoEnCapitalFederal = self.driver.find_element_by_xpath("/html/body/main/div/div[1]/aside/section[2]/dl[7]/dd[1]/a")
        filtradoEnCapitalFederal.click()
        sleep(2)
        filtradoPorObjetosNuevos = self.driver.find_element_by_xpath("/html/body/main/div/div/aside/section[3]/dl[6]/dd[1]/a")
        filtradoPorObjetosNuevos.click()
        sleep(2)

        objetos = self.driver.find_elements_by_class_name("ui-search-layout__item")
        resultadosBusqueda = {}
        for elemento in range(len(objetos)):
            titulo = objetos[elemento].find_element_by_class_name("ui-search-item__title").text
            precio = objetos[elemento].find_element_by_class_name("price-tag-fraction").text
            publicacionURL = objetos[elemento].find_element_by_css_selector(".ui-search-item__group__element.ui-search-link").get_attribute("href")

            if elemento not in resultadosBusqueda:
                resultadosBusqueda[elemento] = {
                    "titulo": titulo,
                    "precio": precio,
                    "URL": publicacionURL
                }
        return resultadosBusqueda

    def guardarDatosBusqueda(self, resultadosBusqueda):
        """
            Guarda toda la informacion en un archivo de texto plano.
            Precondicion: debe ingresarse un diccionario que contenga los datos de la busqueda realizada.
        """

        with open("publicaciones.txt", "w") as archivo:
            if dt.now().minute < 10:
                archivo.write(f"**FECHA Y HORA DE BUSQUEDA: {date.today()} , {dt.now().hour}:0{dt.now().minute}hs **\n\n")
            else:
                archivo.write(f"**FECHA Y HORA DE BUSQUEDA: {date.today()} , {dt.now().hour}:{dt.now().minute}hs**\n\n")
            for resultado in resultadosBusqueda:
                archivo.write(f"Resultado {resultado+1}:\n")
                archivo.write(f"--Titulo: {resultadosBusqueda[resultado]['titulo']}\n")
                archivo.write(f"--Precio: ${resultadosBusqueda[resultado]['precio']}\n")
                archivo.write(f"--URL: {resultadosBusqueda[resultado]['URL']}\n\n\n")

    def ordenarPorPrecioAscendente(self, resultadosBusqueda):
        """
            TODO: hacer que este metodo ordene el diccionario con las publicaciones, con precio
            ascendente
        """


        # for resultado in resultadosBusqueda:
        #     if 
            # pass
    
x = Scraper("https://www.mercadolibre.com.ar/")
x.buscar("teclado")
data = x.conseguirInfo()
x.guardarDatosBusqueda(data)