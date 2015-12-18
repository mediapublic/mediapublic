/**
 * Small library of useful functions.
 */
import _ from 'underscore';
import deparam from 'jquery-deparam';
import Backbone from 'backbone';


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
  },


  getQueryParams: function() {
    var params = {};
    var queryString = window.location.search;
    if (queryString.length > 1) {
      params = deparam(queryString.slice(1));
    }

    var hashParts = window.location.hash.split('?')
    if (hashParts.length > 1) {
      _.extend(params, deparam(hashParts[1]));
    }

    return params;
  },


  updateQueryParams: function(params) {
    var href = window.location.hash;
    _.each(params, function(value, key) {
      href = href.replace(new RegExp(key + '=[^&]*(&)?'), key + '=' + value + '$1');
    });
    Backbone.history.navigate(href, {replace: true});
  }
};
