from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Administrador(db.Model):
    __tablename__ = "administrador"

    idAdministrador = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(128), unique=True, nullable=False)
    contraseña = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User {self.correo}>"

    def set_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    # Para convertir a JSON la respuesta

    @staticmethod
    def get_by_id(idAdministrador):
        return Administrador.query.get(idAdministrador)

    @staticmethod
    def get_by_email(correo):
        return Administrador.query.filter_by(correo=correo).first()


class Preguntas(db.Model):
    __tablename__ = "Preguntas"

    idPreguntas = db.Column(db.Integer, primary_key=True)
    textoPreguntas= db.Column(db.Text, nullable=False)
    respuestas = db.relationship("Respuestas", backref="Preguntas", lazy=True)

    # Para convertir a JSON la consulta
    def serialize(self):
        return {
            "idPreguntas": self.idPreguntas,
            "titulo": self.textoPreguntas,
        }

    def save(self):
        if not self.idPreguntas:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(idPreguntas):
        return Preguntas.query.get(idPreguntas)


class Respuestas(db.Model):
    idRespuestas = db.Column(db.Integer, primary_key=True)
    textoRespuestas = db.Column(db.Text, nullable=False)
    valorNumerico = db.Column(db.Integer, nullable=False)
    idPreguntas = db.Column(db.Integer, db.ForeignKey("Preguntas.idPreguntas"), nullable=False)

    # Para convertir a JSON la consulta
    def serialize(self):
        return {
            "idRespuestas": self.idRespuestas,
            "textoRespuestas": self.textoRespuestas,
            "valorNumerico": self.valorNumerico,
            "idPreguntas": self.idPreguntas,
        }

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(idRespuestas):
        return Respuestas.query.get(idRespuestas)


class rangoResultado(db.Model):
    idRango= db.Column(db.Integer, primary_key=True)
    rangoResultado = db.Column(db.Text, nullable=False)
    limite_inicial = db.Column(db.Integer)
    limite_final = db.Column(db.Integer)
    idRespuestas = db.Column(db.Integer, db.ForeignKey("Respuestas.idRespuestas"), nullable=False)
   

    def serialize(self):
        return {
            "id": self.idRango,
            "resultado": self.resultado,
            "limite_inicial": self.limite_inicial,
            "limite_final": self.limite_final,
            "idRespuestas": self.idRespuestas,
        }

    def save(self):
        if not self.idRango:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(idRango):
        return rangoResultado.query.get(idRango)
