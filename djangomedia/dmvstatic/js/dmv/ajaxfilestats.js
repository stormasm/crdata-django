/**
 * @namespace dmv.ajaxfilestats
 * Contains functions relating to building checkboxes based on data received from AJAX
 */
 
dmv.ajaxfilestats;
if(!dmv.ajaxfilestats) {
	 dmv.ajaxfilestats = {};
}else if (typeof dmv.ajaxfilestats != "object") {
	throw new Error("dmv.ajaxfilestats already exists and is not an object");
}

dmv.ajaxfilestats = {

	attachchangeventoselect: function(id,iderror) {

			var twoFiles = new Array(2);
		
			$("select").change(function () {
			$("select option:selected").each(function (i) {
				var xfilename = $(this).text();			
				twoFiles[i]= xfilename;
			});

			$.post('ajaxgetnumberofcolumnsfromfile', {'filename1': twoFiles[0],'filename2':twoFiles[1]},
				function(data){
					numofcolumns = data['check'];
					dmv.radiobutton.generate(id,iderror,numofcolumns);
				}, "json");
		});
	},
}

