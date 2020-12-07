import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import sys
import requests
import datetime
import os

class covid19galicia:
    
    path = ""
    datefile = ""
    dict_areas = {}
    pop = ""
    initial_dir = ""
    figures_dir = ""
    
    def __init__(self):
        
        self.path = 'https://coronavirus.sergas.gal/infodatos/'
        self.dict_areas={'A.S. A CORUÑA E CEE':'A Coruña',
                         'A.S. FERROL':'Ferrol',
                         'A.S. LUGO, A MARIÑA E MONFORTE':'Lugo',
                         'A.S. OURENSE, VERÍN E O BARCO':'Ourense',
                         'A.S. PONTEVEDRA E O SALNÉS':'Pontevedra',
                         'A.S. SANTIAGO E BARBANZA':'Santiago',
                         'A.S. VIGO':'Vigo'
                        }
        self.areas = ['A Coruña', 'Ferrol', 'Lugo', 'Ourense', 'Pontevedra', 'Santiago', 'Vigo', 'GALICIA']
        file = '_COVID19_Web_CifrasTotais.csv'
        #Obtiene el día 'datefile' más reciente en los ficheros
        for i in range(0,10):
            self.datefile = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            filepath = self.path+self.datefile+file
            response = requests.head(filepath)
            if response.status_code == requests.codes.ok:
                print('Ultima actualización: '+self.datefile)
                break;
            elif i == 9:
                print('Algo ha ido mal. La web lleva muchos días sin actualizarse o ha cambiado su estructura')
                
        self.pop = pd.read_csv('poblacion.csv')
        self.__makeDir()
         
    
    def __makeDir(self):
        self.initial_dir = os.getcwd()
        if not os.path.isdir(self.datefile):
            try:
                os.mkdir(self.datefile)
            except OSError:
                print('No se ha podido crear el directorio')
        self.figures_dir = os.path.join(os.getcwd(), self.datefile) + '\\'
        
    def exit(self):
        os.chdir(self.initial_dir)
    
        
    def getActivosCuradosFallecidos(self):
        file = '_COVID19_Web_ActivosCuradosFallecidos.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        return df
    
    
    def getCifrasTotais(self):
        file = '_COVID19_Web_CifrasTotais.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Fecha'] = [(d[0]) for d in df['Fecha'].str.split(' ')]
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        df = df[df['Area_Sanitaria'] != 'GALICIA']
        
        return df
    
    
    def getFallecidos(self):
        file = '_COVID19_Web_Fallecidos.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        
        return df
    
    def getInfectados(self):
        file = '_COVID19_Web_InfectadosPorFecha.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        return df
    
    
    def getOcupacionCamas(self):
        file = '_COVID19_Web_OcupacionCamasHospital.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Fecha'] = [(d[0]) for d in df['Fecha'].str.split(' ')]
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        df = df[df['Area_Sanitaria'] != 'GALICIA']
        
        return df
    
    
    def getInfeccionesPorFecha(self):
        file = '_COVID19_Web_PorcentajeInfeccionesPorFecha.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Porcentaje_Infecciones'] = [float(p[0].replace(',','.')) for p in df['Porcentaje_Infecciones'].str.split('%')]
        df.rename(columns={'Area_Sanitaria':'Area', 'Casos_Abiertos':'Positivos','Pruebas_PCR_Realizadas':'PCR',
                           'Porcentaje_Infecciones':'%Infecciones'}, inplace=True)
        
        return df
    
    
    def getInfectadosGenero(self):
        file = '_COVID19_Web_PorcentajeInfectadosPorGenero.csv'
        df = pd.read_csv(self.path+self.datefile+file, decimal=',', thousands='.')
        df['Area_Sanitaria'] = df['Area_Sanitaria'].replace(self.dict_areas)
        
        return df
          
    
    def plotCasosActivos(self, casos_activos, cienmil):
        values = []
        title, xlabel, savename = "", "", ""
        offset = 0
        if cienmil:
            df = pd.merge(how='inner', left=casos_activos, right=self.pop, 
                          left_on='Area_Sanitaria', right_on='Area sanitaria')
            df['100.000h'] = round((df['Pacientes_Sin_Alta']*100000)/df['Habitantes'])
            df = df[['Area_Sanitaria','100.000h']].sort_values('100.000h', ascending=True)
            title = 'Casos activos / 100.000 habitantes por área sanitaria'
            xlabel = 'Casos activos/100.000h'
            values = list(df['100.000h'])
            savename = '_casos_activos_100000h.png'
            offset = 5
        else:
            df = casos_activos[['Area_Sanitaria','Pacientes_Sin_Alta']].sort_values('Pacientes_Sin_Alta')
            title = 'Casos activos - Total por área sanitaria'
            xlabel = 'Casos activos'
            values = list(df['Pacientes_Sin_Alta'])
            savename = '_casos_activos_total.png'
            offset = 20
            
        df.plot(kind='barh', x='Area_Sanitaria', legend=False, figsize=(14,8), color='darkcyan', alpha=0.5)
        plt.title(title)
        plt.ylabel('Área sanitaria')
        plt.xlabel(xlabel)
        
        for i,val in enumerate(values):
            label = format(int(val), ',').replace(',','.')
            plt.annotate(label, xy=(val-offset,i), color='white', fontweight='semibold', ha='right', va='center')
        plt.savefig(self.figures_dir+self.datefile+savename)    
        plt.show()
        
        
    def plotPorcentajeAreas(self, casos_activos):
        colors=['lightsteelblue','lavender','honeydew','paleturquoise','moccasin','thistle','mistyrose']
        df = casos_activos[['Area_Sanitaria','Pacientes_Sin_Alta']].sort_values('Pacientes_Sin_Alta')
        df[['Pacientes_Sin_Alta']].plot(kind='pie',labels=df['Area_Sanitaria'],subplots=True,
                                        figsize=(10,10),shadow=True,startangle=90,pctdistance=0.85,
                                        autopct='%1.1f%%',colors=colors,legend=False)

        plt.title('Casos activos - Porcentaje por área sanitaria')
        plt.ylabel(None)
        plt.savefig(self.figures_dir+self.datefile+'_casos_activos_porcentaje.png') 
        plt.show()
        
        
    def calculateAcumulados(self, df, kind, days):
        if days > 0:
            if kind == 'Casos':
                acu = list(df['Positivos'].cumsum())
                for j in range(days,len(acu)+1):
                    acu[j-1] = df['Positivos'].iloc[j-days:j].sum()
            elif kind == 'PCR':
                acu = list(100*(df['Positivos'].cumsum() / df['PCR'].cumsum()))
                for j in range(days,len(acu)+1):
                    acu[j-1] = round(100*(df['Positivos'].iloc[j-days:j].sum() / df['PCR'].iloc[j-days:j].sum()), 2)
            return acu
        else:
            raise ValueError('Invalid days number to calculate acumulated cases')
        
        
    def plotAcumulados(self, daily_data, kind, days):
        areas = ['A Coruña', 'Ferrol', 'Lugo', 'Ourense', 'Pontevedra', 'Santiago', 'Vigo', 'GALICIA']
        colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'magenta', 'olive']

        if kind == 'Casos':
            searched = 'Positivos'
            ylabel = kind
            save_title = '_positivos'
        elif kind == 'PCR':
            searched = '%Infecciones'
            ylabel = '% PCR Positivas'
            save_title = '_PCR_positivas'
        else:
            print("Sólo se permiten 'casos' y 'pcr' como tipos de gráfica")
            return
        
        fig, axes = plt.subplots(4,2)
        fig.set_size_inches(18,32)
        fig.suptitle(ylabel+' '+str(days)+' días por área sanitaria - Evolución', fontsize=22, y=0.92)

        for i,ax in enumerate(axes.flatten()):
            df = daily_data[['Fecha','Positivos','PCR','%Infecciones']][daily_data['Area']==self.areas[i]]
            acu = list(df[searched])
            
            if days > 0:
                acu = self.calculateAcumulados(df, kind, days)
                variation = round((acu[-1]/acu[-2]-1)*100, 1)
                text_print = 'Último valor = {0} ({1:+}%)'.format(acu[-1],variation)
                days_title = '_'+str(days)+'dias'
            else:
                text_print = 'Último valor = ' + str(acu[-1])
                days_title = '_diario'
                                                     
            ax.plot(df['Fecha'],acu,color=colors[i],alpha=0.6)
            ax.text(datetime.datetime.strptime('2020-05-01','%Y-%m-%d'),
                    max(acu)*0.7,
                    text_print, color='black', size=12)
            if kind=='PCR':
                #5% recomendado por OMS
                ax.plot(df['Fecha'],np.full(len(df),5),color='red')
                ax.text(datetime.datetime.strptime('2020-05-01','%Y-%m-%d'), 5.2, 'Recomendado OMS', color='black', size=10)
            ax.grid(alpha=0.3)
            ax.set_title(self.areas[i], fontsize=14)
            ax.set_xlabel(None)
            ax.set_ylabel(ylabel)    

        plt.savefig(self.figures_dir+self.datefile+save_title+days_title+'.png', dpi=90)
        plt.show()
        
    def plotOcupacionCamas(self, camas):
        df = camas.groupby(['Area_Sanitaria']).sum()
        df['Ingresados'] = df['Camas_Ocupadas_HOS'] + df['Camas_Ocupadas_UC']
        df.sort_values('Ingresados', ascending=True, axis=0, inplace=True)
        df.drop(columns=['Ingresados'], axis=1, inplace=True)

        df.plot(kind='barh',stacked=True,figsize=(14,8),alpha=0.5,color=['darkcyan','coral'])
        val_prev = []
        for i,val in enumerate(df['Camas_Ocupadas_HOS']):
            label = format(int(val), ',').replace(',','.')
            plt.annotate(label,xy=(val-1,i),color='white',fontweight='semibold',ha='right',va='center')
            val_prev.append(val)
        for i,val in enumerate(df['Camas_Ocupadas_UC']):
            if not val==0:
                label = format(int(val), ',').replace(',','.')
                plt.annotate(label,xy=(val_prev[i]+val-0.5,i),color='black',fontweight='semibold',ha='right',va='center')

        plt.title('Ocupación actual de camas en Galicia')        
        plt.xlabel('Camas')
        plt.ylabel('Area Sanitaria')
        plt.legend(['Camas ocupadas planta','Camas UCI'])
        plt.savefig(self.figures_dir+self.datefile+'_camas_ocupadas_por_area.png')    
        plt.show()
        
    def getAcumuladosAreas(self, df, days):
        """Genera un dataframe con los casos acumulados para todas las áreas"""
        todos = pd.DataFrame(list(set(df['Fecha'])), columns=['Fecha'])
        todos = todos.sort_values('Fecha', ascending=True)
        todos.set_index('Fecha', drop=True, inplace=True)
        for area in self.dict_areas.values():
            df_area = df[['Fecha','Positivos']][df['Area']==area]
            todos[area] = self.calculateAcumulados(df_area, 'Casos', days)
        return todos
        
    def plotCombinado(self, df):
        """Muestra en un único gráfico la evolución de todas las áreas sanitarias en lo que a incidencia acumulada
        a 7 días se refiere"""
        #Elimina los datos referentes al total de Galicia y comienza donde hay datos de todas las áreas
        df = df[df['Area'] != 'GALICIA']
        df = df[df['Fecha'] >= '2020-03-10']
        #Crea un nuevo dataframe con los casos acumulados a 7 días de cada área como columna
        todos = self.getAcumuladosAreas(df, 7)
        #Dibuja la gráfica
        colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'magenta', 'olive']
        todos.plot(figsize=(18,12), alpha=0.7, color=colors)
        date_max = str(df['Fecha'].max()).split(' ')[0]
        for i,area in enumerate(self.dict_areas.values()):
            plt.text(datetime.datetime.strptime(date_max,'%Y-%m-%d') + timedelta(2), todos[area].tail(1)[0], 
                     area, color=colors[i], size=12)
        plt.grid(alpha=0.3)
        plt.xlabel('Fecha')
        plt.ylabel('Positivos últimos 7 días')
        plt.title('Positivos acumulados en 7 días', fontsize=18)
        plt.legend(loc='upper left')
        plt.xlim('2020-03-10',date.today() + timedelta(30))
        plt.savefig(self.figures_dir+self.datefile+'_casos_activos_agrupado'+'.png') 
        plt.show()
        
    def getIncidenciaConcello(self):
        """Calcula la incidencia por 100.000 habitantes en los últimos 14 días"""
        #Lee el fichero de incidencia acumulada
        inc = pd.read_csv('data-jKpTc.csv')
        casos = []
        for caso in list(inc['CASOS']):
            try:
                casos.append(int(caso.split(': ')[1].split('.')[0]))
            except:
                if caso == 'Número de novos casos diagnosticados no concello: entre 1 e 9.':
                    casos.append(1) #Como no se sabe la cifra concreta, optamos por la menor 
                elif caso == 'Sen novos casos diagnosticados no concello.':
                    casos.append(0)
        inc['CASOS'] = casos
        #Lee el fichero de población por concello
        pop_concellos = pd.read_csv('pop_concellos.csv')
        #Fusiona ambos dataframe en uno único y calcula la incidencia
        fusion = pd.merge(how='inner', left=inc, right=pop_concellos, left_on='ID', right_on='Codigo')
        fusion = fusion[['Municipio', 'Habitantes', 'CASOS']]
        fusion.rename(columns={'CASOS': 'Casos'}, inplace=True)
        fusion['Inc100K'] = (fusion['Casos'] * 100000) // fusion['Habitantes']
        
        return fusion
    
    def plotIncidenciaAcumulada(self, inc14, tipo):
        """Imprime la gráfica de incidencia acumualda por 100.000 habitantes a 14 días"""
        #Habrá 2 tipos de gráfica, la top10 y la ciudades
        if tipo == 'top10':
            df = inc14.sort_values('Inc100K', ascending=False).head(10)
            df = df[['Municipio', 'Inc100K']].sort_values('Inc100K', ascending=True)
            title = 'Top 10 concellos - Casos por 100.000 habitantes a 14 días'
            offset = 30
            save = '_top10_concellos'
        elif tipo == 'ciudades':
            ciudades = ['A Coruña', 'Ferrol', 'Santiago de Compostela', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            df = inc14[inc14['Municipio'].isin(ciudades)]
            df = df[['Municipio','Inc100K']].sort_values('Inc100K', ascending=True)
            title = 'Principales ciudades - Casos por 100.000 habitantes a 14 días'
            offset = 5
            save = '_principales_ciudades'
        else:
            raise ValueError('plotIncidenciaAcumulada only supports top10 and ciudades as tipo')
        df.plot(kind='barh', x='Municipio', legend=False, figsize=(14,8), color='darkcyan', alpha=0.5)
        plt.title(title)
        plt.xlabel('Casos por 100.000 habitantes a 14 días')
        for i,val in enumerate(list(df['Inc100K'])):
            label = format(int(val), ',').replace(',','.')
            plt.annotate(label, xy=(val-offset,i), color='white', fontweight='semibold', ha='right', va='center')
        plt.savefig(self.figures_dir+self.datefile+save+'.png') 
        plt.show()
        
    def plotFallecidos(self, fallecidos):
        fallecidos = fallecidos[fallecidos['Area_Sanitaria'] == 'GALICIA']
        fallecidos = fallecidos[['Fecha', 'Exitus']]
        exitus = list(fallecidos['Exitus'])
        exitus = [(exitus[i]-exitus[i-1]) if i>0 else 0 for i in range(0, len(exitus))]
        fallecidos['Exitus'] = exitus
        fallecidos.set_index('Fecha', inplace=True, drop=True)
        fallecidos.plot(figsize=(16,10), legend=False, grid=True, alpha=0.7)
        plt.grid(alpha=0.3)
        plt.ylim(-1,fallecidos['Exitus'].max()+6)
        plt.title('Fallecidos diarios')
        plt.xlabel('Fecha')
        plt.ylabel('Fallecidos')

        #Anota datos para la 1ª ola
        wave = int(fallecidos[fallecidos.index < '2020-06-15'].sum())
        center = (datetime.datetime.strptime('2020-06-15', '%Y-%m-%d')-datetime.datetime.strptime('2020-03-01', '%Y-%m-%d')).days
        center = (datetime.datetime.strptime('2020-03-01', '%Y-%m-%d') + timedelta(days=center//2)).strftime("%Y-%m-%d")
        level = fallecidos['Exitus'].max()+2
        plt.annotate('', xycoords='data', xy=('2020-03-01',level), xytext=('2020-06-15',level), 
                     arrowprops=dict(arrowstyle='<->', connectionstyle='arc3', color='red', lw=2))
        plt.annotate('1º ola: {} muertos'.format(wave), xy=(center, level+1), ha='center')

        #Anota datos para la 2ª ola
        wave = int(fallecidos[fallecidos.index > '2020-08-01'].sum())
        center = (datetime.datetime.strptime(self.datefile, '%Y-%m-%d')-datetime.datetime.strptime('2020-08-01', '%Y-%m-%d')).days
        center = (datetime.datetime.strptime('2020-08-01', '%Y-%m-%d') + timedelta(days=center//2)).strftime("%Y-%m-%d")
        max_date = fallecidos.index.max()
        plt.annotate('', xycoords='data', xy=('2020-08-01',level), xytext=(max_date,level), 
                     arrowprops=dict(arrowstyle='<->', connectionstyle='arc3', color='red', lw=2))
        plt.annotate('2º ola: {} muertos'.format(wave), xy=(center, level+1), ha='center')
        plt.savefig(self.figures_dir+self.datefile+'_fallecidos'+'.png') 
        plt.show()