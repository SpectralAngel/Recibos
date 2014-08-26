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

from decimal import Decimal

from turbogears import controllers, validators, redirect, expose, validate

from recibos import model


class Venta(controllers.Controller):
    @expose()
    def index(self, tg_errors=None):
        if tg_errors:
            tg_errors = [(param, inv.msg, inv.value) for param, inv in
                         tg_errors.items()]

        return dict(tg_errors=tg_errors)

    @expose()
    @validate(validators=dict(venta=validators.Int()))
    def default(self, venta):
        return dict(venta=model.Venta.get(venta))

    @expose()
    @validate(validators=dict(venta=validators.Int()))
    def eliminar(self, venta):
        eliminando = model.Venta.get(venta)
        recibo = eliminando.recibo
        eliminando.delete()

        raise redirect('/recibo/{0}'.format(recibo.id))

    @expose()
    @validate(validators=dict(recibo=validators.Int(),
                              producto=validators.Int(),
                              unitario=validators.String(),
                              descripcion=validators.String(),
                              cantidad=validators.Int()))
    def agregar(self, recibo, producto, **kw):
        kw['unitario'] = Decimal(kw['unitario'])
        venta = model.Venta(**kw)

        venta.producto = model.Producto.get(producto)
        venta.recibo = model.Recibo.get(recibo)

        venta.flush()

        raise redirect('/recibo/{0}'.format(venta.recibo.id))
