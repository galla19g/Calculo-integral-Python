"""
Modelado Computacional de Integrales por Sustitución Trigonométrica
Versión Interactiva para Jupyter Notebook / Google Colab

Autor: Estudiante UNIPUTUMAYO
Asignatura: Cálculo Integral / Programación Aplicada a la Matemática
"""

# Instalación de dependencias (descomentar si es necesario)
# !pip install sympy matplotlib ipywidgets

import sympy as sp
from sympy import symbols, sqrt, sin, cos, tan, sec, asin, atan, integrate
from sympy import simplify, trigsimp, latex
import re
from typing import Tuple, Dict, Optional
from IPython.display import display, HTML, Math, Latex
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Símbolos globales
x, a, theta = symbols('x a theta', real=True, positive=True)


def mostrar_titulo(texto, nivel=1):
    """Muestra un título formateado en HTML."""
    colores = {1: '#667eea', 2: '#764ba2', 3: '#f093fb'}
    sizes = {1: '28px', 2: '22px', 3: '18px'}
    
    html = f"""
    <div style='background: linear-gradient(135deg, {colores[nivel]}, #f093fb);
                padding: 15px; border-radius: 10px; margin: 20px 0;'>
        <h{nivel} style='color: white; margin: 0; font-size: {sizes[nivel]};'>
            {texto}
        </h{nivel}>
    </div>
    """
    display(HTML(html))


def mostrar_paso(titulo, contenido, latex_expr=None):
    """Muestra un paso con formato visual atractivo."""
    html = f"""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; 
                margin: 15px 0; border-left: 5px solid #667eea;'>
        <h3 style='color: #667eea; margin-bottom: 10px;'>📌 {titulo}</h3>
        <div style='font-size: 16px; line-height: 1.8; color: #333;'>
            {contenido}
        </div>
    </div>
    """
    display(HTML(html))
    
    if latex_expr:
        display(Math(latex_expr))


def mostrar_formula(descripcion, formula_latex):
    """Muestra una fórmula matemática destacada."""
    html = f"""
    <div style='background: white; padding: 20px; border-radius: 10px;
                margin: 10px 0; border: 2px solid #667eea; text-align: center;'>
        <p style='color: #666; margin-bottom: 10px;'>{descripcion}</p>
    </div>
    """
    display(HTML(html))
    display(Math(formula_latex))


