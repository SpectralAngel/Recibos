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

from datetime	import datetime, date
from elixir		import Entity, Field, OneToMany, ManyToOne, ManyToMany
from elixir		import options_defaults, using_options, setup_all
from elixir		import Integer, Boolean, Numeric
from elixir		import String, Unicode, Text
from elixir		import DateTime, Date
from turbogears	import identity
from decimal import Decimal

Currency = Numeric

options_defaults['autosetup'] = False

class Casa(Entity):
	
	"""Sucursal del COPEMH
	
	Representa un lugar físico donde se encuentra una sede del COPEMH.
	"""
	
	using_options(tablename='casa')
	
	nombre = Field(Unicode(20), required=True)
	direccion = Field(Unicode(100))
	telefono = Field(Unicode(11))
	recibos = OneToMany("Recibo", order_by='dia')
	activa = Field(Boolean, default=True)

class Afiliado(Entity):
	
	"""Datos sobre un miembro
	
	Contiene los datos básicos sobre un miembro del COPEMH. Estos datos son en
	realidad parte de otra aplicación y no deben ser modificados por el gestor
	de recibos."""
	
	using_options(tablename='affiliate')
	
	nombre = Field(Unicode(50), colname='first_name')
	apellidos = Field(Unicode(50), colname='last_name')
	
	cotizacion = Field(String(20), colname='payment')

class Recibo(Entity):
	
	"""Recibo extendido a un cliente
	
	Contiene los datos sobre  un recibo que haya sido extendido a un cliente,
	ya sea este afiliado o no.
	"""
	
	using_options(tablename='recibo')
	
	casa = ManyToOne("Casa")
	afiliado = Field(Integer(6))
	cliente = Field(Unicode(100), required=True)
	dia = Field(Date, required=True, default=date.today)
	# Marca si el recibo ya ha sido impreso
	impreso = Field(Boolean, default=False)
	ventas = OneToMany("Venta")
	alquileres = OneToMany('Alquiler')
	
	def total(self):
		
		"""Retorna el total de las ventas de un recibo"""
		
		return sum(venta.valor() for venta in self.ventas)

class Venta(Entity):
	
	"""Descripción de Venta
	
	Contiene los datos sobre la venta de determinado producto en un recibo."""
	
	using_options(tablename='venta')
	
	recibo = ManyToOne("Recibo")
	producto = ManyToOne("Producto")
	descripcion = Field(Unicode(200))
	cantidad = Field(Integer(3), required=True)
	# No siempre el precio unitario esta determinado por el precio nominal de un
	# producto, este puede cambiar como en el caso de los préstamos
	unitario = Field(Currency, required=True)
	
	def valor(self):
		
		"""Retorna el total de una venta"""
		
		return self.cantidad * self.unitario

class Organizacion(Entity):
	
	"""Beneficiario de las Ventas
	
	Contiene la información sobre las estructuras organizacionales que se
	benefician en la venta de determinados productos.
	"""
	
	using_options(tablename='organizacion')
	
	nombre = Field(Unicode(50), required=True)
	detalles = OneToMany("Detalle")

class Producto(Entity):
	
	'''Servicios u Objetos a la venta
	
	Guarda los datos de productos que se tienen a la disposición de los
	afiliados.'''
	
	using_options(tablename='producto')
	
	nombre = Field(Unicode(100), required=True)
	descripcion = Field(Text)
	detalles = OneToMany("Detalle")
	# Marca si el producto se encuentra disponible para ser facturado
	activo = Field(Boolean, default=True)
	
	def valor(self):
		
		"""Retorna el precio real de un producto"""
		
		return sum(detalle.valor for detalle in self.detalles)

class Detalle(Entity):
	
	"""
	Expresa a que organización debe adjudicarse parte del valor de la venta de
	un producto."""
	
	using_options(tablename='detalle_producto')
	
	producto = ManyToOne("Producto")
	organizacion = ManyToOne("Organizacion")
	nombre = Field(Unicode(100))
	valor = Field(Currency, required=True)

class Cubiculo(Entity):
	
	using_options(tablename='cubiculo')
	
	nombre = Field(Unicode(255))
	inquilino = Field(Unicode(255))
	precio = Field(Currency, required=True)
	alquileres = OneToMany('Alquiler')
	enee = Field(Unicode(100), required=True)
	intereses = Field(Numeric, required=True, default=Decimal("0.02"))
	
	def impuesto(self):
		
		return self.precio * Decimal('0.12')
	
	def interesMoratorio(self):
		
		return self.intereses
	
	def calcularInteres(self, meses):
		
		return self.intereses * self.precio * meses / Decimal('100') 

class Alquiler(Entity):
	
	using_options(tablename='alquiler')
	
	cubiculo = ManyToOne('Cubiculo')
	dia = Field(Date, required=True)
	descripcion = Field(Unicode(255))
	inquilino = Field(Unicode(100))
	recibo = ManyToOne('Recibo')
	monto = Field(Currency, required=True)
	mora = Field(Currency, default=0)
	impuesto = Field(Currency, default=0)

# the identity model

class Visit(Entity):
	"""
	A visit to your site
	"""
	using_options(tablename='visit')

	visit_key = Field(String(40), primary_key=True)
	created = Field(DateTime, nullable=False, default=datetime.now)
	expiry = Field(DateTime)

	@classmethod
	def lookup_visit(cls, visit_key):
		return Visit.get(visit_key)

class VisitIdentity(Entity):
	"""
	A Visit that is link to a User object
	"""
	using_options(tablename='visit_identity')

	visit_key = Field(String(40), primary_key=True)
	user = ManyToOne('User', colname='user_id', use_alter=True)

class Group(Entity):
	"""
	An ultra-simple group definition.
	"""
	using_options(tablename='tg_group')

	group_id = Field(Integer, primary_key=True)
	group_name = Field(Unicode(16), unique=True)
	display_name = Field(Unicode(255))
	created = Field(DateTime, default=datetime.now)
	users = ManyToMany('User', tablename='user_group')
	permissions = ManyToMany('Permission', tablename='group_permission')

class User(Entity):
	"""
	Reasonably basic User definition.
	Probably would want additional attributes.
	"""
	using_options(tablename='tg_user')

	user_id = Field(Integer, primary_key=True,colname="id")
	user_name = Field(Unicode(16), unique=True)
	email_address = Field(Unicode(255), unique=True)
	display_name = Field(Unicode(255))
	password = Field(Unicode(40))
	created = Field(DateTime, default=datetime.now)
	groups = ManyToMany('Group', tablename='user_group')

	@property
	def permissions(self):
		perms = set()
		for g in self.groups:
			perms |= set(g.permissions)
		return perms

class Permission(Entity):
	"""
	A relationship that determines what each Group can do
	"""
	using_options(tablename='permission')

	permission_id = Field(Integer, primary_key=True)
	permission_name = Field(Unicode(16), unique=True)
	description = Field(Unicode(255))
	groups = ManyToMany('Group', tablename='group_permission')

# Set up all Elixir entities declared above

setup_all()
