from datetime import datetime
from db import db


class Loteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    fecha_c = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Loteria: {self.nombre}'

    @classmethod
    def find_by_name(cls, nombre):
        return cls.query.filter_by(nombre=nombre).all()

    def grabar_loteria(self):
        db.session.add(self)
        db.session.commit()

    def editar_loteria(self):
        print('Editar loteria guardada')
        db.session.commit()

    def borrar_loteria(self):
        db.session.delete(self)
        db.session.commit()


class Sorteo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    loteria_id = db.Column(db.Integer, db.ForeignKey('loteria.id'), nullable=False)
    premio_loto1 = db.Column(db.Integer, nullable=False)
    premio_loto2 = db.Column(db.Integer, nullable=False)
    premio_loto3 = db.Column(db.Integer, nullable=False)
    premio_ref1 = db.Column(db.Integer, nullable=False)
    premio_ref2 = db.Column(db.Integer, nullable=False)
    premio_ref3 = db.Column(db.Integer, nullable=False)
    premio_calc1 = db.Column(db.Integer, nullable=False)
    premio_calc2 = db.Column(db.Integer, nullable=False)
    premio_calc3 = db.Column(db.Integer, nullable=False)
    fecha_c = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    loteria = db.relationship('Loteria', backref=db.backref('sorteo', lazy=True))

    def __repr__(self):
        return f'Sorteo: {self.fecha}, {self.loteria.nombre}, {self.premio_loto1}, {self.premio_loto2}, {self.premio_loto3}'

    def grabar_sorteo(self):
        db.session.add(self)
        db.session.commit()

    def editar_sorteo(self):
        db.session.commit()

    def borrar_sorteo(self):
        db.session.delete(self)
        db.session.commit()
