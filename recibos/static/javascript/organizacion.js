// Copyright 2008 � Carlos Flores <cafg10@gmail.com>
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

var Organizacion = {
  url : '/',
	todas : function()
	{
		$.getJSON(this.url + 'organizacion/todos?tg_format=json', function(data)
		{
			$.each(data.organizaciones, function(i, organizacion)
			{
				var option = $('<option/>');
				option.val(organizacion.id);
				option.text(organizacion.nombre);
				$('.organizaciones').append(option);
			});
		});
	},
	lista : function()
	{
		$.getJSON(this.url + 'organizacion/todos?tg_format=json', function(data)
		{
			$.each(data.organizaciones, function(i, organizacion)
			{
				var li = $('<li/>');
				var a = $('<a/>');
				a.attr('href', this.url + 'organizacion/' + organizacion.id);
				a.text(organizacion.nombre);
				li.append(a);
				$('.listaOrganizaciones').append(li);
			});
		});
	}
}