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
from venta		import Venta

class Recibo(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	venta = Venta()
	
	@expose(template="recibos.templates.recibo.index")
	def index(self, tg_errors=None, tg_exceptions=None):
		
		return dict(tg_errors=tg_errors, exception=tg_exceptions)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.recibo")
	@validate(validators=dict(recibo=validators.Int()))
	def default(self, recibo):
		
		"""Muestra un recibo junto con su interfaz para agregar ventas"""
		
		return dict(recibo=model.Recibo.get(recibo),
					productos=model.Producto.query.filter_by(activo=True).all())
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(recibo=validators.Int()))
	def mostrar(self, recibo):
		
		"""Permite utilizar un formulario para mostrar un recibo en el cliente"""
		
		return self.default(recibo)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.impresion")
	@validate(validators=dict(recibo=validators.Int()))
	def impresion(self, recibo):
		
		'''Muestra la plantilla de impresion de recibos'''
		
		recibo=model.Recibo.get(recibo)
		
		if not recibo.impreso:
			recibo.impreso = True
			recibo.flush()
		else:
			flash('El recibo ya ha sido impreso')
		
		return dict(recibo=recibo)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(recibo=validators.Int()))
	def eliminar(self, recibo):
		
		'''Elimina un recibo de la base de datos'''
		
		eliminando = model.recibo.get(recibo)
		eliminando.delete()
		
		flash('El recibo ha sido eliminado')
		
		return self.index()
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(id=validators.Int(),
							afiliado=validators.Int(),
							casa=validators.Int(),
							dia=validators.DateTimeConverter(format='%d/%m/%Y'),
							cliente=validators.String()))
	def agregar(self, dia, casa, **kw):
		
		'''Agrega un nuevo recibo a la base de datos'''
		
		if kw['afiliado'] == '': del kw['afiliado']
		else:
			afiliado = model.Afiliado.get(kw['afiliado'])
			kw['cliente'] = afiliado.nombre + ' ' + afiliado.apellidos
		
		from datetime import datetime
		recibo = model.Recibo(**kw)
		recibo.dia = dia
		recibo.flush()
		
		casa = model.Casa.get(casa)
		recibo.casa = casa
		
		return self.default(recibo.id)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.dia")
	@validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y')))
	def dia(self, dia):
		
		"""Muestra los recibos de un dia"""
		
		return dict(recibos=model.Recibo.query.filter_by(dia=dia).all(), dia=dia)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.dia")
	@validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y'),
							casa=validators.Int()))
	def diaCasa(self, dia, casa):
		
		"""Muestra los recibos de un dia en una casa"""
		
		casa = model.Casa.get(casa)
		recibos = model.Recibo.query.filter_by(dia=dia, casa=casa).all()
		
		return dict(recibos=recibos, dia=dia, casa=casa)
	
	@expose()
	@validate(validators=dict(casa=validators.Int()))
	def porImprimir(self, casa):
		
		"""Muestra los recibos que aun no se han impreso"""
		
		casa = model.Casa.get(casa)
		return dict(recibos=model.Recibo.query.filter_by(impreso=False, casa=casa).all())

