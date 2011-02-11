// Copyright 2008 - 2011 (c) Carlos Flores <cafg10@gmail.com>
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

var Recibo = {
  url : '/',
	sinImprimir : function()
	{
		$('#imprimir').change(function()
		{
			var casa = $('#imprimir option:selected').val();
			$.getJSON(this.url + 'recibo/porImprimir/' + casa, function(data)
			{
				$('.recibosSinImprimir').empty();
				$.each(data.recibos, function(i, recibo)
				{
					var a = $('<a/>');
					a.attr('href', this.url + 'recibo/' + recibo.id);
					a.text(recibo.id + ' ' + recibo.cliente);
					var li = $('<li/>');
					li.append(a);
					$('.recibosSinImprimir').append(li);
				});
			});
		});
	}
}

