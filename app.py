from flask import Flask, render_template, request, send_file, make_response
from generador import main

app = Flask(__name__) 

@app.route('/', methods=['GET', 'POST'])
def home(): 
    return render_template('home.html')

def asignar_valores(req):
    config["title"] = req["nombreActividad"]
    config["nombreMaestro"] = req["nombreMaestro"]
    config["studentName"] = req["nombreAlumno"]
    if req["complejidad"] == "1 - 9":
        config["max_number"] = 9
    elif req["complejidad"] == "1 - 99":
        config["max_number"] = 99
    elif req["complejidad"] == "1 - 999":
        config["max_number"] = 999
    config["logo"] = ""
    config["numero_problemas"] = int(req["numeroEjercicios"])
    if req["operacion"] == "Todos":
        config["main_type"] = "mix"
    elif req["operacion"] == "Suma":
        config["main_type"] = "+"
    elif req["operacion"] == "Resta":
        config["main_type"] = "-"
    elif req["operacion"] == "Multiplicacion":
        config["main_type"] = "x"
    else:
        config["main_type"] = req["operacion"]
    return config

config = {
        "title": "Actividades",
        "nombreMaestro": "",
        "studentName": "",
        "max_number": 99,
        "main_type": "mix",
        "logo": "",
        "numero_problemas": 10
    }

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        req = request.form.to_dict()
        config = asignar_valores(req)
        lpdf = main(config)
        response = make_response(lpdf)
        if config["title"] == "":
            config["title"] = "Actividad"
        response.headers.set('Content-Disposition', 'attachment', filename=f'{config["title"]}.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
    return render_template('home.html')

if __name__ == "__main__":
    app.run(port=80, debug=TRUE)
