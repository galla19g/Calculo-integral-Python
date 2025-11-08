"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    MODELADO COMPUTACIONAL DE INTEGRALES POR SUSTITUCIÓN TRIGONOMÉTRICA       ║
║                                                                              ║
║    Asignatura: Cálculo Integral                                              ║
║    Programa: Tecnología en Desarrollo de Software - UNIPUTUMAYO              ║
║    Descripción:                                                              ║
║    Programa que resuelve integrales por sustitución trigonométrica de        ║
║    forma paso a paso, detectando automáticamente el patrón y aplicando       ║
║    las identidades trigonométricas apropiadas.                               ║
║                                                                              ║
║    Patrones soportados:                                                      ║
║    • √(a² - x²) → x = a·sen(θ)  [Identidad: 1 - sen²(θ) = cos²(θ)]           ║
║    • √(a² + x²) → x = a·tan(θ)  [Identidad: 1 + tan²(θ) = sec²(θ)]           ║
║    • √(x² - a²) → x = a·sec(θ)  [Identidad: sec²(θ) - 1 = tan²(θ)]           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

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
x, a_sym, theta = symbols('x a theta', real=True, positive=True)

# ---------- Configuración de impresión ----------
def formatear_expresion(expr):
    """
    Formatea una expresión de SymPy para presentación limpia.
    Elimina .0 de números enteros y mejora la visualización.
    """
    expr_str = str(expr)
    # Reemplazar patrones comunes
    expr_str = expr_str.replace('.0', '')
    expr_str = expr_str.replace('**', '^')
    expr_str = expr_str.replace('*', '·')
    expr_str = expr_str.replace('sqrt', '√')
    return expr_str

def expr_a_latex_limpio(expr):
    """
    Convierte expresión a LaTeX sin decimales innecesarios.
    """
    latex_str = latex(expr)
    # Simplificar números enteros
    import re
    latex_str = re.sub(r'(\d+)\.0+(?!\d)', r'\1', latex_str)
    return latex_str

# ---------- Helpers de impresión ASCII mejorados ----------
def linea(sep='─', largo=80):
    """Línea horizontal decorativa"""
    print(sep * largo)

def linea_doble(largo=80):
    """Línea doble para títulos principales"""
    print('═' * largo)

def mostrar_titulo_principal(texto):
    """Título principal con formato destacado"""
    print()
    linea_doble()
    print(f"║  {texto.center(76)}  ║")
    linea_doble()
    print()

def mostrar_titulo_seccion(texto, numero=None):
    """Título de sección con numeración"""
    print()
    if numero:
        linea()
        print(f"┌─ PASO {numero}: {texto}")
        linea()
    else:
        linea()
        print(f"┌─ {texto}")
        linea()
    print()

def mostrar_subtitulo(texto):
    """Subtítulo con formato suave"""
    print(f"\n  ► {texto}")
    print(f"  {'─' * (len(texto) + 4)}")

def mostrar_contenido(etiqueta, contenido, indent=4):
    """Muestra contenido con etiqueta"""
    espacios = ' ' * indent
    print(f"{espacios}• {etiqueta}:")
    if isinstance(contenido, str):
        for linea in contenido.split('\n'):
            print(f"{espacios}  {linea}")
    else:
        print(f"{espacios}  {contenido}")
    print()

def mostrar_formula(descripcion, expr_sympy=None, expr_latex=None):
    """Muestra una fórmula con formato mejorado y limpio"""
    print(f"    ┌─ {descripcion}")
    if expr_sympy is not None:
        print(f"    │")
        # Crear representación matemática limpia
        from sympy.printing import pretty
        pretty_str = pretty(expr_sympy, use_unicode=True)
        
        # Limpiar decimales innecesarios
        pretty_str = pretty_str.replace('.0 ', ' ')
        pretty_str = pretty_str.replace('.0\n', '\n')
        pretty_str = pretty_str.replace('.0)', ')')
        pretty_str = pretty_str.replace('.0²', '²')
        pretty_str = pretty_str.replace('.0*', '*')
        
        for linea in pretty_str.split('\n'):
            print(f"    │   {linea}")
    if expr_latex is not None:
        # Limpiar LaTeX de decimales
        import re
        expr_latex = re.sub(r'(\d+)\.0+(?!\d)', r'\1', expr_latex)
        print(f"    │")
        print(f"    │   LaTeX: {expr_latex}")
    print(f"    └{'─' * 70}")
    print()

