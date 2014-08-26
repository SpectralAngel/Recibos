# -*- coding: utf8 -*-
#
# Copyright (c) 2010, 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears import (controllers, identity, validators, flash, redirect,
                        expose, validate)

from recibos import model


class Pago(controllers.Controller):
    require = identity.not_anonymous()

    @expose()
    @validate(validators=dict(cubiculo=validators.Int(),
                              dia=validators.DateConverter(
                                  month_style="dd/mm/yyyy"),
                              descripcion=validators.UnicodeString(),
                              retraso=validators.Int(),
                              alquiler=validators.Int(),
                              isv=validators.Int(),
                              mora=validators.Int(),
                              recibo=validators.Int()))
    def agregar(self, cubiculo, casa, alquiler, mora, recibo, retraso, isv,
                **kw):
        cubiculo = model.Cubiculo.get(cubiculo)
        alquiler = model.Producto.get(alquiler)
        recibo = model.Recibo.get(recibo)
        isv = model.Producto.get(isv)
        mora = model.Producto.get(mora)

        kw['inquilino'] = cubiculo.inquilino
        kw['mora'] = cubiculo.calcularInteres(retraso)
        kw['impuesto'] = cubiculo.impuesto()
        kw['monto'] = cubiculo.precio

        vkw = dict()
        # Monto por el mes
        vkw['unitario'] = cubiculo.precio
        vkw['descripcion'] = kw['descripcion']
        vkw['cantidad'] = 1
        venta = model.Venta(**vkw)
        venta.recibo = recibo
        venta.producto = alquiler
        venta.flush()

        # Impuesto sobre la venta
        vkw['unitario'] = cubiculo.impuesto()
        vkw['descripcion'] = u'Impuesto sobre la venta'
        vkw['cantidad'] = 1
        venta = model.Venta(**vkw)
        venta.recibo = recibo
        venta.producto = isv
        venta.flush()

        # intereses moratorios
        if retraso > 0:
            vkw['unitario'] = cubiculo.calcularInteres(1)
            vkw['descripcion'] = u'Intereses Moratorios {0} meses'.format(
                retraso)
            vkw['cantidad'] = retraso
            venta = model.Venta(**vkw)
            venta.recibo = recibo
            venta.producto = mora
            venta.flush()

        pago = model.Alquiler(**kw)
        pago.cubiculo = cubiculo
        pago.recibo = recibo
        pago.flush()

        flash(u'Se ha registrado el pago del Local {0} en el recibo {1}'.format(
            cubiculo.nombre, recibo.id))

        raise redirect('/cubiculo/{0}'.format(cubiculo.id))

    @expose()
    @validate(validators=dict(pago=validators.Int()))
    def eliminar(self, pago):
        pago = model.Alquiler.get(pago)
        cubiculo = pago.cubiculo
        pago.delete()

        flash('Agregado el pago al cubiculo')

        raise redirect('/cubiculo/{0}'.format(cubiculo.id))


class Cubiculo(controllers.Controller):
    require = identity.not_anonymous()
    pago = Pago()

    @expose(template='recibos.templates.cubiculo.index')
    def index(self):

        return dict(cubiculos=model.Cubiculo.query.all())

    @validate(validators=dict(cubiculo=validators.Int()))
    def mostrar(self, cubiculo):

        raise redirect('/cubiculo/{0}'.format(cubiculo))

    @expose(template='recibos.templates.cubiculo.cubiculo')
    @validate(validators=dict(cubiculo=validators.Int()))
    def default(self, cubiculo):

        return dict(cubiculo=model.Cubiculo.get(cubiculo))

    @expose()
    @validate(validators=dict(nombre=validators.UnicodeString(),
                              inquilino=validators.UnicodeString(),
                              precio=validators.UnicodeString(),
                              enee=validators.UnicodeString()))
    def guardar(self, precio, **kw):

        kw['precio'] = Decimal(precio.replace(',', ''))
        if 'id' in kw:
            cubiculo = model.Cubiculo.get(kw['id'])
            del kw['id']
            for key in kw:
                setattr(cubiculo, key, kw[key])
            cubiculo.flush()
        else:
            cubiculo = model.Cubiculo(**kw)
            cubiculo.flush()

        raise redirect('/cubiculo/{0}'.format(cubiculo.id))
