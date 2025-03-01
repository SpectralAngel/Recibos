# -*- coding: utf8 -*-
#
# Copyright (c) 2008 - 2012 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, expose, url, identity, redirect
from cherrypy import request, response

from recibos.controllers import (producto, recibo, casa, organizacion, reporte,
                                 alquiler)

# from recibos import json
# import logging
# log = logging.getLogger("recibos.controllers")


class Root(controllers.RootController):
    recibo = recibo.Recibo()
    producto = producto.Producto()
    organizacion = organizacion.Organizacion()
    casa = casa.Casa()
    reporte = reporte.Reporte()
    cubiculo = alquiler.Cubiculo()

    @identity.require(identity.not_anonymous())
    @expose(template="recibos.templates.welcome")
    def index(self, tg_errors=None):

        if tg_errors:
            tg_errors = [(param, inv.msg, inv.value) for param, inv in
                         tg_errors.items()]

        return dict(tg_errors=tg_errors)

    @expose(template="recibos.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
                and identity.was_login_attempted() \
                and not identity.get_identity_errors():
            if not forward_url:
                forward_url = url('/')
            raise redirect(forward_url)

        forward_url = None
        previous_url = url(request.path_info)

        if identity.was_login_attempted():
            msg = _("The credentials you supplied were not correct or "
                    "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _("You must provide your credentials before accessing "
                    "this resource.")
        else:
            msg = _("Please log in.")
            forward_url = request.headers.get("Referer", "/")

        response.status = 403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
