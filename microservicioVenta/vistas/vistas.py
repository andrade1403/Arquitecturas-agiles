from flask import request
from flask_restful import Resource
from ..modelos import db, Venta, VentasSchema

venta_schema = VentasSchema()

class VistaVenta(Resource):
    def get(self, id_venta):
        venta = Venta.query.filter(Venta.id == id_venta).first()
        return venta_schema.dumps(venta)

    def put(self, id_venta):
        venta = Venta.query.filter(Venta.id == id_venta).first()

        if venta is None:
            return {'mensaje': 'Venta no encontrada'}, 404
        
        else:
            venta.fecha_pedido = request.json.get('fecha_pedido', venta.fecha_pedido)
            venta.fecha_limite = request.json.get('fecha_limite', venta.fecha_limite)
            venta.estado = request.json.get('estado', venta.estado.value)
        
        db.session.commit()

        return venta_schema.dumps(venta)