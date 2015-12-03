import Backbone from 'backbone';
import _ from 'underscore';
import config from '../config.json';

// Override root url for API requests
var orginalSync = Backbone.sync;
Backbone.sync = function(method, model, options) {
  options = options || {};
  var url = options.url;
  if (!url) {
    url = _.result(model, 'url');
  }

  // If a url was specified, and it's not absolute, we prepend the api root.
  if (url && url.indexOf('http') != 0) {
    options.url = config.apiUrl + url;
  }
  return orginalSync.call(Backbone, method, model, options);
};

export default Backbone;
