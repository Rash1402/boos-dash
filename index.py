import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel("BBDD.xlsx", sheet_name="Hoja1")

st.set_page_config(page_title="Dashboard Boosmap", page_icon="boosmap.png", layout="wide")

#Filtrar por Semana
Semana = ["Todos"] + list( df["Semana2"].unique())
Semana_seleccionada = st.sidebar.selectbox("Semana", Semana)


#Filtrar por Tipo
Tipo = ["Todos"] + list( df["Tipo"].unique())
Tipo_seleccionaada = st.sidebar.selectbox("Tipo de usuario", Tipo)

#Filtrar por Negocio
Negocio =["Todos"] + list( df["Negocio"].unique())
Negocio_seleccionaada = st.sidebar.selectbox("Negocio", Negocio)

#Filtrar por Sub
Sub = ["Todos"] + list( df["Subgerente"].unique())
Sub_seleccionaada = st.sidebar.selectbox("Subgerente", Sub)

#Filtrar por Tm
tm = ["Todos"] + list( df["TM"].unique())
tm_seleccionaada = st.sidebar.selectbox("TM", tm)

#Filtrar por Coordinador
Coordinador = ["Todos"] + list( df["Coordinador"].unique())
Coordinador_seleccionaada = st.sidebar.selectbox("Coordinador", Coordinador)

df_filtrado = df[
    (df["Semana2"]== Semana_seleccionada)&
    (df["Tipo"]== Tipo_seleccionaada) &
    (df["Negocio"]== Negocio_seleccionaada) &
    (df["Subgerente"]== Sub_seleccionaada) &
    (df["TM"]== tm_seleccionaada) &
    (df["Coordinador"]== Coordinador_seleccionaada)
]

df_filtrado = df.copy()

if Semana_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Semana2"] == Semana_seleccionada]
if Tipo_seleccionaada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == Tipo_seleccionaada]    
if Negocio_seleccionaada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Negocio"] == Negocio_seleccionaada]
if Sub_seleccionaada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Subgerente"] == Sub_seleccionaada]
if tm_seleccionaada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["TM"] == tm_seleccionaada]
if Coordinador_seleccionaada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Coordinador"] == Coordinador_seleccionaada]
    


st.image("oracle.png", width=100)
st.image("boosmap_g.png", width=100)
st.title("Dashboard Boosmap") 
st.markdown('''Agosto :calendar:''') 
st.markdown("---")

df_filtrado['Fecha de creación'] = pd.to_datetime(df_filtrado['Fecha de creación'], format='%d/%m/%Y %H:%M')
df_filtrado['Fecha de cierre']= pd.to_datetime(df_filtrado['Fecha de cierre'],format='%d/%m/%Y %H:%M', errors='coerce')
df_filtrado['Tiempo_resolución'] = df_filtrado['Fecha de cierre'] - df_filtrado['Fecha de creación']
df_filtrado['Tiempo_horas'] = df_filtrado['Tiempo_resolución'].dt.total_seconds() / 3600

promedio_general =df_filtrado['Tiempo_horas'].mean()

columnas = ['Pendientes2', 'Fuera de tiempo','En tiempo']

