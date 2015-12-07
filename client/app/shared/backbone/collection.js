import {Collection} from 'backbone';

export default Collection.extend({
  // Automatically unwrap data from the server
  parse: (data) => data.data,
  fetch(options) {
    var self = this;
    options = options || {};
    var success = options.success;
    this.fetchInProgress = true;
    options.success = function() {
      self.fetchInProgress = false;
      if (success) success.apply(options.context, arguments);
    };
    this.fetchPromise = Collection.prototype.fetch.call(this, options)
      .always(() => this.fetchInProgress = false);
    return this.fetchPromise;
  }
});
