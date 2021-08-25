from fpdf import FPDF
import random, os

__author__ = 'R-V-L'
is_last_page = False

os.chdir(os.path.dirname(__file__))

class pdf_config:
    #title = 1
    num_columnas = 4
    num_filas = 2
    def __init__(self, config):
        self._title = config["title"]
        self.logo = config["logo"]
        self.nombreMaestro = config["nombreMaestro"]
        self.studentName = config["studentName"]
        self.numero_problemas = config["numero_problemas"]
        self.pdf = PDF(orientation = 'L', unit = 'mm', format='A4')
        self.pdf.set_font('Helvetica', '', 14)
        self.max_number = config["max_number"]
        self.main_type = config["main_type"]
        self.tipos_operacion = ['+', '-', 'x']
        self.middle_font_size = 15
        self.large_font_size = 30
        self.size = 21
        self.tiny_pad_size = 2
        self.pad_size = 10
        self.large_pad_size = 30
        self.num_x_cell = 4
        self.num_y_cell = 2

class PDF(FPDF, pdf_config):
    def header(self):
        # Add logo if variable has been assigned
        if config["logo"] != None and config["logo"] != "":
            self.image(config["logo"], 10, 8, 33)
        # Helvetica bold 15
        self.set_font(style='B', size=15)
        # Center title
        self.set_x((self.w - self.get_string_width(config["title"])) / 2)
        # Set "answers" if is last page, otherwise type title
        if is_last_page:
            self.cell(30, 10, f"RESPUESTAS - {config['title'].upper()}", 0, 0, 'C')
        else:        
            self.cell(30, 10, config["title"].upper(), 0, 0, 'C')
        # Line break
        self.ln(15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font(style='I')
        # Page number
        self.cell(0, 10, config["nombreMaestro"], 0, 0, 'L')
        self.cell(0, 10, config["studentName"], 0, 0, 'R')

def generar_preguntas(self):
        lista_problemas = []
        for numero_problema in range(self.numero_problemas):          
            num_1 = random.randint(0, self.max_number)
            num_2 = random.randint(0, self.max_number)
            if self.main_type == 'mix':
                current_type = random.choice(self.tipos_operacion)
            else:
                current_type = self.main_type
            if current_type == '+':
                respuesta = num_1 + num_2
            elif current_type == '-':
                num_1, num_2 = sorted((num_1, num_2), reverse=True)
                respuesta = num_1 - num_2
            elif current_type == 'x':
                respuesta = num_1 * num_2
            else:
                print(f'Problema "{current_type}" no soportado')
                answer = None
            lista_problemas.append([numero_problema + 1, num_1, current_type, num_2, respuesta])
        return lista_problemas

def pagina_tareas_2(self, problemas):
    for problema in problemas:
        self.pdf.set_font(size=self.middle_font_size)
        self.pdf.cell(self.pad_size, self.pad_size, txt=str(problema[0]), border='LT', align='C')
        self.pdf.cell(self.size, self.pad_size, border='T')
        self.pdf.cell(self.size, self.pad_size, border='T')
        self.pdf.cell(self.pad_size, self.pad_size, border='TR')
        self.pdf.cell(self.pad_size, self.pad_size)        
    self.pdf.ln()
    
    for problema in problemas:
        self.pdf.set_font(size=self.large_font_size)
        self.pdf.cell(self.pad_size, self.size, border='L')
        self.pdf.cell(self.size, self.size)
        self.pdf.cell(self.size, self.size, txt=str(problema[1]), align='R')
        self.pdf.cell(self.pad_size, self.size, border='R')
        self.pdf.cell(self.pad_size, self.size)           
    self.pdf.ln()

    for problema in problemas:
        self.pdf.cell(self.pad_size, self.size, border='L')
        self.pdf.cell(self.size, self.size, txt=str(problema[2]), align='L')
        self.pdf.cell(self.size, self.size, txt=str(problema[3]), align='R')
        self.pdf.cell(self.pad_size, self.size, border='R')
        self.pdf.cell(self.pad_size, self.size)
    self.pdf.ln()

    for problema in problemas:
        self.pdf.cell(self.pad_size, self.size, border='LB')
        self.pdf.cell(self.size, self.size, border='TB')
        self.pdf.cell(self.size, self.size, border='TB')
        self.pdf.cell(self.pad_size, self.size, border='BR')
        self.pdf.cell(self.pad_size, self.pad_size)

def pagina_tareas(self, problemas):
    self.pdf.add_page()
    """
    line_height = self.pdf.font_size * 2.5
    col_width = self.pdf.epw / 4
    tamano_columna = ((self.pdf.w - ((self.num_columnas * 10) + 10)) / self.num_columnas)
    """
    for i in range(0, len(problemas), 4):
        pagina_tareas_2(self, problemas[i:i+4])
        self.pdf.ln(30)

def pagina_respuestas(self, problemas):
    self.pdf.set_font(size=14)
    global is_last_page
    is_last_page = True
    self.pdf.add_page()
    line_height = self.pdf.font_size * 2.5
    col_width = self.pdf.epw / 10
    
    for problema in problemas:
        problema_actual = f"{problema[0]}: {problema[4]}"
        self.pdf.multi_cell(col_width, line_height, problema_actual, border=1, ln=3, max_line_height=self.pdf.font_size, align="C")
        if((problema[0] / 10).is_integer()):
            self.pdf.ln(line_height)
config = {}
def main(configs):
    global config, is_last_page
    config = configs
    self = pdf_config(config)
    preguntas = generar_preguntas(self)
    pagina_tareas(self, preguntas)
    pagina_respuestas(self, preguntas)
    is_last_page = False
    return self.pdf.output(dest="S")

if __name__ == "__main__":
    config = {
        "title": "Actividades",
        "nombreMaestro": "",
        "studentName": "",
        "max_number": 99,
        "main_type": "mix",
        "logo": "",
        "numero_problemas": 10
    }
    archivo = main(config)
    with open("my_file.pdf", "wb") as binary_file:
        binary_file.write(archivo)