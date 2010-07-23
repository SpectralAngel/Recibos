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
from turbogears	import expose, validate, error_handler
from recibos	import model
from venta		import Venta
from datetime	import date

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
		
		eliminando = model.Recibo.get(recibo)
		eliminando.delete()
		
		flash('El recibo ha sido eliminado')
		
		return self.index()
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(id=validators.Int(),
							afiliado=validators.Int(),
							casa=validators.Int(),
							dia=validators.DateConverter(month_style="dd/mm/yyyy"),
							cliente=validators.String()))
	def agregar(self, dia, casa, **kw):
		
		"""Agrega un nuevo recibo a la base de datos
		
		Es necesario especificar el numero de afiliacion.
		
		Se utiliza para corregir problemas con la numeracion de los recibos"""
		
		if kw['afiliado'] == '' or kw['afiliado'] == None:
			del kw['afiliado']
		else:
			afiliado = model.Afiliado.get(kw['afiliado'])
			kw['cliente'] = afiliado.nombre + ' ' + afiliado.apellidos
		
		recibo = model.Recibo.get(kw['id'])
		if recibo == None:
			
			recibo = model.Recibo(**kw)
		else:
			try:
				recibo.cliente = kw['cliente']
				recibo.afiliado = kw['afiliado']

			except:
				pass
		
		recibo.dia = dia
		recibo.flush()
		
		casa = model.Casa.get(casa)
		recibo.casa = casa
		
		return self.default(recibo.id)
	
	@expose()
	@validate(validators=dict(afiliado=validators.Int(), casa=validators.Int()))
	def nuevo(self, casa, afiliado):
		
		"""Agrega un nuevo recibo con solo especificar el numero de Afiliacion"""
		
		afiliado = model.Afiliado.get(afiliado)
		
		kw = dict()
		kw['cliente'] = afiliado.nombre + ' ' + afiliado.apellidos
		kw['afiliado'] = afiliado.id
		kw['dia'] = date.today()
		
		recibo = model.Recibo(**kw)
		recibo.flush()
		
		casa = model.Casa.get(casa)
		recibo.casa = casa
		
		raise redirect('/recibo/%s' % recibo.id)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.dia")
	@validate(validators=dict(dia=validators.DateConverter(month_style="dd/mm/yyyy")))
	def dia(self, dia):
		
		"""Muestra los recibos de un dia"""
		
		return dict(recibos=model.Recibo.query.filter_by(dia=dia).all(), dia=dia)
	
	@error_handler(index)
	@expose(template="recibos.templates.recibo.dia")
	@validate(validators=dict(dia=validators.DateConverter(month_style="dd/mm/yyyy"),
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
	
	@expose(template="recibos.templates.recibo.nombre")
	@validate(validators=dict(nombre=validators.String()))
	def nombre(self, nombre):
		
		"""Realiza una busqueda por nombre del cliente en los recibos"""
		
		return dict(recibos=model.Recibo.query.filter(model.Recibo.cliente.like("%" + nombre + "%")))
	
	@expose()
	@validate(validators=dict(recibo=validators.Int()))
	def anular(self, recibo):
		
		"""Anula un recibo en la base de Datos
		
		Especificamente coloca el afiliado como 0, el cliente en NULO y elimina
		cualquier venta realizada en el mismo"""
		
		recibo = model.Recibo.get(recibo)
		
		for venta in recibo.ventas:
			
			venta.delete()
		
		recibo.cliente = "Nulo"
		recibo.afiliado = None
		
		flash('Recibo %s Anulado' % recibo.id)
		
		raise redirect('/recibo')
	
	@expose()
	@validate(validators=dict(cliente=validators.String(), casa=validators.Int()))
	def cliente(self, casa, cliente):
		
		"""Agrega un recibo para una persona que no es afiliado"""
		
		kw = dict()
		kw['cliente'] = cliente
		kw['afiliado'] = 0
		kw['dia'] = date.today()
		
		recibo = model.Recibo(**kw)
		recibo.flush()
		
		casa = model.Casa.get(casa)
		recibo.casa = casa
		
		raise redirect('/recibo/%s' % recibo.id)
	
	@expose(template='recibos.template.recibo.nombreDetalle')
	@validate(validators=dict(dia=validators.DateConverter(month_style="dd/mm/yyyy"),
							nombre=validators.String()))
	def detalleNombre(self, dia, nombre):
		
		return dict(recibos=model.Recibo.query.filter(model.Recibo.cliente.like("%" + nombre + "%")).filter(dia=dia))
