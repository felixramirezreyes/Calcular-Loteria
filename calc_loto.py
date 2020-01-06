'''
Calcular los posibles numeros de una loteria, basado en la entrada de dos
grupos de una coleccion de tresy el resultado sera la diferencia indivudual.
'''
import os

from datetime import datetime
from collections import Counter

from flask import Flask, render_template, request, flash, redirect, url_for
from flask import g
from flask_toastr import Toastr
# from flask_debugtoolbar import DebugToolbarExtension

from forms import LoteriaForm, SorteoForm, FrecPorDiaForm
from db import db
from models import Loteria, Sorteo


db_dir = os.path.dirname(os.path.abspath(__file__))
db_file = f'sqlite:///{os.path.join(db_dir, "loto.db")}'

print('db_file:', db_file)

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Llave_Muy_Secreta'
app.config['TOASTR_TIMEOUT'] = 15000

toastr = Toastr()
# deboogtoolb = DebugToolbarExtension()

toastr.init_app(app)
# deboogtoolb.init_app(app)

db.init_app(app)

meses = ('Mes-Incorrecto',
         'Enero',
         'Febrero',
         'Marzo',
         'Abril',
         'Mayo',
         'Junio',
         'Julio',
         'Agosto',
         'Septiembre',
         'Octubre',
         'Noviebre',
         'Diciembre')


def crear_muestra():
    db.session.remove()
    db.drop_all()

    db.create_all()
    db.session.commit()
    print('Limpio')

    loto1 = Loteria(nombre='La Nacional', activo=1)
    loto2 = Loteria(nombre='Loteca', activo=1)

    sorteo1 = Sorteo(loteria_id=1,
                     premio_loto1=21,
                     premio_loto2=15,
                     premio_loto3=22,
                     premio_ref1=13,
                     premio_ref2=25,
                     premio_ref3=28,
                     premio_calc1=abs(21 - 13),
                     premio_calc2=abs(15 - 25),
                     premio_calc3=abs(22 - 28))

    db.session.add(loto1)
    db.session.add(loto2)
    db.session.add(sorteo1)
    db.session.commit()

    print('Ok!')


def buscar_historial(numero):
    if numero == 0:
        qry_result = Sorteo.query.with_entities(
            Sorteo.fecha,
            db.case(
                {
                    0: 'Domingo',
                    1: 'Lunes',
                    2: 'Martes',
                    3: 'Miercoles',
                    4: 'Jueves',
                    5: 'Viernes',
                    6: 'Sabado'
                },
                value=db.extract('dow', Sorteo.fecha)).label('dia'),
            Sorteo.premio_loto1, Sorteo.premio_loto2,
            Sorteo.premio_loto3).all()
    else:
        qry_result = Sorteo.query.with_entities(
            Sorteo.fecha,
            db.case(
                {
                    0: 'Domingo',
                    1: 'Lunes',
                    2: 'Martes',
                    3: 'Miercoles',
                    4: 'Jueves',
                    5: 'Viernes',
                    6: 'Sébado'
                },
                value=db.extract('dow', Sorteo.fecha)).label('dia'),
            Sorteo.premio_loto1, Sorteo.premio_loto2,
            Sorteo.premio_loto3).filter(
                db.extract('day', Sorteo.fecha) == numero).all()
    return qry_result


@app.template_filter()
def formato_id(valor=0):
    valor = int(valor)
    return f'{valor:03d}'


@app.template_filter()
def formato_premios(valor=0):
    valor = int(valor)
    return f'{valor:02d}'


@app.template_filter()
def formato_fechahora(fecha):
    if fecha:
        fechaf = fecha.strftime('%d %m %Y a las %I:%M %p')

        # Formato de la fecha ejemplo: 27-08-2019 a las 10:44 AM
        p2 = fechaf[3:]  # ==========  08-2019 a las 10:44 AM
        mes = meses[int(p2[:2])]  # =  Devuelve 08 = meses[8] = Agosto
        p1 = fechaf[:3]  # ==========  27-
        fechaf = p1 + mes + p2[2:]  # 27-Septiembre-2019 a las 10:44 AM
    else:
        fechaf = None

    return fechaf


@app.template_filter()
def fecha_amigable(fecha,
                   pasado_='Hace',
                   futuro_='Han pasado ya',
                   default='Ahora mismo'):
    '''
    Devuelve una cadena representando la hora desde o hasta
    Ejemplo: 3 dias hace ya, 5 han pasado ya
    '''
    hoy = datetime.now()

    if hoy > fecha:
        dif = hoy - fecha
        fecha_pasada = True
    else:
        dif = fecha - hoy
        fecha_pasada = False

    periodos = ((dif.days / 365, "año", "años"),
                (dif.days / 30, "mes", "meses"),
                (dif.days / 7, "semana", "semanas"),
                (dif.days, "día", "días"),
                (dif.seconds / 3600, "hora", "horas"),
                (dif.seconds / 60, "minuto", "minutos"),
                (dif.seconds, "segundo", "segundos"),)

    for periodo, singular, plurar in periodos:
        if int(periodo) > 0:
            return '%s %d %s' % (pasado_ if fecha_pasada else futuro_,
                                 periodo,
                                 singular if periodo < 2 else plurar)

    return default


