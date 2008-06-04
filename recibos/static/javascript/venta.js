// Copyright 2008 © Carlos Flores <cafg10@gmail.com>
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

var Venta = {
	agregando : function()
	{
		$('#cantidad').change(function()
		{
			$('#valor').text($('#unitario').val() * $('#cantidad').val());
		});
		$('#unitario').change(function()
		{
			$('#valor').text($('#unitario').val() * $('#cantidad').val());
		});
	},
	eliminar : function(url)
	{
		$("<div>Esta seguro de querer eliminar la venta</div>").dialog({
			title : 'Eliminar Venta',
			modal : true,
			buttons : {
				'Si' : function() { $(this).dialog('close'); window.location.href = url; },
				'No' : function() { $(this).dialog('close'); }
			}
		});
	}
}
