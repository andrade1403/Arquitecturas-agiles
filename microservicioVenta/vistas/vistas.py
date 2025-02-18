from flask import request
from datetime import datetime
from flask_restful import Resource
from ..modelos import db, Venta, VentasSchema

venta_schema = VentasSchema()

class VistaVenta(Resource):
    def get(self, id_venta):
        venta = Venta.query.filter(Venta.id == id_venta).first()
        return venta_schema.dump(venta)

    def put(self, id_venta):
        venta = Venta.query.filter(Venta.id == id_venta).first()

        if venta is not None:
            fecha_pedido = datetime.strptime(request.json['fecha_pedido'], '%Y-%m-%d')
            fecha_limite = datetime.strptime(request.json['fecha_limite'], '%Y-%m-%d')
            venta.fecha_pedido = fecha_pedido if fecha_pedido is not None else venta.fecha_pedido
            venta.fecha_limite = fecha_limite if fecha_limite is not None else venta.fecha_limite
            venta.estado = request.json.get('estado', venta.estado.value)
        
        else:
            return {'mensaje': 'Venta no encontrada'}, 404
        
        db.session.commit()

        return venta_schema.dump(venta)
    
    def delete(self, id_venta):
        venta = Venta.query.filter(Venta.id == id_venta).first()

        if venta:
            db.session.delete(venta)
            db.session.commit()
        
        else:
            return {'mensaje': 'Venta no encontrada'}, 404
        
        return '', 204

class VistaVentas(Resource):
    def get(self):
        ventas = Venta.query.all()
        return [venta_schema.dumps(venta) for venta in ventas]
    
    def post(self):
        nueva_venta = Venta(fecha_pedido = request.json['fecha_pedido'],
                            fecha_limite = request.json['fecha_limite'],
                            estado = request.json['estado'].value)
        
        db.session.add(nueva_venta)
        db.session.commit()

        return venta_schema.dump(nueva_venta)