df_largo = df_filtrado.melt(id_vars='Subgerente',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

resumen= df_largo.groupby(['Subgerente','Estado']) ['Valor'].sum().reset_index(name='Total')

totales = resumen[resumen['Estado'] == 'En tiempo']['Total'].sum()

total_general = df_filtrado.shape[0]

porcentaje_global = (totales / total_general) * 100


col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Total de quejas", f"{df_filtrado.shape[0]}")
with col2:
    st.metric("On time", f"{porcentaje_global:.2f} %")  
with col3:
    st.metric("Pendientes", f"{df_filtrado[df_filtrado['Pendientes2'] == 1].shape[0]}")
with col4:
    st.metric("Quemados", f"{df_filtrado[df_filtrado['Fuera de tiempo'] == 1].shape[0]}")


colores= {
    'Pendientes2': '#FFC300',  # Amarillo claro  
    'Fuera de tiempo': '#FF5733',  # Rojo
    'En tiempo': '#28A745'  # Verde
}



columnas = ['Pendientes2', 'Fuera de tiempo','En tiempo']

df_largo = df_filtrado.melt(id_vars='Subgerente',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

df_largo = df_largo[df_largo['Valor'] == 1].drop(columns='Valor')


resumen= df_largo.groupby(['Subgerente', 'Estado'])\
    .size().reset_index(name='Total')    


columnas3 = ['Pendientes2', 'Fuera de tiempo','En tiempo']

df_largo3 = df_filtrado.melt(id_vars='TM',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

df_largo3 = df_largo3[df_largo3['Valor'] == 1].drop(columns='Valor')


resumen3= df_largo3.groupby(['TM', 'Estado'])\
    .size().reset_index(name='Total')    


#calcular el Ontime por subgerente 
en_tiempo = resumen[resumen['Estado'] == 'En tiempo']

total_subgerente = resumen.groupby('Subgerente')['Total'].sum().reset_index(name='Total')
totales_subgerente = en_tiempo.groupby('Subgerente')['Total'].sum().reset_index(name='Total tiempo')

porcentajes = pd.merge(total_subgerente, totales_subgerente, on='Subgerente', suffixes=('_total', '_tiempo'))
porcentajes['Porcentaje'] = ((porcentajes['Total tiempo'] / porcentajes['Total']) * 100).round().astype(int)
porcentajes['Texto'] = porcentajes['Porcentaje'].astype(str) + '%'

#calciular el Ontime por TM
en_tiempo3 = resumen3[resumen3['Estado'] == 'En tiempo']
total_tm = resumen3.groupby('TM')['Total'].sum().reset_index(name='Total')
totales_tm = en_tiempo3.groupby('TM')['Total'].sum().reset_index(name='Total tiempo')   
porcentajes3 = pd.merge(total_tm, totales_tm, on='TM', suffixes=('_total', '_tiempo'))
porcentajes3['Porcentaje'] = ((porcentajes3['Total tiempo'] / porcentajes3['Total']) * 100).round().astype(int)
porcentajes3['Texto'] = porcentajes3['Porcentaje'].astype(str) + '%'


col1, col2 = st.columns(2)
with col1:
    fig = px.bar(resumen, x='Subgerente', y='Total', text='Total', color='Estado',barmode='stack', color_discrete_map=colores)
    fig.add_scatter(x=porcentajes['Subgerente'], y=porcentajes['Porcentaje'], mode='lines+markers+text', name='% On time',yaxis= 'y2', line=dict(color='#0080ff', width=1), text=porcentajes['Texto'], textposition='top center')
    fig.update_layout(title_text='Subgerente', yaxis=dict(title='cantidad',showgrid=False, showticklabels=False), yaxis2=dict(title='% On time', overlaying='y',side='right', range=[0,100], showgrid=False, showticklabels=False), xaxis_title='Subgerente')
    st.plotly_chart(fig)


with col2:
      fig = px.bar(resumen3, x='TM', y='Total', text='Total', color='Estado',barmode='stack',color_discrete_map=colores)
      fig.add_scatter(x=porcentajes3['TM'], y=porcentajes3['Porcentaje'], mode='lines+markers+text', name='% On time',yaxis= 'y2', line=dict(color='#0080ff', width=1), text=porcentajes3['Texto'], textposition='top center')   
      fig.update_layout(title_text='TM', yaxis=dict(title='cantidad',showgrid=False, showticklabels=False), yaxis2=dict(title='% On time', overlaying='y',side='right', range=[0,100], showgrid=False, showticklabels=False), xaxis_title='TM')
      st.plotly_chart(fig)



columnas2 = ['Pendientes2', 'Fuera de tiempo','En tiempo']

df_largo2 = df_filtrado.melt(id_vars='Coordinador',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

df_largo2 = df_largo2[df_largo2['Valor'] == 1].drop(columns='Valor')

resumen2= df_largo2.groupby(['Coordinador', 'Estado'])\
    .size().reset_index(name='Total') 


#calcular el Ontime por Coordinador
en_tiempo2 = resumen2[resumen2['Estado'] == 'En tiempo']
total_coordinador = resumen2.groupby('Coordinador')['Total'].sum().reset_index(name='Total')
totales_coordinador = en_tiempo2.groupby('Coordinador')['Total'].sum().reset_index(name='Total tiempo')
porcentajes2 = pd.merge(total_coordinador, totales_coordinador, on='Coordinador', suffixes=('_total', '_tiempo'))
porcentajes2['Porcentaje'] = ((porcentajes2['Total tiempo'] / porcentajes2['Total']) * 100).round().astype(int)
porcentajes2['Texto'] = porcentajes2['Porcentaje'].astype(str) + '%'



fig = px.bar(resumen2, x='Coordinador', y='Total', text='Total', color='Estado',barmode='stack',color_discrete_map=colores)
fig.add_scatter(x=porcentajes2['Coordinador'], y=porcentajes2['Porcentaje'], mode='lines+markers+text', name='% On time',yaxis= 'y2', line=dict(color='#0080ff', width=1), text=porcentajes2['Texto'], textposition='top center')
fig.update_layout(title_text='Coordinador', yaxis=dict(title='cantidad',showgrid=False, showticklabels=False), yaxis2=dict(title='% On time', overlaying='y',side='right', range=[0,100], showgrid=False, showticklabels=False), xaxis_title='Coordinador')
st.plotly_chart(fig)

st.subheader("Categorías y comportamiento 🚨")
st.markdown("---")



columnas = ['Fuera de tiempo','En tiempo']

df_largo = df_filtrado.melt(id_vars='Semana2',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

df_largo = df_largo[df_largo['Valor'] == 1].drop(columns='Valor')


resumen= df_largo.groupby(['Semana2', 'Estado'])\
    .size().reset_index(name='Total')  


#calcular el Ontime por Semana
en_tiempo = resumen[resumen['Estado'] == 'En tiempo']
total_semana = resumen.groupby('Semana2')['Total'].sum().reset_index(name='Total')
totales_semana = en_tiempo.groupby('Semana2')['Total'].sum().reset_index(name='Total tiempo')
porcentajes_semana = pd.merge(total_semana, totales_semana, on='Semana2', suffixes=('_total', '_tiempo'))
porcentajes_semana['Porcentaje'] = ((porcentajes_semana['Total tiempo'] / porcentajes_semana['Total']) * 100).round().astype(int)
porcentajes_semana['Texto'] = porcentajes_semana['Porcentaje'].astype(str) + '%'



col1, col2 = st.columns(2)
with col1:
    fig = px.bar(resumen, x='Semana2', y='Total', text='Total', color='Estado',barmode='stack', color_discrete_map=colores)
    fig.add_scatter(x=porcentajes_semana['Semana2'], y=porcentajes_semana['Porcentaje'], mode='lines+markers+text', name='% On time',yaxis= 'y2', line=dict(color='#0080ff', width=1), text=porcentajes_semana['Texto'], textposition='top center')
    fig.update_layout(title_text='Semana', yaxis=dict(title='cantidad',showgrid=False, showticklabels=False), yaxis2=dict(title='% On time', overlaying='y',side='right', range=[0,100], showgrid=False, showticklabels=False), xaxis_title='Semana')
    st.plotly_chart(fig)



    

    columnas = ['Fuera de tiempo','En tiempo']

    df_largo = df_filtrado.melt(id_vars='Día',
                                value_vars=columnas,
                                var_name='Estado',
                                value_name='Valor')

    df_largo = df_largo[df_largo['Valor'] == 1].drop(columns='Valor')


    resumen= df_largo.groupby(['Día', 'Estado'])\
        .size().reset_index(name='Total')

    # Reordenar los días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    resumen['Día'] = pd.Categorical(resumen['Día'], categories=dias_semana, ordered=True)
    resumen = resumen.sort_values('Día')  

    #calcular el ontime por Día
    en_tiempo = resumen[resumen['Estado'] == 'En tiempo']
    total_dia = resumen.groupby('Día')['Total'].sum().reset_index(name='Total')
    totales_dia = en_tiempo.groupby('Día')['Total'].sum().reset_index(name='Total tiempo')
    porcentajes_dia = pd.merge(total_dia, totales_dia, on='Día', suffixes=('_total', '_tiempo'))
    porcentajes_dia['Porcentaje'] = ((porcentajes_dia['Total tiempo'] / porcentajes_dia['Total']) * 100).round().astype(int)
    porcentajes_dia['Texto'] = porcentajes_dia['Porcentaje'].astype(str) + '%'

    ordenar_porcentajes = pd.Categorical(porcentajes_dia['Día'], categories=dias_semana, ordered=True)
    porcentajes_dia= porcentajes_dia.sort_values('Día')
    
    with col2: 
        fig = px.bar(resumen, x='Día', y='Total', text='Total', color='Estado',barmode='stack', color_discrete_map=colores)
        fig.add_scatter(x=porcentajes_dia['Día'], y=porcentajes_dia['Porcentaje'], mode='lines+markers+text', name='% On time',yaxis= 'y2', line=dict(color='#0080ff', width=1), text= porcentajes_dia['Texto'], textposition='top center')
        fig.update_layout(title_text='Día', yaxis=dict(title='cantidad',showgrid=False, showticklabels=False), yaxis2=dict(title='% On time', overlaying='y',side='right', range=[0,100], showgrid=False, showticklabels=False), xaxis_title='Día')
        st.plotly_chart(fig)



columnas = ['Fuera de tiempo','En tiempo']

df_largo = df_filtrado.melt(id_vars='Categoría',
                            value_vars=columnas,
                            var_name='Estado',
                            value_name='Valor')

df_largo = df_largo[df_largo['Valor'] == 1].drop(columns='Valor')

# Crear resumen
resumen = df_largo.groupby(['Categoría', 'Estado'])\
    .size().reset_index(name='Total')  

# Calcular el total por categoría
total_categoria = resumen.groupby('Categoría')['Total'].sum().reset_index(name='Total')

# 🔁 ORDENAMOS de mayor a menor
total_categoria = total_categoria.sort_values(by='Total', ascending=True)
orden_categorias = total_categoria['Categoría']

# Reordenamos el resumen usando pd.Categorical
resumen['Categoría'] = pd.Categorical(resumen['Categoría'], categories=orden_categorias, ordered=True)
resumen = resumen.sort_values('Categoría')

# Calculamos on-time
en_tiempo = resumen[resumen['Estado'] == 'En tiempo']
totales_categoria = en_tiempo.groupby('Categoría')['Total'].sum().reset_index(name='Total tiempo')

porcentajes_categoria = pd.merge(total_categoria, totales_categoria, on='Categoría', suffixes=('_total', '_tiempo'))
porcentajes_categoria['Porcentaje'] = ((porcentajes_categoria['Total tiempo'] / porcentajes_categoria['Total']) * 100).round().astype(int)
porcentajes_categoria['Texto'] = porcentajes_categoria['Porcentaje'].astype(str) + '%'

# Reordenamos porcentajes para que coincidan con el orden de las barras
porcentajes_categoria['Categoría'] = pd.Categorical(porcentajes_categoria['Categoría'], categories=orden_categorias, ordered=True)
porcentajes_categoria = porcentajes_categoria.sort_values('Categoría')

# Gráfica
fig = px.bar(
    resumen,
    x='Categoría',
    y='Total',
    text='Total',
    color='Estado',
    barmode='stack',
    color_discrete_map=colores
)

fig.add_scatter(
    x=porcentajes_categoria['Categoría'],
    y=porcentajes_categoria['Porcentaje'],
    mode='lines+markers+text',
    name='% On time',
    yaxis='y2',
    line=dict(color='#0080ff', width=1),
    text=porcentajes_categoria['Texto'],
    textposition='top center'
)

fig.update_layout(
    title_text='Categoría',
    yaxis=dict(title='Cantidad',showgrid=False, showticklabels=False),
    yaxis2=dict(title='% On time', overlaying='y', side='right', range=[0, 100], showgrid=False, showticklabels=False),
    xaxis_title='Categoría'
)

st.plotly_chart(fig)


st.subheader("Quejas Tienda 🛍️")

st.markdown("---")  


#grafica de quejas
df_tienda = df[df['Tipo'] == 'Tiendas']

resumen_cat = df_tienda.groupby('Subcategoría').size().reset_index(name='Total')
resumen_cat = resumen_cat.sort_values('Total',ascending=True)

fig = px.bar(resumen_cat,
             x='Total',
             y='Subcategoría',
             orientation='h',
             text='Total',
             color='Total',
             color_continuous_scale='purples')

fig.update_layout(title='Total por Tienda',
                  xaxis_title='Cantidad',
                  yaxis_title='Tienda')

st.plotly_chart(fig)                                      




# Agrupar por subcategoría y concatenar los asuntos
tabla_resumen = df[df['Tipo'] == 'Tiendas'].groupby('Subcategoría').agg({
    'Asunto': lambda x: '\n'.join(x.unique()),
    'Asunto': 'count'  # esto dará el total de casos
}).rename(columns={'Asunto': 'Casos', '<lambda_0>': 'Asuntos'})

# Como ya se sobreescribió 'Asunto', debemos hacerlo en 2 pasos:
asuntos_concat = df[df['Tipo'] == 'Tiendas'].groupby('Subcategoría')['Asunto'].agg(lambda x: '\n'.join(x.unique()))
casos_count = df[df['Tipo'] == 'Tiendas'].groupby('Subcategoría')['Asunto'].count()

# Juntamos ambos
tabla_resumen = pd.DataFrame({
    'Asuntos': asuntos_concat,
    'Casos': casos_count
}).reset_index()

# Mostrar en streamlit
st.dataframe(tabla_resumen)


