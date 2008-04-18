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
from turbogears	import expose, validate, paginate, error_handler
from cherrypy	import request, response
from recibos	import model
from detalle	import Detalle

class Producto(controllers.Controller):
	
	detalle = Detalle()
	
	@expose(template="recibos.templates.producto.index")
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@expose(template="recibos.templates.producto.producto")
	@validate(validators=dict(producto=validators.Int()))
	def default(self, producto):
		
		'''Muestra una casa en el cliente'''
		
		producto = model.Producto.get(producto)
		
		return dict(producto=producto, valor=producto.valor())
	
	@expose()
	@validate(validators=dict(producto=validators.Int()))
	def mostrar(self, producto):
		
		'''
		Permite utilizar un formulario para mostrar una casa en el cliente
		'''
		
		return self.default(producto)
	
	@expose()
	def todos(self):
		
		'''Responde con un listado de todas las casas disponibles'''
		
		return dict(productos=model.Producto.query.all())
	
	@expose()
	@validate(validators=dict(nombre=validators.String(),
							descripcion=validators.String()))
	def agregar(self, **kw):
		
		'''Agrega un producto a la base de datos'''
		
		producto = model.Producto(**kw)
		producto.flush()
		
		return self.default(producto.id)
	
	@expose()
	@validate(validators=dict(producto=validators.Int()))
	def eliminar(self, producto):
		
		eliminando = model.Producto.get(producto)
		eliminando.delete()
		
		return self.index()
	
