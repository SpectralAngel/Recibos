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

class Usuario(controllers.Controller, identity.SecureResource):
	
	# Restringir el acceso a solo administradores
	require = identity.in_group("admin")
	
	@expose(template="recibo.templates.usuario.index")
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose(template="recibo.templates.usuario.usuario")
	@validate(validators=dict(usuario=validators.Int()))
	def default(self, usuario):
		
		usuario = model.User.get(usuario)
		
		return dict(usuario=usuario)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(usuario=validators.Int()))
	def mostrar(self, usuario):
		
		return self.default(usuario)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(usuario=validators.Int()))
	def eliminar(self, usuario):
		
		usuario = model.User.get(usuario)
		nombre = usuario.display_name
		usuario.delete()
		flash("Se ha eliminado el usuario %s" % nombre)
		
		return self.index()
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(user_name=validators.String(),
							user_email=validators.Email(),
							display_name=validators.String(),
							password=validators.String()))
	def agregar(self, **kw):
		
		usuario = model.User(**kw)
		usuario.flush()
		
		flash("Se ha agregado el usuario")
		
		return self.default(usuario.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int(),
							usuario=validators.Int()))
	def agregarGrupo(self, grupo, usuario):
		
		usuario = model.User.get(usuario)
		grupo = model.Group.get(grupo)
		
		usuario.groups.append(grupo)
		usuario.flush()
		
		flash("Se ha añadido el grupo %s al usuario" % grupo.display_name)
		
		return self.default(usuario.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int(),
							usuario=validators.Int()))
	def eliminarGrupo(self, grupo, usuario):
		
		usuario = model.User.get(usuario)
		grupo = model.Group.get(grupo)
		
		usuario.groups.remove(grupo)
		usuario.flush()
		
		flash("Se ha eliminado el grupo %s al usuario" % grupo.display_name)
		
		return self.default(usuario.id)
