/**
 * @namespace dmv.ajaxbuildcheckbox
 * Contains functions relating to building checkboxes based on data received from AJAX
 */
 
dmv.ajaxbuildcheckbox;
if(!dmv.ajaxbuildcheckbox) {
	 dmv.ajaxbuildcheckbox = {};
}else if (typeof dmv.ajaxbuildcheckbox != "object") {
	throw new Error("dmv.ajaxbuildcheckbox already exists and is not an object");
}

dmv.ajaxbuildcheckbox = {

	countProperties: function(obj) {
		var prop;
		var propCount = 0;
  
		for (prop in obj) {
		propCount++;
		}
		return propCount;
	},

	buildcheckboxnotables: function(data,row) {
	
		var x = " ";
		var y = " ";
		var buffer = [];
		
		var datalength = dmv.ajaxbuildcheckbox.countProperties(data);
		
		for (i = 0; i < datalength; i++) {
			var pstart = "<input type=\"checkbox\" checked=\"yes\" "
			
			var p00;
			if (row) {
				p00 = "name=row "
			}
			else {
				p00 = "name=column "
			}
			var p01 = "value=\"" + data[i] + "\">"
			var pend = "</input>"
			buffer[i] = pstart + p00 + p01 + data[i] + pend;
			x = x + buffer[i]
		}
		return x;
	},

	buildcheckbox: function(data,row) {
	
		var x = " ";
		var y = " ";
		var buffer = [];
		
		var datalength = dmv.ajaxbuildcheckbox.countProperties(data);
			var tstart = "<table>"
			var tend = "</table>"
		for (i = 0; i < datalength; i++) {
			var modvalue = i % 10;

			var rowstart = "<tr>"
			var pstart = "<td><input type=\"checkbox\" checked=\"yes\" "
			
			var p00;
			if (row) {
				p00 = "name=row "
			}
			else {
				p00 = "name=column "
			}
			var p01 = "value=\"" + data[i] + "\">"
			var pend = "</input></td>"
			var rowend = "</tr>"
			
			if ((modvalue == 0) && (i == 0)) {
			  buffer[i] = rowstart + pstart + p00 + p01 + data[i] + pend;
			}
			else if (modvalue == 0) {
			  buffer[i] = rowstart + pstart + p00 + p01 + data[i] + pend;
			}
			else {
         		  buffer[i] = pstart + p00 + p01 + data[i] + pend;
			}
			x = x + buffer[i]
		}
		x = tstart + x + rowend + tend;
		return x;
	},
	
	attachchangeventoselect: function() {
	
			$("select").change(function () {
			$("select option:selected").each(function () {
			var xfilename = $(this).text();
			
			$.post('ajaxgetrownamesfromfile', {'filename': xfilename},
				function(data){
					var row = true;
					var mynewdiv = dmv.ajaxbuildcheckbox.buildcheckbox(data,row);
					$("#rownames").empty();
					$("#rownames").append(mynewdiv);
					}, "json");

			$.post('ajaxgetcolumnnamesfromfile', {'filename': xfilename},
				function(data){
					var row = false;
					var mynewdiv = dmv.ajaxbuildcheckbox.buildcheckbox(data,row);
					$("#columnnames").empty();
					$("#columnnames").append(mynewdiv);
					}, "json");
					
			});			
		});
	},
	
	triggerselectevent: function(xfilename) {
			
		$.post('ajaxgetrownamesfromfile', {'filename': xfilename},
			function(data){
				var row = true;
				var mynewdiv = dmv.ajaxbuildcheckbox.buildcheckbox(data,row);
				$("#rownames").empty();
				$("#rownames").append(mynewdiv);
				}, "json");

		$.post('ajaxgetcolumnnamesfromfile', {'filename': xfilename},
			function(data){
				var row = false;
				var mynewdiv = dmv.ajaxbuildcheckbox.buildcheckbox(data,row);
				$("#columnnames").empty();
				$("#columnnames").append(mynewdiv);
				}, "json");
	},
}

