# Covid-19 Galicia
El propósito del contenido de este repositorio es obtener y analizar los datos relacionados con el impacto de la Covid-19 en Galicia, a partir de los datos publicados por el <a href="https://coronavirus.sergas.gal/Contidos/datos-coronavirus">Sergas en su página web</a>.

Se debe de tener en cuenta que estos datos están organizados por áreas sanitarias, y no por ayuntamientos. Aunque los nombres de las áreas sanitarias coinciden a su vez con nombres de ayuntamientos gallegos, los datos incluyen los de las comarcas y ayuntamientos limítrofes.

Este repositorio está basado en los siguientes Jupyter Notebooks escritos en Python:
<ul>
	<li><b>Población Areas</b>: este cuaderno combina un fichero inicial que relaciona todos los ayuntamientos de Galicia con su respectiva área sanitaria, con los datos de población de los ayuntamientos recogidos en la Wikipedia. De esta forma se obtiene un fichero final llamado <b>poblacion.csv</b>, que contiene el número de habitantes de cada área sanitaria. Esta información será necesaria para los cálculos posteriores basados en 100.000 habitantes.</li>
	<li><b>Covid-19 Galicia</b>: cuaderno principal que descarga de la web del Sergas los ficheros de información correspondientes al último día, y que tras realizar el proceso de data wrangling adecuado, genera un repositorio con una serie de gráficos que analizan el estado actual de forma básica.</li>
</ul>

El resultado de los datos diarios analizados se almacena en un directorio cuyo nombre es la fecha del día, conteniendo a su web las siguientes gráficas:
<ul>
	<li><b>Casos activos totales</b>: número de casos totales vigentes en cada área sanitaria</li>
	<li><b>Casos activos por 100.000 habitantes</b>: número de casos activos por cada 100.000 habitantes del área sanitaria. Se debe tener en cuenta que aunque el Ministerio de Sanidad de España fija un máximo de 500 contagios por 100.000 habitantes como umbral para algunos criterios, este debe ser aplicado por ayuntamiento (dato desconocido) y no por área sanitaria (dato del que sí disponemos). Así, puede haber un área sanitaria con más de 500 casos pero que ninguno de sus ayuntamientos superan este umbral, y situaciones con menos de 500 casos por área pero que sí cuentan con ayuntamientos excediendo el umbral.</li>
	<li><b>Porcentaje de casos activos</b>: porcentaje que los casos activos de un área suponen sobre el total de Galicia.</li>
	<li><b>Positivos diarios</b>: evolución del número de casos positivos reportado cada día en cada área y en el total de Galicia.</li>
	<li><b>Positivos acumulados 7 días</b>: evolución de la suma de los casos positivos reportados en los últimos 7 días en cada área y en el total de Galicia.</li>
	<li><b>Positivos acumulados 14 días</b>evolución de la suma de los casos positivos reportados en los últimos 14 días en cada área y en el total de Galicia.</li>
	<li><b>PCR positivas</b>: evolución diaria del porcentaje de pruebas PCR cuyo resultado ha sido positivo, organizado por áreas y con el total de Galicia. La OMS fija en el 5% el umbral máximo para considerar la pandemia controlada.</li>
	<li><b>PCR positivas 7 días</b>: evolución del porcentaje de PCR positivas teniendo en cuenta los resultados de los últimos 7 días.</li>
	<li><b>PCR positivas 14 días</b>: evolución del porcentaje de PCR positivas teniendo en cuenta los resultados de los últimos 14 días.</li>
	<li><b>Ocupación de camas</b>: número de camas de hospital y camas UCI actuales en cada área sanitaria.</li>
</ul>

Por el momento no se ha realizado ningún análisis de los fallecidos ya que, a diferencia del resto de indicadores, la web del Sergas sólo recoge los datos desde el mes de Julio en lugar de Marzo, comenzando a contar ya desde el acumulado a esa fecha.