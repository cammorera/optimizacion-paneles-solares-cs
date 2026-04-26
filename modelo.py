from pulp import *

def resolver_optimizacion(area_techo=150, consumo_mensual=445, horas_sol=4.5):
    """Resuelve el LP de inversión en paneles solares para la Tarea 3"""
    modelo = LpProblem('Optimizacion_Solar', LpMinimize)

    # Variables de decisión: Cantidad de paneles (deben ser enteros)
    x = LpVariable('Panel_A', lowBound=0, cat='Integer')
    y = LpVariable('Panel_B', lowBound=0, cat='Integer')
    z = LpVariable('Panel_C', lowBound=0, cat='Integer')

    # Función objetivo: Minimizar Inversión (Costos: A=$190, B=$205, C=$255)
    # Fuente: Tarea 1 - Especificaciones de paneles
    modelo += 190*x + 205*y + 255*z

    # Cálculo de rendimientos mensuales (kWh/mes) basado en la Tarea 1:
    # Rendimiento = Potencia(kW) * Horas Sol * 30 días
    # Panel A: 0.40 * h * 30 | Panel B: 0.45 * h * 30 | Panel C: 0.55 * h * 30
    rend_a = 0.40 * horas_sol * 30
    rend_b = 0.45 * horas_sol * 30
    rend_c = 0.55 * horas_sol * 30

    # Restricciones
    # 1. Cubrir la demanda energética mensual
    modelo += rend_a*x + rend_b*y + rend_c*z >= consumo_mensual, 'Demanda_Energia'

    # 2. No exceder el área del techo (m²)
    # Áreas: A=1.9, B=2.1, C=2.5
    modelo += 1.9*x + 2.1*y + 2.5*z <= area_techo, 'Limite_Espacio'

    # Resolver el modelo (silencioso para Streamlit)
    modelo.solve(PULP_CBC_CMD(msg=0))

    # Definir resultados
    # Se utiliza una validación para evitar errores si no hay solución
    status = LpStatus[modelo.status]
    val_x = x.varValue if x.varValue is not None else 0
    val_y = y.varValue if y.varValue is not None else 0
    val_z = z.varValue if z.varValue is not None else 0
    obj_val = value(modelo.objective) if value(modelo.objective) is not None else 0
    area_usada = 1.9*val_x + 2.1*val_y + 2.5*val_z

    return {
        "status": status,
        "x": val_x,
        "y": val_y,
        "z": val_z,
        "costo": obj_val,
        "area_usada": area_usada,
        "total_paneles": val_x + val_y + val_z
    }