def mostrar_caja_info(titulo, contenido):
    """Muestra información en una caja destacada"""
    ancho = 76
    print(f"\n    ╔{'═' * ancho}╗")
    print(f"    ║  {titulo.center(ancho-2)}  ║")
    print(f"    ╠{'═' * ancho}╣")
    for linea in contenido.split('\n'):
        padding = ancho - len(linea) - 2
        print(f"    ║  {linea}{' ' * padding}  ║")
    print(f"    ╚{'═' * ancho}╝\n")

def mostrar_resultado_destacado(titulo, resultado_sympy, latex_str=None):
    """Muestra un resultado importante destacado sin decimales"""
    print()
    print(f"    {'▓' * 78}")
    print(f"    ▓  {titulo.upper().center(74)}  ▓")
    print(f"    {'▓' * 78}")
    print()
    
    from sympy.printing import pretty
    pretty_str = pretty(resultado_sympy, use_unicode=True)
    
    # Limpiar decimales
    pretty_str = pretty_str.replace('.0 ', ' ')
    pretty_str = pretty_str.replace('.0\n', '\n')
    pretty_str = pretty_str.replace('.0)', ')')
    pretty_str = pretty_str.replace('.0²', '²')
    
    for linea in pretty_str.split('\n'):
        print(f"        {linea}")
    
    if latex_str:
        import re
        latex_str = re.sub(r'(\d+)\.0+(?!\d)', r'\1', latex_str)
        print()
        print(f"        LaTeX: {latex_str}")
    
    print()
    print(f"    {'▓' * 78}")
    print()

