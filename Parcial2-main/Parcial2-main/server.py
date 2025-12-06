from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector
from urllib.parse import urlparse




# Conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_academica"
    )

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Mostrar login como primera vista
            with open("login.html", "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())

        elif self.path == "/usuarios.html":
            with open("usuarios.html", "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())

        elif self.path == "/listar":
            self.listar_usuarios()

    def do_POST(self):
        if self.path == "/registrar":
            self.registrar_usuario()
        elif self.path == "/login":
            self.verificar_login()
        elif self.path == "/eliminar":
            self.eliminar_usuario()
        elif self.path == "/editar":
            self.editar_usuario()

    def registrar_usuario(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (data["usuario"], data["clave"], data["nombre"], data["direccion"], data["telefono"]))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Usuario registrado correctamente")

    def listar_usuarios(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(datos).encode())

    def eliminar_usuario(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE idUsuario=%s", (data["id"],))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Usuario eliminado")

    def editar_usuario(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        conn = get_connection()
        cursor = conn.cursor()
        sql = """UPDATE usuarios SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s WHERE idUsuario=%s"""
        cursor.execute(sql, (data["usuario"], data["clave"], data["nombre"], data["direccion"], data["telefono"], data["id"]))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Usuario actualizado")

    def verificar_login(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND clave=%s", (data["usuario"], data["clave"]))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if usuario:
            self.wfile.write(json.dumps({"ok": True}).encode())
        else:
            self.wfile.write(json.dumps({"ok": False}).encode())

# Iniciar servidor
if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), MyHandler)
    print("Servidor corriendo en http://localhost:8080")
    server.serve_forever()
