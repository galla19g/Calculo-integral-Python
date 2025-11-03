import sympy as sp
from sympy import symbols, sqrt, sin, cos, tan, sec, asin, atan, integrate
from sympy import simplify, trigsimp, latex
import re
from typing import Tuple, Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import math

# Símbolos globales
x, a_sym, theta = symbols('x a theta', real=True)

# ---------- Helpers de impresión ASCII ----------
def linea(sep='-', largo=80):
    print(sep * largo)

def mostrar_titulo_ascii(texto):
    linea('=')
    print(f"  {texto}")
    linea('=')
    print()

def mostrar_subtitulo_ascii(texto):
    linea('-')
    print(f"  {texto}")
    linea('-')
    print()

def mostrar_paso_ascii(titulo, contenido):
    mostrar_subtitulo_ascii(titulo)
    if contenido:
        print(contenido)
    print()

def mostrar_formula_ascii(descripcion, expr_latex):
    # Mostrar descripción y la expresión LaTeX (para el informe)
    if descripcion:
        print(f"> {descripcion}")
    print(f"  LaTeX: {expr_latex}")
    print()

# ---------- Clase Triángulo para visualización ----------
class TrianguloRectangulo:
    """Clase para visualizar triángulos rectángulos (matplotlib)."""

    def __init__(self, tipo, parametro_a):
        self.tipo = tipo
        try:
            self.a = float(parametro_a)
        except Exception:
            # si parametro_a no convertible, tomar valor absoluto de 1
            self.a = 1.0
        self.construir_triangulo()

    def construir_triangulo(self):
        if self.tipo == 'tipo1':
            self.hipotenusa = self.a
            self.cateto_opuesto = 'x'
            self.cateto_adyacente = f'√({self.a}² - x²)'
        elif self.tipo == 'tipo2':
            self.hipotenusa = f'√({self.a}² + x²)'
            self.cateto_opuesto = 'x'
            self.cateto_adyacente = str(self.a)
        else:  # tipo3
            self.hipotenusa = 'x'
            self.cateto_opuesto = f'√(x² - {self.a}²)'
            self.cateto_adyacente = str(self.a)

    def dibujar_triangulo(self, guardar=False, nombre_archivo='triangulo.png'):
        fig, ax = plt.subplots(figsize=(6, 5))

        if self.tipo == 'tipo1':
            vertices = np.array([[0, 0], [3.5, 0], [3.5, 2.5]])
            labels = {
                'base': f'Cateto Opuesto = x',
                'altura': f'Cateto Adyacente = √({self.a}² - x²)',
                'hipotenusa': f'Hipotenusa = {self.a}'
            }
            titulo = f'Triángulo para √({self.a}² - x²)'
            sustitucion = f'x = {self.a}·sen(θ)'
            identidad = '1 - sen²(θ) = cos²(θ)'
        elif self.tipo == 'tipo2':
            vertices = np.array([[0, 0], [3, 0], [3, 4]])
            labels = {
                'base': f'Cateto Opuesto = x',
                'altura': f'Cateto Adyacente = {self.a}',
                'hipotenusa': f'Hipotenusa = √({self.a}² + x²)'
            }
            titulo = f'Triángulo para √({self.a}² + x²)'
            sustitucion = f'x = {self.a}·tan(θ)'
            identidad = '1 + tan²(θ) = sec²(θ)'
        else:
            vertices = np.array([[0, 0], [3, 0], [3, 4]])
            labels = {
                'base': f'Cateto Opuesto = √(x² - {self.a}²)',
                'altura': f'Cateto Adyacente = {self.a}',
                'hipotenusa': f'Hipotenusa = x'
            }
            titulo = f'Triángulo para √(x² - {self.a}²)'
            sustitucion = f'x = {self.a}·sec(θ)'
            identidad = 'sec²(θ) - 1 = tan²(θ)'

        triangle = patches.Polygon(vertices, fill=False, edgecolor='#667eea', linewidth=3)
        ax.add_patch(triangle)

        angle = patches.Arc((0, 0), 0.8, 0.8, angle=0, theta1=0, theta2=40,
                            color='#764ba2', linewidth=2)
        ax.add_patch(angle)
        ax.text(0.4, 0.12, 'θ', fontsize=12, color='#764ba2', weight='bold')

        square = patches.Rectangle((vertices[1][0]-0.25, vertices[1][1]),
                                0.25, 0.25, fill=False, edgecolor='#667eea', linewidth=2)
        ax.add_patch(square)

        ax.text(1.8, -0.3, labels['base'], fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='#f093fb', alpha=0.7))
        ax.text(3.5 + 0.25, 1.5, labels['altura'], fontsize=10, rotation=90, va='center',
                bbox=dict(boxstyle='round', facecolor='#4facfe', alpha=0.7))
        ax.text(1.4, 1.2, labels['hipotenusa'], fontsize=10, rotation=30,
                bbox=dict(boxstyle='round', facecolor='#667eea', alpha=0.7))

        ax.set_xlim(-0.5, 5)
        ax.set_ylim(-0.5, 5)
        ax.set_aspect('equal')
        ax.axis('off')

        plt.title(titulo)
        info_text = f'Sustitución: {sustitucion} | Identidad: {identidad}'
        ax.text(0.1, 4.6, info_text, fontsize=9, bbox=dict(facecolor='white', alpha=0.7))

        plt.tight_layout()

        if guardar:
            plt.savefig(nombre_archivo, dpi=150)
            print(f"(Triángulo guardado en '{nombre_archivo}')")
        else:
            plt.show()


