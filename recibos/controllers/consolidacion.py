# -*- coding: utf8 -*-
#
# consolidacion.py
# Copyright (c) 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, validators, redirect, expose, validate, identity
from recibos    import model
from decimal    import Decimal

class Consolidacion(controllers.Controller, identity.SecureResource):
    
    """Registra ingresos de cheques de consolidación"""
    
    require = identity.not_anonymous()
    
    @expose(template="recibos.templates.consolidacion.index")
    def index(self, tg_errors=None, tg_exceptions=None):
        
        return dict(tg_errors=tg_errors, exception=tg_exceptions)
    
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              recibo=validators.Int(),
                              dia=validators.DateConverter(month_style="dd/mm/yyyy"),
                              organizacion=validators.UnicodeString(),
                              monto=validators.UnicodeString(),
                              cheque=validators.UnicodeString()))
    def guardar(self, afiliado, recibo, **kw):
        
        kw["monto"] = Decimal(kw["monto"].replace(',', ''))
        
        consolidacion = model.Consolidacion(**kw)
        consolidacion.afiliado = model.Afiliado.get(afiliado)
        consolidacion.recibo = model.Recibo.get(recibo)
        
        raise redirect('/consolidacion')
    
    @expose(template="recibos.templates.consolidacion.index")
    
