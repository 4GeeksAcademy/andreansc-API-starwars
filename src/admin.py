import os
from flask_admin import Admin
from models import db, User, Planets, Characters, Favorites_characters, Favorites_planets
from flask_admin.contrib.sqla import ModelView

class FavoritesCharactersModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'id_character', 'character', 'id_user', 'user']

class FavoritesPlanetsModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'id_planet', 'planet', 'id_user', 'user']

class UserModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'name', 'password', 'email', 'data_suscription', 'is_ative', 'the_favorites_planets', 'the_favorites_characters']

class CharactersModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id_character', 'name', 'height', 'gender', 'skin', 'birth_year', 'favorite_by']

class PlanetMmodelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id_planet', 'name', 'population', 'climate', 'gravity', 'diameter', 'favorite_by']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(PlanetMmodelView(Planets, db.session))
    admin.add_view(FavoritesCharactersModelView(Favorites_characters, db.session))
    admin.add_view(FavoritesPlanetsModelView(Favorites_planets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))