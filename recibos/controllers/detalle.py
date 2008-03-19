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

from turbogears	import controllers, identity
from turbogears	import flash, redirect
from turbogears	import expose, validators, paginate
from recibos	import model
from cherrypy	import request, response

class Detalle(controllers.Controller):
	
	@expose()
	def index(self):
		
		return dict()
	
	@expose()
	@validate(dict(detalle=validators.Int()))
	def default(self, detalle):
		
		return dict(detalle=model.Detalle.get(detalle))
	
	@expose()
	@validate(dict(detalle=validators.Int()))
	def mostrar(self, detalle):
		
		return self.default(detalle)
	
	@expose()
	@validate(dict(detalle=validators.Int()))
	def eliminar(self, detalle):
		
		eliminando = model.Detalle.get(detalle)
		eliminando.delete()
		
		return dict(detalle=detalle)
	
	@expose()
	@validate(dict(producto=validators.Int(), organizacion=validators.Int()))
	def agregar(self, producto, organizacion, **kw):
		
		producto = model.Producto.get(producto)
		organizacion = model.Organizacion.get(organizacion)
		
		detalle = model.Detalle(**kw)
		
		producto.detalles.add(detalle)
		organizacion.detalles.add(detalle)
		detalle.flush()
		
		return self.default(detalle.id)
