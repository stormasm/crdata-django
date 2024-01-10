/**
 * @namespace dmv.radiobutton
 * Contains functions relating to building groups of radio buttons
 */
 
dmv.radiobutton;
if(!dmv.radiobutton) {
	 dmv.radiobutton = {};
}else if (typeof dmv.radiobutton != "object") {
	throw new Error("dmv.radiobutton already exists and is not an object");
}

dmv.radiobutton = {
	
		generate:  function(id,iderror,numberofbuttons) { 
			this.setNumberOfComponents(numberofbuttons);
			generatedtext = this.generateRadioButtons(this.getNumberOfComponents());
			$(id).empty();
			$(id).append(generatedtext);

			// Event delegation will always start at the topdelegate node
			
			$('#toplsr').bind("click", function (event) {
				var target = $(event.target).parent();
				if (target.hasClass('test09')) {				
					dmv.radiobutton.process(id,iderror);
				}
				else {
					event.stopImmediatePropagation();
//					dmv.debug(target);
//					dmv.debug("miss");	
				}
			});
		},

		process:function(id,iderror){
           			group1value = $("input[name='group1']:checked").val();
				group2value = $("input[name='group2']:checked").val();
				dmv.radiobutton.hideErrorMessage(iderror);
				if(group1value == group2value) {
					dmv.radiobutton.checkRedrawRadioButtons(id,iderror);
				}
		},
		
		checkRedrawRadioButtons: function(id,iderror) {		
				generateradiobutton = this.generateRadioButtons(this.getNumberOfComponents());
				$(id).empty();
				$(id).append(generateradiobutton);
				this.showErrorMessage(iderror);				
		},		
		
		getNumberOfComponents: function() {
			return componentNumber;
		},
		
		setNumberOfComponents: function(num) {
			componentNumber = num;
		},

		showErrorMessage: function(id) {		
			$(id).show();
		},
		
		hideErrorMessage: function(id) {		
			$(id).hide();
		},
		
		// pass in the number of components you want generated
		
		generateRadioButtons: function(numofcomponents) {

			var x = " ";		
			var buffer = [];
			
			// THIS IS GROUP ONE
			
			for (i = 1; i <= numofcomponents; i++) {
			
				if (i == 1) {
					var pstart = "<input type=\"radio\" checked "
				}
				else {
					var pstart = "<input type=\"radio\" "
				}
			
				var p00;
					p00 = "name=\"group1\" "

					var p01 = "value=\"" + i + "\">"
					var data = "Principal Component " + i;
					var pend = "</input> <br>"
					buffer[i] = pstart + p00 + p01 + data + pend;
					x = x + buffer[i]
			}

			x = x + "<hr>"
			
			// THIS IS GROUP TWO
			
			for (i = 1; i <= numofcomponents; i++) {

				if (i == 2) {
					var pstart = "<input type=\"radio\" checked "
				}
				else {
					var pstart = "<input type=\"radio\" "
				}
			
				var p00;
					p00 = "name=\"group2\" "

					var p01 = "value=\"" + i + "\">"
					var data = "Principal Component " + i;
					var pend = "</input> <br>"
					buffer[i] = pstart + p00 + p01 + data + pend;
					x = x + buffer[i]
			}
			return x;
		},
}

