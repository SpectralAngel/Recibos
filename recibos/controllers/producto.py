# -*- coding: utf8 -*-
#
# Copyright (c) 2008 - 2010 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from turbogears import (controllers, identity, validators, flash, expose,
                        validate, error_handler)

from recibos import model
from detalle import Detalle


class Producto(controllers.Controller, identity.SecureResource):
    require = identity.not_anonymous()

    detalle = Detalle()

    @expose(template="recibos.templates.producto.index")
    def index(self, tg_errors=None):

        return dict(tg_errors=tg_errors)

    @error_handler(index)
    @expose(template="recibos.templates.producto.producto")
    @validate(validators=dict(producto=validators.Int()))
    def default(self, producto):

        """Muestra una casa en el cliente"""

        producto = model.Producto.get(producto)

        return dict(producto=producto, valor=producto.valor())

    @error_handler(index)
    @expose()
    @validate(validators=dict(producto=validators.Int()))
    def mostrar(self, producto):

        """Permite utilizar un formulario para mostrar una casa en el cliente"""

        return self.default(producto)

    @error_handler(index)
    @expose()
    def todos(self):

        """Responde con un listado de todas las casas disponibles"""

        return dict(productos=model.Producto.query.all())

    @error_handler(index)
    @expose()
    def activos(self):

        """Responde con un listado de todas las casas disponibles"""

        return dict(productos=model.Producto.query.filter_by(activo=True).all())

    @error_handler(index)
    @expose()
    @validate(validators=dict(producto=validators.Int(),
                              nombre=validators.String(),
                              descripcion=validators.String()))
    def editar(self, producto, nombre, descripcion):

        """Cambia datos del producto especificado"""

        producto = model.Producto.get(producto)
        producto.nombre = nombre
        producto.descripcion = descripcion

        producto.flush()

        return self.default(producto.id)

    @error_handler(index)
    @expose()
    @validate(validators=dict(nombre=validators.String(),
                              descripcion=validators.String()))
    def agregar(self, **kw):

        """Agrega un producto a la base de datos"""

        producto = model.Producto(**kw)
        producto.flush()

        return self.default(producto.id)

    @error_handler(index)
    @expose()
    @validate(validators=dict(producto=validators.Int()))
    def eliminar(self, producto):

        eliminando = model.Producto.get(producto)
        eliminando.delete()

        return self.index()

    @error_handler(index)
    @expose()
    @validate(validators=dict(producto=validators.Int()))
    def copiar(self, producto):

        """Copia un producto como una Aportacion Retrasada"""

        producto = model.Producto.get(producto)

        kw = dict()
        kw['nombre'] = "Aportacion Retrasada %s" % producto.valor()
        kw['descripcion'] = producto.descripcion
        kw['activo'] = producto.activo
        retrasada = model.Producto(**kw)
        retrasada.flush()

        kw = dict()
        kw['producto'] = retrasada
        for detalle in producto.detalles:
            kw['nombre'] = detalle.nombre
            kw['organizacion'] = detalle.organizacion
            kw['valor'] = detalle.valor
            nuevo = model.Detalle(**kw)
            nuevo.flush()

        flash("Se ha copiado el producto como retrasada")

        return self.default(retrasada.id)

    @error_handler(index)
    @expose()
    @validate(validators=dict(producto=validators.Int()))
    def adelantada(self, producto):

        """Copia un producto como una Aportacion Adelantada"""

        producto = model.Producto.get(producto)

        kw = dict()
        kw['nombre'] = "Aportacion Adelantada {0}".format(producto.valor())
        kw['descripcion'] = producto.descripcion
        kw['activo'] = producto.activo
        retrasada = model.Producto(**kw)
        retrasada.flush()

        kw = dict()
        kw['producto'] = retrasada
        for detalle in producto.detalles:
            kw['nombre'] = detalle.nombre
            kw['organizacion'] = detalle.organizacion
            kw['valor'] = detalle.valor
            nuevo = model.Detalle(**kw)
            nuevo.flush()

        flash("Se ha copiado el producto como Adelantada")

        return self.default(retrasada.id)
