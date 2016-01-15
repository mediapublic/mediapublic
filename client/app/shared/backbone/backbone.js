import Backbone from 'backbone';
import _ from 'underscore';

// Override root url for API requests
var orginalSync = Backbone.sync;
Backbone.sync = function(method, model, options) {
  options = options || {};
  var url = options.url;
  if (!url) {
    url = _.result(model, 'url');
  }

  // If a url was specified, and it's not absolute, we prepend the api root.
  if (url && url.indexOf('http') !== 0) {
    options.url = app.config.apiUrl + url;
  }

  // Specify that we want to send cookies along for the ride
  options.xhrFields = {
    withCredentials: true
  };

  return orginalSync.call(Backbone, method, model, options);
};

export default Backbone;
