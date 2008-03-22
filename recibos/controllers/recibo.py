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
from venta		import Venta

class Recibo(controllers.Controller):
	
	venta = Venta()
	
	@expose(template="recibos.templates.recibo.index")
	def index(self):
		
		return dict(casas=model.Casa.query.all())
	
	@expose(template="recibos.templates.recibo.recibo")
	@validate(validators=dict(recibo=validators.Int()))
	def default(self, recibo):
		
		return dict(recibo=model.Recibo.get(recibo))
	
	@expose(template="recibos.templates.recibo.impresion")
	@validate(validators=dict(recibo=validators.Int()))
	def impresion(self, recibo):
		
		recibo=model.Recibo.get(recibo)
		
		if not recibo.impreso:
			recibo.impreso = True
		else:
			flash('El recibo ya ha sido impreso')
		
		recibo.flush()
		return dict(recibo=recibo)
	
	@expose()
	@validate(validators=dict(recibo=validators.Int()))
	def eliminar(self, recibo):
		
		eliminando = model.recibo.gett(recibo)
		eliminando.delete()
		
		flash('El recibo ha sido eliminado')
		
		return self.index()
	
	@expose()
	@validate(validators=dict(casa=validators.Int()))
	def agregar(self, dia, casa, **kw):
		
		if kw['afiliado'] == '':
			
			del kw['afiliado']
		else:
			afiliado = model.Afiliado.get(int(kw['afiliado']))
			kw['cliente'] = afiliado.nombre + ' ' + afiliado.apellido
		
		from datetime import datetime
		recibo = model.Recibo(**kw)
		recibo.dia = datetime.strptime(dia, '%d/%m/%Y').date()
		recibo.flush()
		
		casa = model.Casa.get(casa)
		recibo.casa = casa
		
		return self.default(recibo.id)
