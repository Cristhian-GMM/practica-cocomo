from flask import Flask, render_template, request

app = Flask(__name__)

COCOMO_CONSTANTS = {
    'organico': {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
    'semi_aplicado': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
    'acoplado': {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entrada = float(request.form.get('entrada'))
        salida = float(request.form.get('salida'))
        total = entrada + salida

        factor_organico = float(request.form.get('factor_organico'))
        factor_semi_aplicado = float(request.form.get('factor_semi_aplicado'))
        factor_acoplado = float(request.form.get('factor_acoplado'))

        if not (50 <= factor_organico <= 80):
            return render_template('index.html', error="El factor Orgánico debe estar entre 50 y 80.")
        if not (81 <= factor_semi_aplicado <= 100):
            return render_template('index.html', error="El factor Semi Aplicado debe estar entre 81 y 100.")
        if not (101 <= factor_acoplado <= 150):
            return render_template('index.html', error="El factor Acoplado debe estar entre 101 y 150.")

        tipo_proyecto = request.form.get('tipo_proyecto')
        if tipo_proyecto == 'organico':
            ldc = factor_organico * total
        elif tipo_proyecto == 'semi_aplicado':
            ldc = factor_semi_aplicado * total
        elif tipo_proyecto == 'acoplado':
            ldc = factor_acoplado * total

        mldc = ldc / 1000

        a = COCOMO_CONSTANTS[tipo_proyecto]['a']
        b = COCOMO_CONSTANTS[tipo_proyecto]['b']
        c = COCOMO_CONSTANTS[tipo_proyecto]['c']
        d = COCOMO_CONSTANTS[tipo_proyecto]['d']

        esfuerzo = a * (mldc ** b)

        esfuerzo_redondeado = round(esfuerzo)
        esfuerzo_str = f"{esfuerzo_redondeado} PERSONAS MES"

        td = c * (esfuerzo ** d)

        td_redondeado = round(td)
        td_str = f"{td_redondeado} MESES DE TRABAJO"

        cp = round(esfuerzo / td)
        cp_str = f"{cp} PERSONAS"

        p = round(ldc / esfuerzo)
        p_str = f"{p} LDC CADA MES A REALIZAR"

        salario = float(request.form.get('salario'))
        costo = round(esfuerzo * salario, 2)

        costo_ldc = round(costo / ldc, 2)

        return render_template(
            'index.html', total=total, ldc=ldc, mldc=mldc, esfuerzo=esfuerzo_str, 
            td=td_str, cp=cp_str, p=p_str, costo=costo, costo_ldc=costo_ldc
        )

    return render_template('index.html', total=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)