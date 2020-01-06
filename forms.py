'''Formularios para las vistas'''
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, IntegerField
from wtforms import BooleanField, SelectField, SubmitField, validators
from wtforms import SelectField, DateTimeField
# from wtforms.fields.html5 import DateTimeField
# from models import Loteria, listloterias


class LoteriaForm(FlaskForm):
    nombre = StringField('Nombre',
                         [validators.InputRequired(
                           'El nombre de la loteria es obligario')])
    activo = BooleanField('Activa',
                          [validators.InputRequired(
                           'Este campo es obligario')],
                           default=True)
    guardar = SubmitField()
    borrar = SubmitField()
    cancelar = SubmitField()


class SorteoForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(SorteoForm, self).__init__(*args, **kwargs)

        from models import Loteria

        self.loteria.choices = [(l.id, l.nombre)
                                for l in Loteria.query.filter_by(activo=True).all()]

    fecha = DateTimeField('Fecha del sorteo',
                          format='%d-%m-%Y %H:%M:%S')

    loteria = SelectField('Loteria', coerce=int)

    premio_loto1 = IntegerField('Primer premio',
                                [validators.InputRequired(
                                 'Este campo es obligario')],
                               render_kw={'id': 'premio_loto1'})
    premio_loto2 = IntegerField('Segundo premio',
                                [validators.InputRequired(
                                 'Este campo es obligario')],
                               render_kw={'id': 'premio_loto2'})
    premio_loto3 = IntegerField('Tercer premio',
                                [validators.InputRequired(
                                 'Este campo es obligario')],
                               render_kw={'id': 'premio_loto3'})
    premio_ref1 = IntegerField('Ref. al 1.er premio',
                               render_kw={'id': 'premio_ref1'})
    premio_ref2 = IntegerField('Ref. al 2.do premio',
                               render_kw={'id': 'premio_ref2'})
    premio_ref3 = IntegerField('Ref. al 3.er premio',
                               render_kw={'id': 'premio_ref3'})
    premio_calc1 = IntegerField('1.er calculado',
                               render_kw={'id': 'premio_calc1'})
    premio_calc2 = IntegerField('2.do calculado',
                               render_kw={'id': 'premio_calc2'})
    premio_calc3 = IntegerField('3.er calculado',
                               render_kw={'id': 'premio_calc3'})
    guardar = SubmitField()
    borrar = SubmitField()
    cancelar = SubmitField()


class FrecPorDiaForm(FlaskForm):
    dias_semana = [(1, 'Domingo'),
                   (2, 'Lunes'),
                   (3, 'Martes'),
                   (4, 'Miercoles'),
                   (5, 'Jueves'),
                   (6, 'Vieernes'),
                   (7, 'Sabado')]
    dias_mes = [(dia, str(dia)) for dia in range(0, 33)]

    '''
    dia_nombre_semana = SelectField('Día de la Semana o Dia del Mes',
                                     choices=[(1, 'Día de la semana'),
                                              (2, 'Día del mes')],
                                     coerce=int)
    dia_semana = SelectField('Días de la Semana',
                             choices=dias_semana,
                             coerce=int)
    '''
    dia_mes = SelectField('Días del Mes',
                          choices=dias_mes,
                          coerce=int)
    buscar = SubmitField()