# ---------- Clase Triángulo mejorada ----------
class TrianguloRectangulo:
    """Clase para visualizar triángulos rectángulos con diseño mejorado."""

    def __init__(self, tipo, parametro_a):
        self.tipo = tipo
        try:
            self.a = float(parametro_a)
        except Exception:
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
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f8f9fa')

        if self.tipo == 'tipo1':
            vertices = np.array([[0, 0], [3.5, 0], [3.5, 2.5]])
            labels = {
                'base': f'x',
                'altura': f'√({self.a}² - x²)',
                'hipotenusa': f'{self.a}'
            }
            titulo = f'Triángulo Rectángulo: √({self.a}² - x²)'
            sustitucion = f'x = {self.a}·sen(θ)'
            identidad = '1 - sen²(θ) = cos²(θ)'
        elif self.tipo == 'tipo2':
            vertices = np.array([[0, 0], [3, 0], [3, 4]])
            labels = {
                'base': f'x',
                'altura': f'{self.a}',
                'hipotenusa': f'√({self.a}² + x²)'
            }
            titulo = f'Triángulo Rectángulo: √({self.a}² + x²)'
            sustitucion = f'x = {self.a}·tan(θ)'
            identidad = '1 + tan²(θ) = sec²(θ)'
        else:
            vertices = np.array([[0, 0], [3, 0], [3, 4]])
            labels = {
                'base': f'√(x² - {self.a}²)',
                'altura': f'{self.a}',
                'hipotenusa': f'x'
            }
            titulo = f'Triángulo Rectángulo: √(x² - {self.a}²)'
            sustitucion = f'x = {self.a}·sec(θ)'
            identidad = 'sec²(θ) - 1 = tan²(θ)'

        # Dibujar triángulo
        triangle = patches.Polygon(vertices, fill=False, edgecolor='#2563eb', linewidth=3)
        ax.add_patch(triangle)

        # Ángulo theta
        angle = patches.Arc((0, 0), 0.8, 0.8, angle=0, theta1=0, theta2=40,
                            color='#dc2626', linewidth=2.5)
        ax.add_patch(angle)
        ax.text(0.5, 0.15, 'θ', fontsize=14, color='#dc2626', weight='bold')

        # Ángulo recto
        square = patches.Rectangle((vertices[1][0]-0.25, vertices[1][1]),
                                0.25, 0.25, fill=False, edgecolor='#2563eb', linewidth=2)
        ax.add_patch(square)

        # Etiquetas de lados
        ax.text(1.8, -0.4, labels['base'], fontsize=11, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef3c7', alpha=0.9, edgecolor='#f59e0b'))
        ax.text(4.0, 1.5, labels['altura'], fontsize=11, rotation=90, va='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#dbeafe', alpha=0.9, edgecolor='#3b82f6'))
        ax.text(1.4, 1.4, labels['hipotenusa'], fontsize=11, rotation=30, weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0e7ff', alpha=0.9, edgecolor='#6366f1'))

        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-0.8, 5.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Título y información
        plt.title(titulo, fontsize=14, weight='bold', pad=20)
        
        info_box = f'Sustitución: {sustitucion}\nIdentidad: {identidad}'
        ax.text(0.1, 5.0, info_box, fontsize=10, 
                bbox=dict(boxstyle='round,pad=0.8', facecolor='#f0fdf4', 
                         alpha=0.95, edgecolor='#22c55e', linewidth=2))

        plt.tight_layout()

        if guardar:
            plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
            print(f"\n    ✓ Triángulo guardado en '{nombre_archivo}'\n")
        else:
            plt.show()

# ---------- Clase principal mejorada ----------
class SustitucionTrigonometricaInteractiva:
    def __init__(self, funcion, variable=x):
        self.funcion = funcion
        self.variable = variable
        self.tipo_sustitucion = None
        self.parametro_a = None
        self.triangulo = None

    def detectar_tipo_sustitucion(self) -> Optional[str]:
        mostrar_titulo_seccion("Análisis y Detección del Patrón", 1)
        
        mostrar_subtitulo("Función Original")
        
        # Crear representación limpia de la integral
        from sympy.printing import pretty
        funcion_pretty = pretty(self.funcion, use_unicode=True)
        funcion_pretty = funcion_pretty.replace('.0 ', ' ').replace('.0)', ')')
        
        print(f"    Integral a resolver:")
        print()
        for linea in funcion_pretty.split('\n'):
            print(f"         {linea}")
        print(f"    ∫ ─────────────── dx")
        print()
        
        latex_limpio = expr_a_latex_limpio(self.funcion)
        mostrar_formula("Expresión LaTeX", None, r'\int ' + latex_limpio + r' \, dx')

        func_str = str(self.funcion)

        # Patrones de detección
        patron1 = re.search(r'sqrt\(\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*x\*\*2\s*\)', func_str)
        patron2 = re.search(r'sqrt\(\s*([0-9]+(?:\.[0-9]+)?)\s*\+\s*x\*\*2\s*\)', func_str)
        patron3 = re.search(r'sqrt\(\s*x\*\*2\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*\)', func_str)

        if patron1:
            a_cuadrado = int(float(patron1.group(1)))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo1'
            
            info = (
                f"Forma detectada: √(a² - x²)\n"
                f"Donde: a² = {a_cuadrado}  →  a = {self.parametro_a}\n\n"
                f"Sustitución a usar: x = {self.parametro_a}·sen(θ)\n"
                f"Identidad pitagórica: 1 - sen²(θ) = cos²(θ)"
            )
            mostrar_caja_info("✓ PATRÓN TIPO 1", info)
            return 'tipo1'

        if patron2:
            a_cuadrado = int(float(patron2.group(1)))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo2'
            
            info = (
                f"Forma detectada: √(a² + x²)\n"
                f"Donde: a² = {a_cuadrado}  →  a = {self.parametro_a}\n\n"
                f"Sustitución a usar: x = {self.parametro_a}·tan(θ)\n"
                f"Identidad pitagórica: 1 + tan²(θ) = sec²(θ)"
            )
            mostrar_caja_info("✓ PATRÓN TIPO 2", info)
            return 'tipo2'

        if patron3:
            a_cuadrado = int(float(patron3.group(1)))
            self.parametro_a = sp.Integer(int(math.sqrt(a_cuadrado)))
            self.tipo_sustitucion = 'tipo3'
            
            info = (
                f"Forma detectada: √(x² - a²)\n"
                f"Donde: a² = {a_cuadrado}  →  a = {self.parametro_a}\n\n"
                f"Sustitución a usar: x = {self.parametro_a}·sec(θ)\n"
                f"Identidad pitagórica: sec²(θ) - 1 = tan²(θ)"
            )
            mostrar_caja_info("✓ PATRÓN TIPO 3", info)
            return 'tipo3'

        mostrar_contenido("Advertencia", "No se detectó un patrón estándar automáticamente.")
        return None

    def construir_triangulo_rectangulo(self):
        mostrar_titulo_seccion("Construcción del Triángulo Rectángulo", 2)
        
        mostrar_subtitulo("Representación Geométrica")
        print("    El triángulo rectángulo nos ayuda a visualizar las relaciones trigonométricas")
        print("    y facilita el proceso de sustitución y desustitución.\n")
        
        self.triangulo = TrianguloRectangulo(self.tipo_sustitucion, self.parametro_a)
        
        try:
            self.triangulo.dibujar_triangulo()
        except Exception as e:
            print(f"    ⚠ Advertencia: No se pudo mostrar el triángulo gráficamente.")
        
        mostrar_subtitulo("Verificación del Teorema de Pitágoras")
        
        if self.tipo_sustitucion == 'tipo1':
            latex_pitagoras = f'{self.parametro_a}^2 = x^2 + (\\sqrt{{{self.parametro_a}^2 - x^2}})^2'
        elif self.tipo_sustitucion == 'tipo2':
            latex_pitagoras = f'(\\sqrt{{{self.parametro_a}^2 + x^2}})^2 = x^2 + {self.parametro_a}^2'
        else:
            latex_pitagoras = f'x^2 = (\\sqrt{{x^2 - {self.parametro_a}^2}})^2 + {self.parametro_a}^2'
        
        print(f"    LaTeX: {latex_pitagoras}\n")

    def aplicar_sustitucion(self):
        mostrar_titulo_seccion("Aplicación de la Sustitución Trigonométrica", 3)
        
        if self.tipo_sustitucion == 'tipo1':
            x_sust = self.parametro_a * sin(theta)
            dx_sust = self.parametro_a * cos(theta)
        elif self.tipo_sustitucion == 'tipo2':
            x_sust = self.parametro_a * tan(theta)
            dx_sust = self.parametro_a * sec(theta)**2
        else:
            x_sust = self.parametro_a * sec(theta)
            dx_sust = self.parametro_a * sec(theta) * tan(theta)

        mostrar_subtitulo("Sustituciones")
        mostrar_formula("Variable x", x_sust, f'x = {latex(x_sust)}')
        mostrar_formula("Diferencial dx", dx_sust, f'dx = {latex(dx_sust)} \\, d\\theta')

        func_sustituida = sp.simplify(self.funcion.subs(self.variable, x_sust))
        expresion_completa = func_sustituida * dx_sust
        
        mostrar_subtitulo("Integral Transformada")
        mostrar_formula("Nueva integral en θ", expresion_completa, 
                       r'\int ' + latex(expresion_completa) + r' \, d\theta')

        return func_sustituida, dx_sust

    def simplificar_con_pitagoras(self, expresion):
        mostrar_titulo_seccion("Simplificación con Identidades Pitagóricas", 4)
        
        mostrar_subtitulo("Expresión Antes de Simplificar")
        print(f"    {sp.pretty(expresion)}\n")

        expr_simplificada = trigsimp(simplify(expresion))

        if self.tipo_sustitucion == 'tipo1':
            explicacion = (
                f"Identidad aplicada: 1 - sen²(θ) = cos²(θ)\n\n"
                f"Al sustituir x = {self.parametro_a}·sen(θ) en √({self.parametro_a}² - x²):\n"
                f"√({self.parametro_a}² - ({self.parametro_a}·sen(θ))²) = √({self.parametro_a}²(1 - sen²(θ)))\n"
                f"                                  = √({self.parametro_a}²·cos²(θ))\n"
                f"                                  = {self.parametro_a}·cos(θ)"
            )
        elif self.tipo_sustitucion == 'tipo2':
            explicacion = (
                f"Identidad aplicada: 1 + tan²(θ) = sec²(θ)\n\n"
                f"Al sustituir x = {self.parametro_a}·tan(θ) en √({self.parametro_a}² + x²):\n"
                f"√({self.parametro_a}² + ({self.parametro_a}·tan(θ))²) = √({self.parametro_a}²(1 + tan²(θ)))\n"
                f"                                  = √({self.parametro_a}²·sec²(θ))\n"
                f"                                  = {self.parametro_a}·sec(θ)"
            )
        else:
            explicacion = (
                f"Identidad aplicada: sec²(θ) - 1 = tan²(θ)\n\n"
                f"Al sustituir x = {self.parametro_a}·sec(θ) en √(x² - {self.parametro_a}²):\n"
                f"√(({self.parametro_a}·sec(θ))² - {self.parametro_a}²) = √({self.parametro_a}²(sec²(θ) - 1))\n"
                f"                                  = √({self.parametro_a}²·tan²(θ))\n"
                f"                                  = {self.parametro_a}·tan(θ)"
            )

        mostrar_caja_info("Proceso de Simplificación", explicacion)
        
        mostrar_subtitulo("Resultado Simplificado")
        mostrar_formula("Expresión simplificada", expr_simplificada, latex(expr_simplificada))

        return expr_simplificada

    def integrar_en_theta(self, expresion):
        mostrar_titulo_seccion("Integración en la Variable θ", 5)
        
        mostrar_subtitulo("Integral a Resolver")
        mostrar_formula("Integrando", expresion, r'\int ' + latex(expresion) + r' \, d\theta')
        
        integral_theta = integrate(expresion, theta)
        
        mostrar_subtitulo("Resultado de la Integración")
        mostrar_formula("Antiderivada en θ", integral_theta, latex(integral_theta) + r' + C')
        
        return integral_theta

    def desustituir(self, resultado_theta):
        mostrar_titulo_seccion("Desustitución: Retorno a la Variable Original x", 6)
        
        mostrar_subtitulo("Relaciones Trigonométricas del Triángulo")
        
        resultado_x = resultado_theta

        if self.tipo_sustitucion == 'tipo1':
            relaciones = (
                f"sen(θ) = x/{self.parametro_a}\n"
                f"cos(θ) = √({self.parametro_a}² - x²)/{self.parametro_a}"
            )
            latex_rel = (f'\\sin(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\cos(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 - x^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(sin(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(cos(theta), sqrt(self.parametro_a**2 - x**2)/self.parametro_a)
            
        elif self.tipo_sustitucion == 'tipo2':
            relaciones = (
                f"tan(θ) = x/{self.parametro_a}\n"
                f"sec(θ) = √({self.parametro_a}² + x²)/{self.parametro_a}"
            )
            latex_rel = (f'\\tan(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\sec(\\theta) = \\frac{{\\sqrt{{{self.parametro_a}^2 + x^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(tan(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(sec(theta), sqrt(self.parametro_a**2 + x**2)/self.parametro_a)
            
        else:
            relaciones = (
                f"sec(θ) = x/{self.parametro_a}\n"
                f"tan(θ) = √(x² - {self.parametro_a}²)/{self.parametro_a}"
            )
            latex_rel = (f'\\sec(\\theta) = \\frac{{x}}{{{self.parametro_a}}}, \\quad '
                        f'\\tan(\\theta) = \\frac{{\\sqrt{{x^2 - {self.parametro_a}^2}}}}{{{self.parametro_a}}}')
            
            resultado_x = resultado_x.subs(sec(theta), x/self.parametro_a)
            resultado_x = resultado_x.subs(tan(theta), sqrt(x**2 - self.parametro_a**2)/self.parametro_a)

        print(f"    {relaciones}")
        print(f"\n    LaTeX: {latex_rel}\n")

        resultado_final = simplify(resultado_x)
        
        mostrar_subtitulo("Expresión Final en x")
        mostrar_formula("Resultado", resultado_final, latex(resultado_final) + r' + C')
        
        return resultado_final

    def resolver(self):
        try:
            mostrar_titulo_principal("🧮 RESOLUCIÓN DE INTEGRAL POR SUSTITUCIÓN TRIGONOMÉTRICA")
            
            tipo = self.detectar_tipo_sustitucion()
            if not tipo:
                raise ValueError("No se detectó un patrón estándar para sustitución trigonométrica.")

            self.construir_triangulo_rectangulo()
            func_sust, dx_sust = self.aplicar_sustitucion()
            expresion_completa = func_sust * dx_sust
            expr_simplificada = self.simplificar_con_pitagoras(expresion_completa)
            resultado_theta = self.integrar_en_theta(expr_simplificada)
            resultado_final = self.desustituir(resultado_theta)

            # Resultado final destacado
            mostrar_titulo_principal("✓ RESULTADO FINAL DE LA INTEGRAL")
            mostrar_resultado_destacado(
                "Solución",
                self.funcion,
                None
            )
            print("    =")
            print()
            mostrar_resultado_destacado(
                "",
                resultado_final,
                latex(resultado_final) + r' + C'
            )

            # Verificación
            mostrar_titulo_seccion("Verificación con SymPy", "✓")
            mostrar_subtitulo("Integración Directa")
            verificacion = integrate(self.funcion, x)
            mostrar_formula("Resultado de SymPy", verificacion, latex(verificacion) + r' + C')
            
            return resultado_final

        except Exception as e:
            print("\n    ❌ ERROR EN LA RESOLUCIÓN")
            print(f"    {str(e)}\n")
            return None


# ---------- Menú mejorado ----------
def menu_consola():
    """
    Menú principal para selección de funciones a integrar.
    Permite al usuario elegir entre funciones predefinidas o ingresar una personalizada.
    """
    opciones = {
        1: "1/(x**2 * sqrt(x**2 - 4))",  # Caso sugerido en el PDF
        2: "1/sqrt(9 - x**2)",
        3: "x**2/sqrt(16 + x**2)",
        4: "1/(x * sqrt(x**2 - 25))",
        5: "personalizada"
    }

    mostrar_titulo_principal("📋 MENÚ DE SELECCIÓN DE FUNCIONES")
    
    print("    Seleccione una función para integrar:\n")
    for k, v in opciones.items():
        if k == 5:
            print(f"        [{k}]  Ingresar función personalizada")
        elif k == 1:
            print(f"        [{k}]  ∫ {v} dx  ⭐ (Caso sugerido)")
        else:
            print(f"        [{k}]  ∫ {v} dx")
    print()
    print("    " + "─" * 70)
    
    # Solicitar nivel de detalle
    print("\n    Nivel de detalle:")
    print("        [1] Básico")
    print("        [2] Detallado (por defecto)")
    print("        [3] Completo con gráficos")
    
    try:
        entrada = input("\n    Ingrese opción de función [1-5] (Enter para 1): ").strip()
        opcion = int(entrada) if entrada != "" else 1
        if opcion not in opciones:
            print("\n    ⚠ Opción inválida. Usando opción 1 por defecto.\n")
            opcion = 1
    except Exception:
        print("\n    ⚠ Entrada inválida. Usando opción 1 por defecto.\n")
        opcion = 1

    # Manejo de función personalizada
    if opcion == 5:
        print("\n    Ingrese la función a integrar (use 'x' como variable)")
        print("    Ejemplo: 1/(x**2 * sqrt(x**2 - 9))")
        try:
            func_str = input("\n    f(x) = ").strip()
            if not func_str:
                func_str = opciones[1]
                print(f"    Usando función por defecto: {func_str}")
        except Exception:
            func_str = opciones[1]
            print(f"    Error. Usando función por defecto: {func_str}")
    else:
        func_str = opciones[opcion]
        print(f"\n    ✓ Función seleccionada: {func_str}\n")
    
    try:
        funcion = sp.sympify(func_str)
        resolvedor = SustitucionTrigonometricaInteractiva(funcion, x)
        resolvedor.resolver()
    except Exception as e:
        print(f"\n    ❌ Error al procesar la función: {str(e)}")
        print("    Verifique que la sintaxis sea correcta.\n")


if __name__ == "__main__":
    # Mostrar información del proyecto
    print(__doc__)
    print("\n" + "═" * 80)
    print("  INICIANDO PROGRAMA...")
    print("═" * 80 + "\n")
    
    # Ejecutar menú de consola
    menu_consola()