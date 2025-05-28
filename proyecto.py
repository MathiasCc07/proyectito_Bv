# autores: Matias Alexander Copa Catari
#         Gael Colomo Ramos
# fecha: 22/05/2025
# Version: 3.0

import streamlit as st
import pandas as pd

productos = sorted([
    "papa imilla", "papa huaycha", "zanahoria", "cebolla", "tomate", "lechuga", "nabo", "ají amarillo",
    "queso criollo", "leche fresca", "huevos de campo", "pan de batalla", "arroz grano de oro", "harina integral",
    "charque", "carne de res", "pollo fresco", "trucha del lago", "pescado seco", 
    "ropa de alpaca", "chompas artesanales", "mantas tejidas", "bolsos de aguayo", 
    "miel pura", "jarabe de coca", "té de muña", "licor de caña", "yogurt natural",
    "jabón artesanal", "shampoo de quinua", "crema de sábila", "vinagre de manzana"
])

ingredientes_por_plato = {
    "Silpancho": {
        "arroz (g)": 100,
        "papa (g)": 150,
        "carne (g)": 100,
        "huevo (unidad)": 1
    },
    "Pique Macho": {
        "papa (g)": 200,
        "carne (g)": 150,
        "salchicha (g)": 100,
        "tomate (g)": 50
    },
    "Majadito": {
        "arroz (g)": 120,
        "charque (g)": 100,
        "plátano (unidad)": 1,
        "huevo (unidad)": 1
    }
}

def calcular_ingredientes(cantidades, ingredientes_por_plato):
    totales = {}
    for plato in cantidades:
        cantidad = cantidades[plato]
        for ingrediente, cantidad_por_porcion in ingredientes_por_plato[plato].items():
            if ingrediente in totales:
                totales[ingrediente] += cantidad * cantidad_por_porcion
            else:
                totales[ingrediente] = cantidad * cantidad_por_porcion
    return totales

def buscar_producto(lista, producto_buscado):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == producto_buscado:
            return medio
        elif lista[medio] < producto_buscado:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

categorias = {
    "Verduras": ["papa imilla", "papa huaycha", "zanahoria", "cebolla", "tomate", "lechuga", "nabo", "ají amarillo"],
    "Frutas": ["plátano"],
    "Lácteos": ["queso criollo", "leche fresca", "yogurt natural"],
    "Carnes y huevos": ["charque", "carne de res", "pollo fresco", "trucha del lago", "pescado seco", "huevos de campo"],
    "Pan y cereales": ["pan de batalla", "arroz grano de oro", "harina integral"],
    "Bebidas y otros": ["miel pura", "jarabe de coca", "té de muña", "licor de caña"],
    "Artesanías": ["ropa de alpaca", "chompas artesanales", "mantas tejidas", "bolsos de aguayo"],
    "Cuidado personal": ["jabón artesanal", "shampoo de quinua", "crema de sábila", "vinagre de manzana"]
}

def pagina_mercado():
    st.header("Mercado Digital Bolivia")
    opcion = st.radio("¿Qué quieres hacer?", ["Ver productos por categoría", "Buscar un producto"])

    if opcion == "Ver productos por categoría":
        for categoria, items in categorias.items():
            st.subheader(categoria)
            for producto in sorted(items):
                st.write("-", producto)

    elif opcion == "Buscar un producto":
        producto_buscado = st.text_input("Escribe el nombre exacto del producto:").lower()
        if st.button("Buscar"):
            lista_completa = sorted([item for sublist in categorias.values() for item in sublist])
            indice = buscar_producto(lista_completa, producto_buscado)
            if indice != -1:
                st.success(f"Producto encontrado: '{producto_buscado}' en la posición {indice}.")
            else:
                st.error("Producto no encontrado.")


def pagina_calculadora():
    st.header("Calculadora de Ingredientes")
    cantidades = {}
    for plato in ingredientes_por_plato.keys():
        cantidades[plato] = st.number_input(f"¿Cuántas porciones de {plato} quieres preparar?", min_value=0, step=1)

    if st.button("Calcular ingredientes"):
        totales = calcular_ingredientes(cantidades, ingredientes_por_plato)

        data = []
        for ingrediente, cantidad_total in totales.items():
            platos_usados = []
            for plato, ingredientes in ingredientes_por_plato.items():
                if ingrediente in ingredientes:
                    platos_usados.append(plato)
            data.append({
                "Ingrediente": ingrediente,
                "Cantidad Total": cantidad_total,
                "Platos Relacionados": ", ".join(platos_usados)
            })

        df = pd.DataFrame(data)
        st.subheader("Ingredientes Totales Necesarios")
        st.dataframe(df)

        total_porciones = sum(cantidades.values())
        st.markdown(f"Total de porciones solicitadas: {total_porciones}")

def main():
    st.sidebar.title("Menú")
    pagina = st.sidebar.selectbox("Selecciona la página", ["Mercado", "Calculadora"])

    if pagina == "Mercado":
        pagina_mercado()
    else:
        pagina_calculadora()

if __name__ == "__main__":
    main()
