#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright (c) 2010 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, identity, validators, url
from turbogears import flash, redirect
from turbogears import expose, validate
from decimal import Decimal
from recibos import model
from datetime import date

class Pago(controllers.Controller):
    
    require = identity.not_anonymous()
    
    @expose()
    @validate(validators=dict(cubiculo=validators.Int(),
                              descripcion=validators.UnicodeString(),
                              inquilino=validators.UnicodeString(),
                              isv=validators.Int(),
                              retraso=validators.Int(),
                              casa=validators.Int(),
                              alquiler=validators.Int(),
                              intereses=validators.Int()))
    def agregar(self, cubiculo, recibo, intereses, isv, alquiler, casa, retraso, **kw):
        
        # Obteniendo la información necesaria desde la base de datos
        cubiculo = model.Cubiculo.get(cubiculo)
        intereses = model.Producto.get(intereses)
        isv = model.Producto.get(isv)
        alquiler = model.Producto.get(alquiler)
        casa = model.Casa.get(casa)
        
        kw['mora'] = cubiculo.calcularInteres(retraso)
        kw['impuesto'] = cubiculo.impuesto()
        kw['monto'] = cubiculo.precio
        
        # Crear el recibo
        rkw = dict()
        rkw['cliente'] = kw['inquilino']
        rkw['dia'] = kw['dia'] = date.today()
        
        recibo = model.Recibo(**rkw)
        recibo.casa = casa
        recibo.flush()
        
        # Crear las ventas necesarias en el recibo
        vkw = dict()
        # Monto por el mes
        vkw['descripcion'] = kw['descipcion']
        vkw['unitario'] = cubiculo.precio
        vkw['cantidad'] = 1
        venta = model.Venta(**kw)
        venta.recibo = recibo
        venta.producto = alquiler
        venta.flush()
        
        # Impuesto sobre la venta
        vkw['descripcion'] = ""
        vkw['unitario'] = cubiculo.impuesto()
        vkw['cantidad'] = 1
        venta = model.Venta(**kw)
        venta.recibo = recibo
        venta.producto = isv
        venta.flush()
        
        # intereses moratorios
        if kw['mora'] > 0:
            vkw['descripcion'] = ""
            vkw['unitario'] = kw['mora']
            vkw['cantidad'] = 1
            venta = model.Venta(**kw)
            venta.recibo = recibo
            venta.producto = intereses
            venta.flush()
        
        # Registrar el pago del alquiler en el cubiculo
        pago = model.Alquiler(**kw)
        pago.cubiculo = cubiculo
        pago.recibo = recibo
        pago.flush()
        
        flash('Pago de alquiler el recibo %s se ha creado automaticamente' % recibo.id)
        
        raise redirect(url('/cubiculo/%s' % cubiculo.id))
    
    @expose()
    @validate(validators=dict(pago=validators.Int()))
    def eliminar(self, pago):
        
        pago = model.Alquiler.get(pago)
        cubiculo = pago.cubiculo
        pago.delete()
        
        flash('Agregado el pago al cubiculo')
        
        raise redirect('/cubiculo/%s' % cubiculo.id)

class Cubiculo(controllers.Controller):
    
    require = identity.not_anonymous()
    pago = Pago()
    
    @expose(template='recibos.templates.cubiculo.index')
    def index(self):
        
        return dict(cubiculos=model.Cubiculo.query.all())
    
    @expose(template='recibos.templates.cubiculo.cubiculo')
    @validate(validators=dict(cubiculo=validators.Int()))
    def default(self, cubiculo):
        
        return dict(cubiculo=model.Cubiculo.get(cubiculo))
    
    @expose()
    @validate(validators=dict(cubiculo=validators.Int()))
    def mostrar(self, cubiculo):
       
        raise redirect(url('/cubiculo/%s' % cubiculo))
    
    @expose()
    @validate(validators=dict(nombre=validators.UnicodeString(),
                              inquilino=validators.UnicodeString(),
                              precio=validators.String()))
    def guardar(self, precio, **kw):
        
        kw['precio'] = Decimal(precio)
        cubiculo = model.Cubiculo(**kw)
        cubiculo.flush()
        
        raise redirect(url('/cubiculo/%s' % cubiculo.id))
