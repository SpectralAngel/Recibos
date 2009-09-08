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
from recibos	import model
from cherrypy	import request, response
from decimal	import *

class Detalle(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	@expose()
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(detalle=validators.Int()))
	def default(self, detalle):
		
		'''Permite mostrar un detalle en el cliente'''
		
		return dict(detalle=model.Detalle.get(detalle))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(detalle=validators.Int()))
	def mostrar(self, detalle):
		
		'''
		Permite utilizar un formulario para mostrar un detalle en el cliente
		'''
		
		return self.default(detalle)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(detalle=validators.Int()))
	def eliminar(self, detalle):
		
		'''Elimina un detalle de la base de datos'''
		
		eliminando = model.Detalle.get(detalle)
		producto = eliminando.producto
		eliminando.delete()
		
		raise redirect("/producto/%s" % producto.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(producto=validators.Int(),
							organizacion=validators.Int(),
							nombre=validators.String(),
							valor=validators.String()))
	def agregar(self, producto, organizacion, **kw):
		
		'''Agrega un nuevo detalle al producto y la organización especificada'''
		
		producto = model.Producto.get(producto)
		organizacion = model.Organizacion.get(organizacion)
		
		kw['valor'] = Decimal(kw['valor'])
		detalle = model.Detalle(**kw)
		
		detalle.producto = producto
		detalle.organizacion = organizacion
		detalle.flush()
		
		raise redirect("/producto/%s" % producto.id)

