# IMPORTAMOS FLASK
from flask import Flask, render_template, request

# IMPORTAMOS MYSQL
import mysql.connector


# CONEXIÓN CON LA BASE DE DATOS

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="par_impar"
)

print("Conexión exitosa")


# CREAR LA APLICACIÓN FLASK

app = Flask(__name__)


# CLASE 1: PAR O IMPAR

class ParImpar:

    def comprobar(self, numero):

        if numero % 2 == 0:
            resultado = "El número es par"
        else:
            resultado = "El número es impar"

        # Guardar en MySQL
        cursor = conexion.cursor()

        sql = """
        INSERT INTO resultados (numero, resultado)
        VALUES (%s, %s)
        """

        valores = (numero, resultado)

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()

        return resultado


# CLASE 2: TABLA DE MULTIPLICAR

class TablaMultiplicar:

    def generar(self, numero):

        tabla = []

        for i in range(1, 11):

            resultado = numero * i

            tabla.append(
                f"{numero} x {i} = {resultado}"
            )

        # Convertimos la lista en un texto
        tabla_texto = "\n".join(tabla)

        # Guardar en MySQL
        cursor = conexion.cursor()

        sql = """
        INSERT INTO tablas_multiplicar (numero, tabla_generada)
        VALUES (%s, %s)
        """

        valores = (numero, tabla_texto)

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()

        return tabla


# CLASE 3: ADIVINA EL NÚMERO

class AdivinaNumero:

    def comprobar(self, intento):

        numero_secreto = 7

        while True:

            if intento < numero_secreto:

                mensaje = "El número es mayor"
                break

            elif intento > numero_secreto:

                mensaje = "El número es menor"
                break

            else:

                mensaje = "¡Correcto! Adivinaste el número"
                break

        # Guardar en MySQL
        cursor = conexion.cursor()

        sql = """
        INSERT INTO adivina_numero
        (intento, numero_secreto, mensaje)
        VALUES (%s, %s, %s)
        """

        valores = (
            intento,
            numero_secreto,
            mensaje
        )

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()

        return mensaje


# CREAR LOS OBJETOS

ejercicio_par_impar = ParImpar()

ejercicio_tabla = TablaMultiplicar()

ejercicio_adivina = AdivinaNumero()


# RUTA 1: PAR O IMPAR

@app.route("/", methods=["GET", "POST"])
def par_impar():

    resultado = None

    if request.method == "POST":

        numero = int(request.form["numero"])

        resultado = ejercicio_par_impar.comprobar(numero)

    return render_template(
        "par_impar.html",
        resultado=resultado
    )


# ==========================================
# RUTA 2: TABLA DE MULTIPLICAR
# ==========================================

@app.route("/tabla", methods=["GET", "POST"])
def tabla():

    resultado = None

    if request.method == "POST":

        numero = int(request.form["numero"])

        resultado = ejercicio_tabla.generar(numero)

    return render_template(
        "tabla_multiplicar.html",
        tabla=resultado
    )


# ==========================================
# RUTA 3: ADIVINA EL NÚMERO
# ==========================================

@app.route("/adivina", methods=["GET", "POST"])
def adivina():

    mensaje = None

    if request.method == "POST":

        intento = int(request.form["intento"])

        mensaje = ejercicio_adivina.comprobar(intento)

    return render_template(
        "adivina_numero.html",
        mensaje=mensaje
    )


# ==========================================
# EJECUTAR FLASK
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)