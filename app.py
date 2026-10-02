# IMPORTAMOS LAS HERRAMIENTAS QUE VAMOS A UTILIZAR
from flask import Flask, render_template, request

# Nos permite conectar Python con MySQL
import mysql.connector


# CREAR LA APLICACIÓN FLASK
app = Flask(__name__)


# CONEXIÓN CON MYSQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="par_impar"
)

print("Conexión exitosa")


# RUTA PRINCIPAL
@app.route("/", methods=["GET", "POST"])
def inicio():

    # COMPROBAMOS SI SE ENVIÓ UN FORMULARIO
    if request.method == "POST":

        # ==========================================
        # EJERCICIO 1: PAR O IMPAR
        # ==========================================

        if "numero_par" in request.form:

            # Recibimos el número
            numero = int(request.form["numero_par"])

            # Comprobamos si es par o impar
            if numero % 2 == 0:
                resultado = "El número es par"
            else:
                resultado = "El número es impar"

            # Conectamos con MySQL
            cursor = conexion.cursor()

            # Instrucción SQL
            sql = """
            INSERT INTO resultados (numero, resultado)
            VALUES (%s, %s)
            """

            # Valores que vamos a guardar
            valores = (numero, resultado)

            # Ejecutamos el INSERT
            cursor.execute(sql, valores)

            # Guardamos los cambios
            conexion.commit()

            # Cerramos el cursor
            cursor.close()

            # Mostramos el resultado
            return render_template(
                "index.html",
                resultado=resultado
            )


        # ==========================================
        # EJERCICIO 2: TABLA DE MULTIPLICAR
        # ==========================================

        if "numero_tabla" in request.form:

            # Recibimos el número
            numero = int(request.form["numero_tabla"])

            # Creamos una lista vacía
            tabla = []

            # Repetimos del 1 al 10
            for i in range(1, 11):

                # Multiplicamos
                resultado = numero * i

                # Guardamos la operación
                tabla.append(
                    f"{numero} x {i} = {resultado}"
                )

            # Mostramos la tabla
            return render_template(
                "index.html",
                tabla=tabla
            )


        # ==========================================
        # EJERCICIO 3: ADIVINA EL NÚMERO
        # ==========================================

        if "intento" in request.form:

            # Recibimos el intento
            intento = int(request.form["intento"])

            # Número secreto
            numero_secreto = 7

            # Mientras el intento no sea correcto
            while True:

                # Si el intento es menor
                if intento < numero_secreto:

                    mensaje = "El número es mayor"
                    break

                # Si el intento es mayor
                elif intento > numero_secreto:

                    mensaje = "El número es menor"
                    break

                # Si acertó
                else:

                    mensaje = "¡Correcto! Adivinaste el número"
                    break

            # Mostramos el mensaje
            return render_template(
                "index.html",
                mensaje=mensaje
            )


    # MOSTRAR LA PÁGINA AL ENTRAR
    return render_template("index.html")


# EJECUTAR LA APLICACIÓN
if __name__ == "__main__":
    app.run(debug=True)