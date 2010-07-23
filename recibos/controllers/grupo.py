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

class Grupo(controllers.Controller, identity.SecureResource):
	
	# Restringir el acceso a solo administradores
	require = identity.in_group("admin")
	
	@expose(template="recibo.templates.grupo.index")
	def index(self, tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose(template="recibo.templates.grupo.grupo")
	@validate(validators=dict(grupo=validators.Int()))
	def default(self, grupo):
		
		return dict(grupo=model.Group.get(grupo))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int()))
	def mostrar(self, grupo):
		
		return self.default(grupo)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(group_name=validators.String(),
							display_name=validators.String()))
	def agregar(self, **kw):
		
		grupo = model.Group(**kw)
		grupo.flush()
		
		flash("Se ha agregado el grupo %s" % grupo.display_name)
		
		return self.default(grupo.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int()))
	def eliminar(self, grupo):
		
		grupo = model.Group.get(grupo)
		nombre = grupo.display_name
		grupo.delete()
		
		flash("Se ha eliminado el grupo %s" % nombre)
		
		return self.index()
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int(),
							usuario=validators.Int()))
	def agregarUsuario(self, grupo, usuario):
		
		usuario = model.User.get(usuario)
		grupo = model.Group.get(grupo)
		
		usuario.groups.append(grupo)
		usuario.flush()
		
		flash("Se ha añadido el usuario %s al grupo" % usuario.display_name)
		
		return self.default(grupo.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(grupo=validators.Int(),
							usuario=validators.Int()))
	def eliminarUsuario(self, grupo, usuario):
		
		usuario = model.User.get(usuario)
		grupo = model.Group.get(grupo)
		
		usuario.groups.remove(grupo)
		usuario.flush()
		
		flash("Se ha eliminado el usuario %s del grupo" % usuario.display_name)
		
		return self.default(grupo.id)

