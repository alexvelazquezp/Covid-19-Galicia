from classes.covid19galicia import covid19galicia
import pandas as pd

def main():
	#Importamos los datos
	galicia = covid19galicia()
	casos_activos = galicia.getCifrasTotais()
	infectados_fecha = galicia.getInfeccionesPorFecha()
	camas = galicia.getOcupacionCamas()
	fallecidos = galicia.getActivosCuradosFallecidos()
	inc14 = galicia.getIncidenciaConcello()

	#Imprimimos gráficas
	galicia.plotCasosActivos(casos_activos, cienmil=False)
	galicia.plotPorcentajeAreas(casos_activos)
	galicia.plotAcumulados(infectados_fecha, kind='Casos', days=7)
	galicia.plotCombinado(infectados_fecha)
	galicia.plotIncidenciaAcumulada(inc14, 'ciudades')
	galicia.plotIncidenciaAcumulada(inc14, 'top10')
	galicia.plotAcumulados(infectados_fecha, kind='PCR', days=7)
	galicia.plotOcupacionCamas(camas)
	galicia.plotFallecidos(fallecidos)
	print('Proceso finalizado con éxito')

if __name__ == '__main__':
	main()