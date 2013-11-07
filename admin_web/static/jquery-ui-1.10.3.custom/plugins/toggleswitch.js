// Copyright (c) 2011 Matt Whipple

// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:

// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


(function($, undefined) {

    $.widget("ui.toggleswitch", {
	version: "0.1",
	options: {
	    labels: new Array("No", "Yes")
	},
	_create: function() {
	    this.element
		.addClass( "ui-toggleswitch ui-widget ui-widget-header ui-corner-all")
		.attr({
		    role: "toggleswitch"
		});
		this._switch = $("<div class='ui-toggleswitch-child ui-toggleswitch-switch'>");
		control = this;
	    var oldInput = this.element.find("input")
	      .after(
	        $("<div class='ui-toggleswitch-child ui-toggleswitch-state ui-toggleswitch-off'>")
	          .html(this.options.labels[0])
	          .click(function(event) { control._toggleValue(event, true) }))
          .after(this._switch)
	      .after(
	        $("<div class='ui-toggleswitch-child ui-toggleswitch-state ui-toggleswitch-on'>")
	          .html(this.options.labels[1])
	          .click(function(event) { control._toggleValue(event, false)}))
	      .hide();

	},

	_destroy: function() {
	    this.element.removeClass( "ui-slidetoggle ui-widget ui-corner-all");
	    this.element.find(".ui-toggleswitch-child").remove();
	},
	value: function(newValue) {
	    if (newValue == undefined) {
		  return this._value();
	    }
	    this._setOption("value", newValue);
	    this.element.find("input").val(newValue);
	    return this;
	},

	_value: function() {
	    var val = this.options.value;
	    if ( typeof val !== "boolean") {
		value = false;
	    }
	    return val;
	},
    _toggleValue: function(event, value) {
      this.value(value);
      this._toggleSwitch(event);
    },
	_toggleSwitch: function(event) {
      this._switch.css({ left: event.target.offsetLeft});
	},

    });
})(jQuery);