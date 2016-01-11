// Simply loads typeahead.js and installs it on jQuery.
import typeahead from 'typeahead.js-browserify';

var TypeaheadService = function() {};

TypeaheadService.prototype.start = function() {
  typeahead.loadjQueryPlugin();
};

export default new TypeaheadService();
