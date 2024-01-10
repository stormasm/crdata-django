/**
 * @namespace dmv.selectallcheckbox
 * Contains functions relating to selecting all/none of the checkboxes
 */
 
dmv.selectallcheckbox;
if(!dmv.selectallcheckbox) {
	 dmv.selectallcheckbox = {};
}else if (typeof dmv.selectallcheckbox != "object") {
	throw new Error("dmv.selectallcheckbox already exists and is not an object");
}

dmv.selectallcheckbox = {

	selectallrows: function() {
			$("#allrows").click(function()				
			{
				var checked_status = this.checked;
				$("div input[name=row]").each(function()
				{
					this.checked = checked_status;
				});
			});
	},

	selectallcolumns: function() {
			$("#allcolumns").click(function()				
			{
				var checked_status = this.checked;
				$("div input[name=column]").each(function()
				{
					this.checked = checked_status;
				});
			});					
	},
}

