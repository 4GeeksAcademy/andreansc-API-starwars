from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(String(12), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True)
    date_suscription: Mapped[str] = mapped_column(String(10))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    the_favorites_planets: Mapped[list['Favorites_planets']] = relationship(
        back_populates='user')
    the_favorites_characters: Mapped[list['Favorites_characters']] = relationship(
        back_populates='user')

    def __str__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'data_suscription': self.date_suscription,
            'is_active': self.is_active
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id_planet: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(12), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    climate: Mapped[str] = mapped_column(String(12), nullable=False)
    gravity: Mapped[float] = mapped_column(Float, nullable=False)
    diameter: Mapped[float] = mapped_column(Float, nullable=False)
    favorite_by: Mapped[list['Favorites_planets']
                        ] = relationship(back_populates='planet')

    def __str__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            'id_planet': self.id_planet,
            'name': self.name,
            'population': self.population,
            'climate': self.climate,
            'gravity': self.gravity,
            'diameter': self.diameter
        }


class Characters(db.Model):
    __tablename__ = 'characters'
    id_character: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10))
    skin: Mapped[str] = mapped_column(String(10))
    birth_year: Mapped[str] = mapped_column(String(10), nullable=False)
    favorite_by: Mapped[list['Favorites_characters']
                        ] = relationship(back_populates='character')

    def __str__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            'id': self.id_character,
            'name': self.name,
            'height': self.height,
            'gender': self.gender,
            'skin': self.skin,
            'birth_year': self.birth_year
        }


class Favorites_planets(db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_planet: Mapped[int] = mapped_column(ForeignKey('planets.id_planet'))
    planet: Mapped['Planets'] = relationship(back_populates='favorite_by')
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='the_favorites_planets')

    def __str__(self):
        return f'{self.user} like {self.planet}'

    def serialize(self):
        return {
            'id': self.id,
            'id_planet': self.id_planet,
            'id_user': self.id_user
        }


class Favorites_characters(db.Model):
    __tablename__ = 'favorites_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_character: Mapped[int] = mapped_column(
        ForeignKey('characters.id_character'))
    character: Mapped['Characters'] = relationship(
        back_populates='favorite_by')
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(
        back_populates='the_favorites_characters')

    def __str__(self):
        return f'{self.user} like {self.character}'

    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'date_suscription': self.date_suscription,  
        'is_active': self.is_active
         }
