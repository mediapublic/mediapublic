/**
 * Small library of useful functions.
 */
var _ = require('underscore');


module.exports = {


  /**
   * Ensures that requiredKeys are present in options, throwing an informative
   * error message if not.
   *
   * @param  {[type]} options      An options hash.
   * @param  {[type]} requiredKeys The keys that must be present.
   * @return {undefined}
   */
  requirePresence: function(options, requiredKeys) {
    if (_.isUndefined(options)) {
      throw new Error('Missing options');
    }

    if (!_.isObject(options)) {
      throw new Error('Options is not an object');
    }

    _.each(requiredKeys, function(key) {
      if (_.isUndefined(options[key])) {
        throw new Error('Missing option ' + key);
      }
    });
  },


  /**
   * Exactly what it sounds like.
   *
   * @param  {Object}  obj
   * @return {Boolean}
   */
  isNullOrUndefined: function(obj) {
    return _.isNull(obj) || _.isUndefined(obj);
  },


  /**
   * Takes a URL and ensures that it ends with a trailing slash.
   *
   * @param  {string} url
   * @return {string}
   */
  ensureTrailingSlash: function(url) {
    if (url.charAt(url.length - 1) != '/') {
      url += '/';
    }

    return url;
  }
};
