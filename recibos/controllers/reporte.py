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

class Reporte(controllers.Controller):
	
	'''Muestra reportes de ingresos por compañia, por dia o por producto'''
	
	@expose(template="recibos.templates.reportes.index")
	def index(self):
		
		return dict(organizaciones=model.Organizacion.query.all(),
				casas=model.Casa.query.all())
	
	@error_handler(index)
	@expose(template="recibos.templates.reportes.dia")
	@validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y')))
	def dia(self, dia):
		
		recibos = model.Recibo.query.filter_by(dia=dia).all()
		
		# filtrando las ventas por detalle de producto
		detalles = {}
		for recibo in recibos:
			
			for venta in recibo.ventas:
				
				for detalle in venta.producto.detalles:
					
					try:
						detalles[detalle] += detalle.valor
					except KeyError:
						detalles[detalle] = detalle.valor
		
		return dict(dia=dia)
	
	@error_handler(index)
	@expose(template="recibos.templates.reportes.dia")
	@validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y'),
							casa=validators.Int()))
	def diaCasa(self, dia, casa):
		
		casa = model.Casa.get(casa)
		recibos = model.Recibo.query.filter_by(dia=dia, casa=casa).all()
		
		# filtrando las ventas por detalle de producto
		detalles = {}
		for recibo in recibos:
			
			for venta in recibo.ventas:
				
				for detalle in venta.producto.detalles:
					
					try:
						detalles[detalle] += detalle.valor
					except KeyError:
						detalles[detalle] = detalle.valor
		
		return dict(detalles=detalles, dia=dia, casa=casa)
	
	@error_handler(index)
	@expose(template="recibos.templates.reportes.organizacion")
	@validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y'),
							casa=validators.Int(),
							organizacion=validators.Int()))
	def organizacion(self, dia, casa, organizacion):
		
		casa = model.Casa.get(casa)
		organizacion = model.Organizacion.get(organizacion)
		
		recibos = model.Recibo.query.filter_by(casa=casa, dia=dia).all()
		
		# filtrando las ventas por detalle de producto
		detalles = {}
		for recibo in recibos:
			
			for venta in recibo.ventas:
				
				for detalle in venta.producto.detalles:
					
					if detalle.organizacion == organizacion:
					
						try:
							detalles[detalle] += detalle.valor
						except KeyError:
							detalles[detalle] = detalle.valor
		
		return dict(detalles=detalles, dia=dia, organizacion=organizacion, casa=casa)
