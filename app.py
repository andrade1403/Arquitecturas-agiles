from flask_restful import Api
from . import create_app
from .microservicioVenta.modelos import db
from .microservicioVenta.vistas import VistaVenta, VistaVentas

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaVenta, '/venta/<int:id_venta>')
api.add_resource(VistaVentas, '/ventas')