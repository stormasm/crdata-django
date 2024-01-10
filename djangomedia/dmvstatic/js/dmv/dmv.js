/**
 * @namespace dmv
 * Global dmv namespace to encapsulate all other dmv related namespaces and classes
 */

var dmv;
if(!dmv) {
	 dmv = {};
}else if (typeof dmv != "object") {
	throw new Error("dmv already exists and is not an object");
}

dmv = {

	debug : function (msg) {
		if (typeof console != "undefined")
		{
			console.log(msg);
		}
	},	
}
