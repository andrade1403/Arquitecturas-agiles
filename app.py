from flask_restful import Api
from . import create_app
from .microservicioventa.modelos import db, Venta
from .microservicioventa.vistas import VistaVenta, VistaVentas

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaVenta, '/ventas/<int:id_venta>')
api.add_resource(VistaVentas, '/ventas')