@app.route('/')
def home():
    return redirect(url_for('listar_sorteos'))


@app.route('/crear_loteria', methods=['GET', 'POST'])
def crear_loteria():
    form = LoteriaForm()

    if form.validate_on_submit():
        try:
            # Confirmar que no exista el nombre de la loteria a crear
            loteria = Loteria.query.filter_by(nombre=form.nombre.data).first()

            if loteria is None:
                loteria = Loteria(nombre=form.nombre.data,
                                  activo=form.activo.data)
            else:
                flash(f'La loteria: {form.nombre.data}, ya existe', 'error')

                form = LoteriaForm(obj=loteria)
                return render_template('loteria.html', form=form)

            loteria.grabar_loteria()
            flash(f'Lotaria: {form.nombre.data}, Guardada!', 'success')
            return redirect(url_for('listar_loterias'))
        except Exception:
            flash(f'Error grabando la loteria: {form.nombre.data}', 'error')
            return redirect(request.path)

    return render_template('loteria.html', form=form)


@app.route('/editar_loteria/<int:id>', methods=['GET', 'POST'])
def editar_loteria(id):
    loteria = Loteria.query.filter_by(id=id).first()

    if request.method == 'GET':
        form = LoteriaForm(obj=loteria)  # , csrf_enabled=False

        if not loteria:
            flash(f'Error cargando loteria {loteria}', 'info')
            # return redirect(redirect.referrer)

        return render_template('loteria.html', form=form, nuevo=False)

    if request.method == 'POST':
        form = LoteriaForm()

        if form.validate_on_submit():
            if form.guardar.data:
                loteria.nombre = form.nombre.data
                loteria.activo = form.activo.data

                try:
                    loteria.editar_loteria()
                    flash(f'Lotaria: {form.nombre.data}, Guardada!', 'success')
                except Exception:
                    flash('Error grabando la loteria', 'error')

            if form.borrar.data:
                try:
                    loteria.borrar_loteria()
                    flash(f'Loteria {id} {loteria.nombre} Borrada!', 'info')
                except Exception:
                    flash('Error al borrar la loteria', 'error')

            if form.cancelar.data:
                flash(f'Cambios para la loteria {loteria.nombre}, Ignorados!',
                      'info')

            return redirect(url_for('listar_loterias'))
        else:
            return str(form.errors)


@app.route('/listar_loterias')
def listar_loterias():
    loterias = Loteria.query.all()
    return render_template('listar_loterias.html', loterias=loterias)


@app.route('/agregar_sorteo', methods=['GET', 'POST'])
def agregar_sorteo():
    form = SorteoForm()

    if form.validate_on_submit():
        nombre_lot = dict(form.loteria.choices).get(form.loteria.data)

        if nombre_lot is None:
            nombre_lot = ''

        sorteo = Sorteo(fecha=form.fecha.data,
                        loteria_id=form.loteria.data,
                        premio_loto1=form.premio_loto1.data,
                        premio_loto2=form.premio_loto2.data,
                        premio_loto3=form.premio_loto3.data,
                        premio_ref1=form.premio_ref1.data,
                        premio_ref2=form.premio_ref2.data,
                        premio_ref3=form.premio_ref3.data,
                        premio_calc1=form.premio_calc1.data,
                        premio_calc2=form.premio_calc2.data,
                        premio_calc3=form.premio_calc3.data)

        try:
            sorteo.grabar_sorteo()
        except Exception as e:
            mensaje = (f'Error grabando el sorteo: {nombre_lot}'
                       f'Error Original: {str(e)}')
            flash(mensaje, 'error')
            return redirect(request.url)

        mensaje = (f'Sorteo de la Loeteria {nombre_lot}, Guardado!')
        flash(mensaje, 'success')

        return redirect(url_for('listar_sorteos'))

    return render_template('agregar_sorteo.html', form=form)