class TrianguloRectangulo:
    """Clase para visualizar triángulos rectángulos."""
    
    def __init__(self, tipo, parametro_a):
        self.tipo = tipo
        self.a = float(parametro_a)
        self.construir_triangulo()
        
    def construir_triangulo(self):
        """Construye el triángulo según el tipo."""
        if self.tipo == 'tipo1':
            self.hipotenusa = self.a
            self.cateto_opuesto = 'x'
            self.cateto_adyacente = f'√({self.a}² - x²)'
            
        elif self.tipo == 'tipo2':
            self.hipotenusa = f'√({self.a}² + x²)'
            self.cateto_opuesto = 'x'
            self.cateto_adyacente = str(self.a)
            
        elif self.tipo == 'tipo3':
            self.hipotenusa = 'x'
            self.cateto_opuesto = f'√(x² - {self.a}²)'
            self.cateto_adyacente = str(self.a)
    
    def dibujar_triangulo(self):
        """Dibuja el triángulo usando Matplotlib."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Muestra coordenadas del triángulo
        if self.tipo == 'tipo1':
            vertices = np.array([[0, 0], [4, 0], [4, 3]])
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
            
        else:  # tipo3
            vertices = np.array([[0, 0], [3, 0], [3, 4]])
            labels = {
                'base': f'Cateto Opuesto = √(x² - {self.a}²)',
                'altura': f'Cateto Adyacente = {self.a}',
                'hipotenusa': f'Hipotenusa = x'
            }
            titulo = f'Triángulo para √(x² - {self.a}²)'
            sustitucion = f'x = {self.a}·sec(θ)'
            identidad = 'sec²(θ) - 1 = tan²(θ)'
        
        # Dibujar el triángulo
        triangle = patches.Polygon(vertices, fill=False, edgecolor='#667eea', linewidth=3)
        ax.add_patch(triangle)
        
        # Ángulo theta
        angle = patches.Arc((0, 0), 0.8, 0.8, angle=0, theta1=0, theta2=40, 
                        color='#764ba2', linewidth=2)
        ax.add_patch(angle)
        ax.text(0.5, 0.15, 'θ', fontsize=16, color='#764ba2', weight='bold')
        
        # Ángulo recto
        square = patches.Rectangle((vertices[1][0]-0.3, vertices[1][1]), 
                                0.3, 0.3, fill=False, edgecolor='#667eea', linewidth=2)
        ax.add_patch(square)
        
        # Etiquetas de los lados
        ax.text(2, -0.5, labels['base'], fontsize=12, ha='center', 
            bbox=dict(boxstyle='round', facecolor='#f093fb', alpha=0.7))
        ax.text(4.8, 1.5, labels['altura'], fontsize=12, rotation=90, va='center',
            bbox=dict(boxstyle='round', facecolor='#4facfe', alpha=0.7))
        ax.text(1.5, 1.8, labels['hipotenusa'], fontsize=12, rotation=37, 
            bbox=dict(boxstyle='round', facecolor='#667eea', alpha=0.7))
        
        # Configuración de ejes
        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Título y información
        plt.title(titulo, fontsize=18, weight='bold', color='#667eea', pad=20)
        
        # Caja de información
        info_text = f'Sustitución: {sustitucion}\nIdentidad de Pitágoras: {identidad}'
        ax.text(0.5, 4.5, info_text, fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='#f8f9fa', alpha=0.9),
            verticalalignment='top')
        
        plt.tight_layout()
        plt.show()


class SustitucionTrigonometricaInteractiva:
    """Clase principal con salida visual para notebook."""
    
    def __init__(self, funcion, variable=x):
        self.funcion = funcion
        self.variable = variable
        self.tipo_sustitucion = None
        self.parametro_a = None
        self.triangulo = None
        
    def detectar_tipo_sustitucion(self) -> Optional[str]:
        """Detecta el tipo de sustitución."""
        mostrar_titulo("PASO 1: Análisis y Detección del Patrón", 1)
        
        mostrar_paso("Función a Integrar", 
                    f"Debemos resolver la siguiente integral:")
        
        mostrar_formula("Integral Original", 
                    r'\int ' + latex(self.funcion) + r' \, dx')
        
        func_str = str(self.funcion)
        
        # Patrón tipo 1: √(a² - x²)
        patron1 = re.search(r'sqrt\((\d+)\s*-\s*x\*\*2\)', func_str)
        if patron1:
            a_cuadrado = int(patron1.group(1))
            self.parametro_a = sp.sqrt(a_cuadrado)
            self.tipo_sustitucion = 'tipo1'
            
            contenido = f"""
            ✅ <strong>Patrón detectado:</strong> √(a² - x²)<br>
            📐 <strong>Valores:</strong> a² = {a_cuadrado}, por lo tanto a = {self.parametro_a}<br>
            🔄 <strong>Sustitución apropiada:</strong> x = {self.parametro_a}·sen(θ)<br>
            📖 <strong>Justificación:</strong> Usamos la identidad pitagórica 1 - sen²(θ) = cos²(θ)
            """
            mostrar_paso("Resultado del Análisis", contenido)
            return 'tipo1'
        
        # Patrón tipo 2: √(a² + x²)
        patron2 = re.search(r'sqrt\((\d+)\s*\+\s*x\*\*2\)', func_str)
        if patron2:
            a_cuadrado = int(patron2.group(1))
            self.parametro_a = sp.sqrt(a_cuadrado)
            self.tipo_sustitucion = 'tipo2'
            
            contenido = f"""
            ✅ <strong>Patrón detectado:</strong> √(a² + x²)<br>
            📐 <strong>Valores:</strong> a² = {a_cuadrado}, por lo tanto a = {self.parametro_a}<br>
            🔄 <strong>Sustitución apropiada:</strong> x = {self.parametro_a}·tan(θ)<br>
            📖 <strong>Justificación:</strong> Usamos la identidad pitagórica 1 + tan²(θ) = sec²(θ)
            """
            mostrar_paso("Resultado del Análisis", contenido)
            return 'tipo2'
        
        # Patrón tipo 3: √(x² - a²)
        patron3 = re.search(r'sqrt\(x\*\*2\s*-\s*(\d+)\)', func_str)
        if patron3:
            a_cuadrado = int(patron3.group(1))
            self.parametro_a = sp.sqrt(a_cuadrado)
            self.tipo_sustitucion = 'tipo3'
            
            contenido = f"""
            ✅ <strong>Patrón detectado:</strong> √(x² - a²)<br>
            📐 <strong>Valores:</strong> a² = {a_cuadrado}, por lo tanto a = {self.parametro_a}<br>
            🔄 <strong>Sustitución apropiada:</strong> x = {self.parametro_a}·sec(θ)<br>
            📖 <strong>Justificación:</strong> Usamos la identidad pitagórica sec²(θ) - 1 = tan²(θ)
            """
            mostrar_paso("Resultado del Análisis", contenido)
            return 'tipo3'
        
        return None
    
    def construir_triangulo_rectangulo(self):
        """Construye y visualiza el triángulo."""
        mostrar_titulo("PASO 2: Construcción del Triángulo Rectángulo", 1)
        
        mostrar_paso("Teorema de Pitágoras", 
                    "Construimos un triángulo rectángulo que representa la sustitución trigonométrica:")
        
        self.triangulo = TrianguloRectangulo(self.tipo_sustitucion, self.parametro_a)
        self.triangulo.dibujar_triangulo()
        
        # Mostrar verificación de Pitágoras
        if self.tipo_sustitucion == 'tipo1':
            latex_pitagoras = f'({self.parametro_a})^2 = x^2 + (\\sqrt{{{self.parametro_a}^2 - x^2}})^2'
        elif self.tipo_sustitucion == 'tipo2':
            latex_pitagoras = f'(\\sqrt{{{self.parametro_a}^2 + x^2}})^2 = x^2 + ({self.parametro_a})^2'
        else:
            latex_pitagoras = f'x^2 = (\\sqrt{{x^2 - {self.parametro_a}^2}})^2 + ({self.parametro_a})^2'
        
        mostrar_formula("Verificación de Pitágoras", latex_pitagoras)
    
    def aplicar_sustitucion(self):
        """Aplica la sustitución trigonométrica."""
        mostrar_titulo("PASO 3: Aplicación de la Sustitución", 1)
        
        if self.tipo_sustitucion == 'tipo1':
            x_sust = self.parametro_a * sin(theta)
            dx_sust = self.parametro_a * cos(theta)
            
        elif self.tipo_sustitucion == 'tipo2':
            x_sust = self.parametro_a * tan(theta)
            dx_sust = self.parametro_a * sec(theta)**2
            
        else:  # tipo3
            x_sust = self.parametro_a * sec(theta)
            dx_sust = self.parametro_a * sec(theta) * tan(theta)
        
        mostrar_paso("Sustitución de x", f"Hacemos la siguiente sustitución:")
        mostrar_formula("x en términos de θ", f'x = {latex(x_sust)}')
        
        mostrar_paso("Diferencial dx", "Derivamos respecto a θ:")
        mostrar_formula("dx en términos de dθ", f'dx = {latex(dx_sust)} \\, d\\theta')
        
        func_sustituida = self.funcion.subs(self.variable, x_sust)
        
        mostrar_paso("Función Sustituida", "Reemplazamos en la integral original:")
        mostrar_formula("Nueva Integral", 
                       r'\int ' + latex(func_sustituida * dx_sust) + r' \, d\theta')
        
        return func_sustituida, dx_sust
    
    def simplificar_con_pitagoras(self, expresion):
        """Simplifica usando Pitágoras."""
        mostrar_titulo("PASO 4: Simplificación con Pitágoras", 1)
        
        mostrar_paso("Expresión a Simplificar", "")
        mostrar_formula("", latex(expresion))
        
        expr_simplificada = trigsimp(simplify(expresion))
        
        # Explicación específica según el tipo
        if self.tipo_sustitucion == 'tipo1':
            explicacion = f"""
            <strong>Aplicando la identidad:</strong> 1 - sen²(θ) = cos²(θ)<br><br>
            √({self.parametro_a}² - x²) con x = {self.parametro_a}·sen(θ):<br>
            = √({self.parametro_a}² - {self.parametro_a}²·sen²(θ))<br>
            = √({self.parametro_a}²(1 - sen²(θ)))<br>
            = √({self.parametro_a}²·cos²(θ))<br>
            = {self.parametro_a}·|cos(θ)| = {self.parametro_a}·cos(θ)
            """
        elif self.tipo_sustitucion == 'tipo2':
            explicacion = f"""
            <strong>Aplicando la identidad:</strong> 1 + tan²(θ) = sec²(θ)<br><br>
            √({self.parametro_a}² + x²) con x = {self.parametro_a}·tan(θ):<br>
            = √({self.parametro_a}² + {self.parametro_a}²·tan²(θ))<br>
            = √({self.parametro_a}²(1 + tan²(θ)))<br>
            = √({self.parametro_a}²·sec²(θ))<br>
            = {self.parametro_a}·|sec(θ)| = {self.parametro_a}·sec(θ)
            """
        else:
            explicacion = f"""
            <strong>Aplicando la identidad:</strong> sec²(θ) - 1 = tan²(θ)<br><br>
            √(x² - {self.parametro_a}²) con x = {self.parametro_a}·sec(θ):<br>
            = √({self.parametro_a}²·sec²(θ) - {self.parametro_a}²)<br>
            = √({self.parametro_a}²(sec²(θ) - 1))<br>
            = √({self.parametro_a}²·tan²(θ))<br>
            = {self.parametro_a}·|tan(θ)| = {self.parametro_a}·tan(θ)
            """
        
        mostrar_paso("Aplicando Identidades Trigonométricas", explicacion)
        
        mostrar_paso("Resultado Simplificado", "")
        mostrar_formula("Expresión Simplificada", latex(expr_simplificada))
        
        return expr_simplificada
    
    def integrar_en_theta(self, expresion):
        """Integra respecto a θ."""
        mostrar_titulo("PASO 5: Integración en θ", 1)
        
        mostrar_paso("Integrando", "Ahora resolvemos la integral:")
        mostrar_formula("", r'\int ' + latex(expresion) + r' \, d\theta')
        
        integral_theta = integrate(expresion, theta)
        
        mostrar_paso("Resultado de la Integración", "")
        mostrar_formula("", latex(integral_theta) + r' + C')
        
        return integral_theta
    
    def desustituir(self, resultado_theta):
        """Desustitución a términos de x."""
        mostrar_titulo("PASO 6: Desustitución (Regreso a x)", 1)
        
        mostrar_paso("Usando el Triángulo", 
                    "Convertimos las funciones trigonométricas de vuelta a términos de x usando las relaciones del triángulo:")
        
        resultado_x = resultado_theta
        
        if self.tipo_sustitucion == 'tipo1':
            mostrar_formula("Relaciones del Triángulo", 
                        f'\\sin(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\cos(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 - x^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(sin(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(cos(theta), sqrt(self.parametro_a**2 - x**2)/self.parametro_a)
            
        elif self.tipo_sustitucion == 'tipo2':
            mostrar_formula("Relaciones del Triángulo",
                        f'\\tan(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\sec(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 + x^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(tan(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(sec(theta), sqrt(self.parametro_a**2 + x**2)/self.parametro_a)
            
        else:
            mostrar_formula("Relaciones del Triángulo",
                        f'\\sec(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\tan(\\theta) = \\frac{{\\sqrt{{x^2 - {self.parametro_a}^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(sec(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(tan(theta), sqrt(x**2 - self.parametro_a**2)/self.parametro_a)
        
        resultado_final = simplify(resultado_x)
        
        mostrar_paso("Resultado Final", "")
        mostrar_formula("", latex(resultado_final) + r' + C')
        
        return resultado_final
    
    def resolver(self):
        """Método principal."""
        try:
            # Título principal
            html_titulo = """
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 30px;'>
                <h1 style='color: white; font-size: 36px; margin: 0;'>
                    🧮 Resolución de Integral por Sustitución Trigonométrica
                </h1>
            </div>
            """
            display(HTML(html_titulo))
            
            tipo = self.detectar_tipo_sustitucion()
            if not tipo:
                raise ValueError("No se detectó patrón")
            
            self.construir_triangulo_rectangulo()
            func_sust, dx_sust = self.aplicar_sustitucion()
            
            expresion_completa = func_sust * dx_sust
            expr_simplificada = self.simplificar_con_pitagoras(expresion_completa)
            
            resultado_theta = self.integrar_en_theta(expr_simplificada)
            resultado_final = self.desustituir(resultado_theta)
            
            # Resultado final destacado
            html_final = f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                        padding: 30px; border-radius: 15px; text-align: center; margin: 30px 0;'>
                <h2 style='color: white; margin-bottom: 15px;'>✅ RESULTADO FINAL</h2>
            </div>
            """
            display(HTML(html_final))
            
            mostrar_formula("Integral Resuelta",
                        r'\int ' + latex(self.funcion) + r' \, dx = ' + latex(resultado_final) + r' + C')
            
            # Verificación con dependencia SymPy
            mostrar_titulo("Verificación con SymPy", 2)
            verificacion = integrate(self.funcion, x)
            mostrar_formula("Cálculo Directo", 
                        r'\int ' + latex(self.funcion) + r' \, dx = ' + latex(verificacion))
            
            return resultado_final
            
        except Exception as e:
            mostrar_paso("❌ Error", f"Ocurrió un error: {str(e)}")
            return None

