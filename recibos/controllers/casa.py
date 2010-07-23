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

from turbogears	import controllers, identity, flash, validators
from turbogears	import expose, validate, error_handler
from recibos	import model

class Casa(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	@expose(template="recibos.templates.casa.index")
	def index(self,  tg_errors=None, tg_exceptions=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose()
	#@expose(template="recibos.templates.casa.casa")
	@validate(validators=dict(casa=validators.Int()))
	def default(self, casa):
		
		'''Muestra un producto en el cliente'''
		
		return dict(casa=model.Casa.get(casa))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(casa=validators.Int()))
	def mostrar(self, casa):
		
		'''
		Permite utilizar un formulario para mostrar un producto en el cliente
		'''
		
		return self.default(casa)
	
	@expose(template="recibos.templates.casa.casas")
	def todos(self):
		
		'''Responde con un listado de todos los productos disponibles'''
		
		casas = model.Casa.query.all()
		
		return dict(casas=casas, cantidad=len(casas))
	
	@expose(template="recibos.templates.casa.casas")
	def activas(self):
		
		'''Muestra un listado de casas disponibles para hacer nuevos recibos'''
		
		return dict(casas=model.Casa.query.filter_by(activa=True).all())
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(nombre=validators.String(),
								descripcion=validators.String()))
	def agregar(self, **kw):
		
		'''Agrega un producto a la base de datos'''
		
		casa = model.Casa(**kw)
		casa.flush()
		
		return self.default(casa.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(casa=validators.Int()))
	def desactivar(self, casa):
		
		'''Permite desactivar una casa para evitar su uso en nuevos recibos'''
		
		casa = model.Casa.get(casa)
		casa.activa = False
		casa.flush()
		
		flash("La casa %s ha sido desactivada" % casa.nombre)
		return self.index()
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(casa=validators.Int()))
	def activar(self, casa):
		
		'''Permite activar una casa para usarla en nuevos recibos'''
		
		casa = model.Casa.get(casa)
		casa.activa = False
		casa.flush()
		
		flash("La casa %s ha sido Activada" % casa.nombre)
		return self.default(casa.id)