@app.route('/editar_sorteo/<int:id>', methods=['GET', 'POST'])
def editar_sorteo(id):
    sorteo = Sorteo.query.filter_by(id=id).first()

    if request.method == 'GET':
        form = SorteoForm(obj=sorteo)  # , csrf_enabled=False

        if not sorteo:
            flash(f'Error cargando el sorteo: {id}', 'info')
            return redirect(redirect.referrer)

        return render_template('agregar_sorteo.html', form=form, nuevo=False)

    if request.method == 'POST':
        form = SorteoForm()

        if form.validate_on_submit():
            nombre_lot = dict(form.loteria.choices).get(form.loteria.data)

            if form.guardar.data:
                sorteo.fecha = form.fecha.data
                sorteo.loteria_id = form.loteria.data
                sorteo.premio_loto1 = form.premio_loto1.data
                sorteo.premio_loto2 = form.premio_loto2.data
                sorteo.premio_loto3 = form.premio_loto3.data
                sorteo.premio_ref1 = form.premio_ref1.data
                sorteo.premio_ref2 = form.premio_ref2.data
                sorteo.premio_ref3 = form.premio_ref3.data
                sorteo.premio_calc1 = form.premio_calc1.data
                sorteo.premio_calc2 = form.premio_calc2.data
                sorteo.premio_calc3 = form.premio_calc3.data

                try:
                    sorteo.editar_sorteo()

                    mensaje = (f'Sorteo ID: {id}'
                               f' de la Loeteria {nombre_lot}'
                               f', Guardado!')
                    flash(mensaje, 'success')
                except Exception:
                    mensaje = (f'Error al grabar el Sorteo ID: {id}'
                               f' de la Loeteria {nombre_lot}')
                    flash(mensaje, 'error')

            if form.borrar.data:
                try:
                    sorteo.borrar_sorteo()

                    mensaje = (f'Sorteo ID: {id}'
                               f' de la Loeteria {nombre_lot}'
                               f', Borrado!')
                    flash(mensaje, 'success')
                except Exception:
                    mensaje = (f'Error al grabar el Sorteo ID: {id}'
                               f' de la Loeteria {nombre_lot}')
                    flash(mensaje, 'error')

            if form.cancelar.data:
                mensaje = (f'Cambios para el Sorteo ID: {id}'
                           f' de la Loeteria {nombre_lot} Ignorados')
                flash(mensaje, 'info')

            return redirect(url_for('listar_sorteos'))
        else:
            print('ERROR:\n', form.errors)
            flash(form.errors, 'error')
            return redirect(url_for('editar_sorteo', id=form.loteria.data))

            # return str(form.errors)


@app.route('/listar_sorteos')
def listar_sorteos():
    sorteos = Sorteo.query.all()
    return render_template('listar_sorteos.html', sorteos=sorteos)


# Estadisticas globales
@app.route('/estadisticas1')
def estadisticas1():
    sorteos = Sorteo.query.all()

    salidores = [sorteo.premio_loto1 for sorteo in sorteos]
    salidores += [sorteo.premio_loto2 for sorteo in sorteos]
    salidores += [sorteo.premio_loto3 for sorteo in sorteos]

    mas_salen = Counter(salidores).most_common(6)
    menos_salen = sorted(mas_salen, key=lambda tup: tup[1])
    no_salen = [(i, 0) for i in range(1, 101) if i not in mas_salen]

    return render_template('estadisticas1.html',
                           mas_salen=mas_salen,
                           menos_salen=menos_salen,
                           no_salen=no_salen)


# Estadisticas historial de un numero
@app.route('/estadisticas2', methods=['GET', 'POST'])
def estadisticas2():
    form = FrecPorDiaForm()
    mostrar_resultado = False
    qry_result = None

    # if form.validate_on_submit():
    if form.buscar.data:
        qry_result = buscar_historial(form.dia_mes.data)
        mostrar_resultado = True

    return render_template('estadisticas2.html',
                           form=form,
                           mostrar_resultado=mostrar_resultado,
                           numeros=qry_result)


# Estadisticas historial de un numero
@app.route('/estadisticas3/<int:numero>')
def estadisticas3(numero):
    sorteos_p1 = Sorteo.query.filter_by(premio_loto1=numero)
    sorteos_p2 = Sorteo.query.filter_by(premio_loto2=numero)
    sorteos_p3 = Sorteo.query.filter_by(premio_loto3=numero)
    sorteos = sorteos_p1.union(sorteos_p2).union(sorteos_p3).all()

    return render_template('estadisticas3.html',
                           sorteos=sorteos)


@app.route('/inicializar_db')
def inicializar_db():
    with app.app_context():
        print('Inicializando DB, Espere...')

        crear_muestra()

        print('DB Inicializada!')
    return 'DB Inicializada!'


# Para probar libreria Flast-Toastr
@app.route('/testmsg')
def testmsg():
    g.mensaje = 'All Ok!'

    flash(g.mensaje)
    flash("All OK", 'success')
    flash("All Normal", 'info')
    flash("Not So OK", 'error')
    flash("So So", 'warning')
    return render_template('test1.html', g=g)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
