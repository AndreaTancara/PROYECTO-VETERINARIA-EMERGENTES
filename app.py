from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("citas.db")


@app.route("/")
def index():
    conn = get_db()
    citas = conn.execute("SELECT * FROM pacientes").fetchall()
    conn.close()
    return render_template("index.html", citas=citas)


@app.route("/nueva", methods=["GET","POST"])
def nueva():

    if request.method == "POST":

        mascota = request.form["mascota"]
        propietario = request.form["propietario"]
        especie = request.form["especie"]
        fecha = request.form["fecha"]

        conn = get_db()

        conn.execute(
        "INSERT INTO pacientes (mascota,propietario,especie,fecha) VALUES (?,?,?,?)",
        (mascota,propietario,especie,fecha)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("nueva_cita.html")


@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):

    conn = get_db()

    if request.method == "POST":

        mascota = request.form["mascota"]
        propietario = request.form["propietario"]
        especie = request.form["especie"]
        fecha = request.form["fecha"]

        conn.execute("""
        UPDATE pacientes
        SET mascota=?, propietario=?, especie=?, fecha=?
        WHERE id=?
        """,(mascota,propietario,especie,fecha,id))

        conn.commit()
        conn.close()

        return redirect("/")

    cita = conn.execute("SELECT * FROM pacientes WHERE id=?", (id,)).fetchone()

    conn.close()

    return render_template("editar_cita.html", cita=cita)


@app.route("/eliminar/<int:id>")
def eliminar(id):

    conn = get_db()

    conn.execute("DELETE FROM pacientes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)