# ---------- Clase principal ----------
class SustitucionTrigonometricaInteractiva:
    def __init__(self, funcion, variable=x):
        self.funcion = funcion
        self.variable = variable
        self.tipo_sustitucion = None
        self.parametro_a = None
        self.triangulo = None

    def detectar_tipo_sustitucion(self) -> Optional[str]:
        mostrar_titulo_ascii("PASO 1: Análisis y Detección del Patrón")
        mostrar_paso_ascii("Función a Integrar", f"Integral: ∫ {sp.pretty(self.funcion)} dx")
        mostrar_formula_ascii("Integral original (LaTeX)", r'\int ' + latex(self.funcion) + r' \, dx')

        func_str = str(self.funcion)

        # Mejor soporte regex para números con o sin decimales
        patron1 = re.search(r'sqrt\(\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*x\*\*2\s*\)', func_str)
        patron2 = re.search(r'sqrt\(\s*([0-9]+(?:\.[0-9]+)?)\s*\+\s*x\*\*2\s*\)', func_str)
        patron3 = re.search(r'sqrt\(\s*x\*\*2\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*\)', func_str)

        if patron1:
            a_cuadrado = int(patron1.group(1))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo1'
            contenido = (
                f"Patrón detectado: √(a² - x²)\n"
                f"a² = {a_cuadrado}  →  a = {self.parametro_a}\n"
                f"Sustitución: x = {self.parametro_a}·sen(θ)\n"
                "Identidad usada: 1 - sen²(θ) = cos²(θ)"
            )
            mostrar_paso_ascii("Resultado del Análisis", contenido)
            return 'tipo1'

        if patron2:
            a_cuadrado = int(patron2.group(1))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo2'
            contenido = (
                f"Patrón detectado: √(a² + x²)\n"
                f"a² = {a_cuadrado}  →  a = {self.parametro_a}\n"
                f"Sustitución: x = {self.parametro_a}·tan(θ)\n"
                "Identidad usada: 1 + tan²(θ) = sec²(θ)"
            )
            mostrar_paso_ascii("Resultado del Análisis", contenido)
            return 'tipo2'

        if patron3:
            a_cuadrado = int(patron3.group(1))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo3'
            contenido = (
                f"Patrón detectado: √(x² - a²)\n"
                f"a² = {a_cuadrado}  →  a = {self.parametro_a}\n"
                f"Sustitución: x = {self.parametro_a}·sec(θ)\n"
                "Identidad usada: sec²(θ) - 1 = tan²(θ)"
            )
            mostrar_paso_ascii("Resultado del Análisis", contenido)
            return 'tipo3'


        s = self.funcion
        # Buscar subexpresiones tipo sqrt(...)
        for sub in sp.preorder_traversal(s):
            if sub.func == sp.sqrt:
                arg = sub.args[0]
                # intentar comparar con una - x**2
                if arg.is_Add:
                    terms = arg.as_ordered_terms()
                    # buscar pattern a - x**2
                    for t in terms:
                        if t.has(x**2) and any(term.is_Number for term in terms):
                            # fallback: no exact detection, marcar tipo1 por defecto
                            pass
        mostrar_paso_ascii("Resultado del Análisis", "No se detectó un patrón estándar automáticamente.")
        return None

    def construir_triangulo_rectangulo(self):
        mostrar_titulo_ascii("PASO 2: Construcción del Triángulo Rectángulo")
        mostrar_paso_ascii("Teorema de Pitágoras", "Construccion de un triángulo que representa la sustitución.")
        self.triangulo = TrianguloRectangulo(self.tipo_sustitucion, self.parametro_a)
        # intentar mostrar: si no hay entorno gráfico, el usuario puede guardar con --save-img
        try:
            self.triangulo.dibujar_triangulo()
        except Exception as e:
            print("(Advertencia: no se pudo mostrar el triángulo gráficamente.)")
            print(str(e))
        # mostrar verificación simbólica de Pitágoras
        if self.tipo_sustitucion == 'tipo1':
            latex_pitagoras = f'({self.parametro_a})^2 = x^2 + (\\sqrt{{{self.parametro_a}^2 - x^2}})^2'
        elif self.tipo_sustitucion == 'tipo2':
            latex_pitagoras = f'(\\sqrt{{{self.parametro_a}^2 + x^2}})^2 = x^2 + ({self.parametro_a})^2'
        else:
            latex_pitagoras = f'x^2 = (\\sqrt{{x^2 - {self.parametro_a}^2}})^2 + ({self.parametro_a})^2'
        mostrar_formula_ascii("Verificación de Pitágoras (LaTeX)", latex_pitagoras)

    def aplicar_sustitucion(self):
        mostrar_titulo_ascii("PASO 3: Aplicación de la Sustitución")
        if self.tipo_sustitucion == 'tipo1':
            x_sust = self.parametro_a * sin(theta)
            dx_sust = self.parametro_a * cos(theta)
        elif self.tipo_sustitucion == 'tipo2':
            x_sust = self.parametro_a * tan(theta)
            dx_sust = self.parametro_a * sec(theta)**2
        else:
            x_sust = self.parametro_a * sec(theta)
            dx_sust = self.parametro_a * sec(theta) * tan(theta)

        mostrar_paso_ascii("Sustitución de x", f"x = {sp.pretty(x_sust)}")
        mostrar_paso_ascii("Diferencial dx", f"dx = {sp.pretty(dx_sust)} dθ")

        func_sustituida = sp.simplify(self.funcion.subs(self.variable, x_sust))
        mostrar_paso_ascii("Función Sustituida", f"Integrando: ∫ {sp.pretty(func_sustituida * dx_sust)} dθ")
        mostrar_formula_ascii("Integral en θ (LaTeX)", r'\int ' + latex(func_sustituida * dx_sust) + r' \, d\theta')

        return func_sustituida, dx_sust

    def simplificar_con_pitagoras(self, expresion):
        mostrar_titulo_ascii("PASO 4: Simplificación con Identidades")
        mostrar_paso_ascii("Expresión a Simplificar (en θ)", sp.pretty(expresion))
        expr_simplificada = trigsimp(simplify(expresion))

        if self.tipo_sustitucion == 'tipo1':
            explicacion = (
                "Aplicando: 1 - sen²(θ) = cos²(θ)\n"
                f"√({self.parametro_a}² - x²) con x = {self.parametro_a}·sen(θ) => {self.parametro_a}·cos(θ)"
            )
        elif self.tipo_sustitucion == 'tipo2':
            explicacion = (
                "Aplicando: 1 + tan²(θ) = sec²(θ)\n"
                f"√({self.parametro_a}² + x²) con x = {self.parametro_a}·tan(θ) => {self.parametro_a}·sec(θ)"
            )
        else:
            explicacion = (
                "Aplicando: sec²(θ) - 1 = tan²(θ)\n"
                f"√(x² - {self.parametro_a}²) con x = {self.parametro_a}·sec(θ) => {self.parametro_a}·tan(θ)"
            )

        mostrar_paso_ascii("Explicación", explicacion)
        mostrar_paso_ascii("Resultado simplificado (θ)", sp.pretty(expr_simplificada))
        mostrar_formula_ascii("Resultado simplificado (LaTeX)", latex(expr_simplificada))

        return expr_simplificada

    def integrar_en_theta(self, expresion):
        mostrar_titulo_ascii("PASO 5: Integración en θ")
        mostrar_paso_ascii("Integral a resolver (θ)", sp.pretty(expresion))
        mostrar_formula_ascii("Integral a resolver (LaTeX)", r'\int ' + latex(expresion) + r' \, d\theta')
        integral_theta = integrate(expresion, theta)
        mostrar_paso_ascii("Resultado de la Integración (θ)", sp.pretty(integral_theta))
        mostrar_formula_ascii("Resultado en LaTeX", latex(integral_theta) + r' + C')
        return integral_theta

    def desustituir(self, resultado_theta):
        mostrar_titulo_ascii("PASO 6: Desustitución (Volver a x)")
        mostrar_paso_ascii("Relaciones del triángulo", "")
        resultado_x = resultado_theta

        if self.tipo_sustitucion == 'tipo1':
            mostrar_formula_ascii("Relaciones (LaTeX)",
                                f'\\sin(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                                f'\\cos(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 - x^2}}}}{{{self.parametro_a}}}')
            resultado_x = resultado_x.subs(sin(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(cos(theta), sqrt(self.parametro_a**2 - x**2)/self.parametro_a)
        elif self.tipo_sustitucion == 'tipo2':
            mostrar_formula_ascii("Relaciones (LaTeX)",
                                f'\\tan(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                                f'\\sec(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 + x^2}}}}{{{self.parametro_a}}}')
            resultado_x = resultado_x.subs(tan(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(sec(theta), sqrt(self.parametro_a**2 + x**2)/self.parametro_a)
        else:
            mostrar_formula_ascii("Relaciones (LaTeX)",
                                f'\\sec(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                                f'\\tan(\\theta) = \\frac{{\\sqrt{{x^2 - {self.parametro_a}^2}}}}{{{self.parametro_a}}}')
            resultado_x = resultado_x.subs(sec(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(tan(theta), sqrt(x**2 - self.parametro_a**2)/self.parametro_a)

        resultado_final = simplify(resultado_x)
        mostrar_paso_ascii("Resultado Final (en x)", sp.pretty(resultado_final))
        mostrar_formula_ascii("Resultado Final (LaTeX)", latex(resultado_final) + r' + C')
        return resultado_final

    def resolver(self):
        try:
            mostrar_titulo_ascii("🧮 Resolución de Integral por Sustitución Trigonométrica")
            tipo = self.detectar_tipo_sustitucion()
            if not tipo:
                raise ValueError("No se detectó un patrón estándar para sustitución trigonométrica.")

            self.construir_triangulo_rectangulo()
            func_sust, dx_sust = self.aplicar_sustitucion()
            expresion_completa = func_sust * dx_sust
            expr_simplificada = self.simplificar_con_pitagoras(expresion_completa)
            resultado_theta = self.integrar_en_theta(expr_simplificada)
            resultado_final = self.desustituir(resultado_theta)

            mostrar_titulo_ascii("RESULTADO FINAL")
            print(f"∫ {sp.pretty(self.funcion)} dx = {sp.pretty(resultado_final)} + C\n")

            # Verificación con SymPy (integral directa)
            mostrar_titulo_ascii("Verificación con SymPy (integrar directamente en x)")
            verificacion = integrate(self.funcion, x)
            print(f"Integral directa con SymPy: {sp.pretty(verificacion)}\n")
            return resultado_final

        except Exception as e:
            mostrar_paso_ascii("❌ Error", str(e))
            return None


# ---------- Menú / Ejecución ----------
def menu_consola():
    opciones = {
        1: "1/(x**2 * sqrt(x**2 - 4))",
        2: "1/sqrt(9 - x**2)",
        3: "x**2/sqrt(16 + x**2)",
        4: "1/(x * sqrt(x**2 - 25))"
    }

    mostrar_titulo_ascii("📋 Seleccione una función (ingrese el número o presione Enter para 1)")
    for k, v in opciones.items():
        print(f"{k}. {v}")
    print()
    try:
        entrada = input("Opción [1-4] (Enter=1): ").strip()
        opcion = int(entrada) if entrada != "" else 1
        if opcion not in opciones:
            opcion = 1
    except Exception:
        opcion = 1

    func_str = opciones[opcion]
    funcion = sp.sympify(func_str)
    resolvedor = SustitucionTrigonometricaInteractiva(funcion, x)
    resolvedor.resolver()


if __name__ == "__main__":
    # Ejecutar menú de consola
    menu_consola()
