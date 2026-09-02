from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import pymysql
import os


BD_CONFIG = {
	"host": "servidor-bd",
	"user": "root",
	"password": os.getenv("MYSQL_ROOT_PASSWORD"),
	"database": os.getenv("MYSQL_DATABASE"),
	"connect_timeout":3,
	"cursorclass" : pymysql.cursors.DictCursor,
	"autocommit":True
}

app  = Flask(__name__)

def crear_tabla():
	sql= """
		CREATE TABLE IF NOT EXISTS aprendices (
		id INT AUTO_INCREMENT PRIMARY KEY,
		nombre_completo VARCHAR(100) NOT NULL,
		numero_documento VARCHAR(20) NOT NULL,
		ficha VARCHAR(20) NOT NULL,
		creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	"""

	try:
		conn = pymysql.connect(**BD_CONFIG)

		with conn.cursor() as cursor:
			cursor.execute(sql)
		conn.close()
	except Exception as e:
		print(f"error al crear la tabla: {e}")
		
@app.route("/", methods = ["GET"])
def home () :
	aprendices = []
	db_status = "Error: Sin conexión a la base de datos"
	try:
		conn = pymysql.connect(**BD_CONFIG)
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM aprendices ORDER BY creado_en DESC")
			aprendices = cursor.fetchall()
		conn.close()
		db_status = "Conectado y probando CI/CD prueba 2"
	except Exception as e:
		print (f"error al obtener los aprendices: {e}")

	return render_template("index.html", aprendices = aprendices, db_status = db_status)
	
@app.route("/registrar", methods = ["POST"])
def registrar ():
	nombre = request.form.get("nombre_completo")
	documento = request.form.get("numero_documento")
	ficha = request.form.get("ficha")
	
	if nombre and documento and ficha:
		try:
			conn = pymysql.connect(**BD_CONFIG)
			with conn.cursor() as cursor:
				sql = "INSERT INTO aprendices (nombre_completo, numero_documento, ficha) VALUES (%s, %s, %s)"
				cursor.execute(sql, (nombre, documento, ficha))
			conn.close()
		except Exception as e:
			print(f"Error al insertar aprendiz: {e}")		
	return redirect("/")

modo_debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
host = os.getenv("FLASK_HOST") or "0.0.0.0"  # nosec B104

if __name__ == "__main__":
	
	crear_tabla()
	app.run(host = host, port = 5050, debug=modo_debug)
