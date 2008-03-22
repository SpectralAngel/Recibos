#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright © 2008 Carlos Flores <cafg10@gmail.com>
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

from turbogears	import controllers, identity, validators
from turbogears	import flash, redirect
from turbogears	import expose, validate, paginate
from cherrypy	import request, response
from recibos	import model

class Venta(controllers.Controller):
	
	@expose()
	def index(self):
		
		return dict()
	
	@expose()
	@validate(validators=dict(venta=validators.Int()))
	def default(self, venta):
		
		return dict(venta=model.Venta.get(venta))
	
	@expose()
	@validate(validators=dict(venta=validators.Int()))
	def eliminar(self, venta):
		
		eliminando = model.Venta.get(venta)
		eliminando.delete()
		
		return dict(venta=venta)
	
	@expose()
	@validate(validators=dict(recibo=validators.Int(),
				   producto=validators.Int()))
	def agregar(self, recibo, producto, **kw):
		
		recibo = model.Recibo.get(recibo)
		producto = model.Producto.get(producto)
		
		venta = model.Venta(**kw)
		
		recibo.ventas.add(venta)
		producto.ventas.add(venta)
		
		venta.flush()
		
		return self.default(venta.id)