# Menu interactivo
def menu_interactivo():
    """Menú principal del programa."""
    html_menu = """
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; margin: 20px 0;'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>📋 Seleccione una Función</h2>
        <ol style='font-size: 18px; line-height: 2;'>
            <li><code>1/(x**2 * sqrt(x**2 - 4))</code> [Caso sugerido]</li>
            <li><code>1/sqrt(9 - x**2)</code></li>
            <li><code>x**2/sqrt(16 + x**2)</code></li>
            <li><code>1/(x * sqrt(x**2 - 25))</code></li>
        </ol>
    </div>
    """
    display(HTML(html_menu))
    
    print("Ingrese el número de la opción (1-4) o presione Enter para usar la opción 1:")


if __name__ == "__main__":
    funciones_predefinidas = {
        1: "1/(x**2 * sqrt(x**2 - 4))",
        2: "1/sqrt(9 - x**2)",
        3: "x**2/sqrt(16 + x**2)",
        4: "1/(x * sqrt(x**2 - 25))"
    }

    menu_interactivo()
    
    # Cambiar este número para probar diferentes funciones
    opcion = 1  # Se puedes cambiar a 2, 3, o 4
    
    func_str = funciones_predefinidas[opcion]
    funcion = sp.sympify(func_str)

    #resuelve
    resolvedor = SustitucionTrigonometricaInteractiva(funcion, x)
    resultado = resolvedor.resolver()