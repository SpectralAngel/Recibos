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

class Organizacion(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	@expose(template="recibos.templates.organizacion.index")
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose(template="recibos.templates.organizacion.organizacion")
	@validate(validators=dict(organizacion=validators.Int()))
	def default(self, organizacion):
		
		'''Muestra una organizacion en el cliente'''
		
		return dict(organizacion=model.Organizacion.get(organizacion))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(organizacion=validators.Int()))
	def mostrar(self, organizacion):
		
		'''
		Permite utilizar un formulario para mostrar una organizacion en el cliente
		'''
		
		return self.default(organizacion)
	
	@error_handler(index)
	@paginate(var_name="organizaciones")
	@expose(template="recibos.templates.organizacion.organizaciones")
	def todos(self):
		
		'''Responde con un listado de todos los productos disponibles'''
		
		return dict(organizaciones=model.Organizacion.query.all())
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(nombre=validators.String()))
	def agregar(self, nombre):
		
		'''Agrega una organizacion a la base de datos'''
		
		organizacion = model.Organizacion(nombre=nombre)
		organizacion.flush()
		print organizacion.id
		
		raise redirect('/organizacion/%s' % organizacion.id)

