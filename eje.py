from flask import Flask, render_template, request
import mysql.connector


# ==========================================
# CLASE BASE DE DATOS (ENCAPSULACIÓN)
# ==========================================
class BaseDatos:

    def __init__(self, host, user, password, database):
        # Atributo privado: solo se usa dentro de la clase
        self.__conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Conexión exitosa")

    def ejecutar(self, sql, valores):
        cursor = self.__conexion.cursor()
        try:
            cursor.execute(sql, valores)
            self.__conexion.commit()
        finally:
            cursor.close()


# ==========================================
# CLASE PADRE (HERENCIA)
# ==========================================
class Ejercicio:

    def __init__(self, db):
        self._db = db  # atributo protegido, lo heredan las hijas

    def procesar(self, valor):
        # Cada hija debe implementar este método (POLIMORFISMO)
        raise NotImplementedError("Implementar en la clase hija")


# ==========================================
# CLASE 1: PAR O IMPAR
# ==========================================
class ParImpar(Ejercicio):

    def procesar(self, numero):
        if numero % 2 == 0:
            resultado = "El número es par"
        else:
            resultado = "El número es impar"

        self._db.ejecutar(
            "INSERT INTO resultados (numero, resultado) VALUES (%s, %s)",
            (numero, resultado)
        )
        return resultado


# ==========================================
# CLASE 2: TABLA DE MULTIPLICAR
# ==========================================
class TablaMultiplicar(Ejercicio):

    def procesar(self, numero):
        tabla = [f"{numero} x {i} = {numero * i}" for i in range(1, 11)]

        self._db.ejecutar(
            "INSERT INTO tablas_multiplicar (numero, tabla_generada) VALUES (%s, %s)",
            (numero, "\n".join(tabla))
        )
        return tabla


# ==========================================
# CLASE 3: ADIVINA EL NÚMERO
# ==========================================
class AdivinaNumero(Ejercicio):

    def __init__(self, db, numero_secreto=7):
        super().__init__(db)
        self.__numero_secreto = numero_secreto  # privado

    def procesar(self, intento):
        if intento < self.__numero_secreto:
            mensaje = "El número es mayor"
        elif intento > self.__numero_secreto:
            mensaje = "El número es menor"
        else:
            mensaje = "¡Correcto! Adivinaste el número"

        self._db.ejecutar(
            """
            INSERT INTO adivina_numero (intento, numero_secreto, mensaje)
            VALUES (%s, %s, %s)
            """,
            (intento, self.__numero_secreto, mensaje)
        )
        return mensaje


# ==========================================
# CREAR APLICACIÓN Y OBJETOS
# ==========================================
app = Flask(__name__)

db = BaseDatos("localhost", "root", "", "par_impar")

ejercicio_par_impar = ParImpar(db)
ejercicio_tabla = TablaMultiplicar(db)
ejercicio_adivina = AdivinaNumero(db)


# RUTAS
@app.route("/", methods=["GET", "POST"])
def par_impar():
    resultado = None
    if request.method == "POST":
        numero = int(request.form["numero"])
        resultado = ejercicio_par_impar.procesar(numero)
    return render_template("par_impar.html", resultado=resultado)


@app.route("/tabla", methods=["GET", "POST"])
def tabla():
    resultado = None
    if request.method == "POST":
        numero = int(request.form["numero"])
        resultado = ejercicio_tabla.procesar(numero)
    return render_template("tabla_multiplicar.html", tabla=resultado)


@app.route("/adivina", methods=["GET", "POST"])
def adivina():
    mensaje = None
    if request.method == "POST":
        intento = int(request.form["intento"])
        mensaje = ejercicio_adivina.procesar(intento)
    return render_template("adivina_numero.html", mensaje=mensaje)


if __name__ == "__main__":
    app.run(debug=True)