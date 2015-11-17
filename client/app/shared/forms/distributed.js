import Backbone from 'backbone';
import BackboneForm from './form';
import util from '../utilities.js';
import _ from 'underscore';


var DistributedForm = BackboneForm.extend({

  /**
   * Barebones wrapper around the parent implementation that just requires a
   * uniqe identifier to be passed.
   *
   * @param  {string} options.modelCid A unique identifier, possibly
   *     Backbone's client id.
   */
  initialize: function(options) {
    util.requirePresence(options, ['modelCid']);
    this.modelCid = options.modelCid;
    return BackboneForm.prototype.initialize.apply(this, arguments);
  },


  /**
   * Find all of the elements in the DOM that have been marked as belonging to
   * the model--specified (by cid) at initialization--and replace their
   * contents with the appropriate editor elements (editor, field, or
   * fieldset). Any element that should be replaced must have both the
   * 'model=uniqueid' attribute and a secondary attribute of 'data-editor',
   * 'data-field', or 'data-fieldset' specified.
   */
  render: function() {
    var self = this,
        fields = this.fields,
        $ = Backbone.$,
        editableElements = $('[model=' + this.modelCid + ']');

    //Render standalone editors
    editableElements.each(function(i, el) {
      var $container = $(el),
          selection = $container.attr('data-editors');

      if (_.isUndefined(selection)) return;

      //Work out which fields to include
      var keys = (selection == '*')
        ? self.selectedFields || _.keys(fields)
        : selection.split(',');

      // Clear the current contents of the container
      $container.empty();

      //Add the editors
      _.each(keys, function(key) {
        var field = fields[key];

        $container.append(field.editor.render().el);
      });
    });

    //Render standalone fields
    editableElements.each(function(i, el) {
      var $container = $(el),
          selection = $container.attr('data-fields');

      if (_.isUndefined(selection)) return;

      //Work out which fields to include
      var keys = (selection == '*')
        ? self.selectedFields || _.keys(fields)
        : selection.split(',');

      // Clear the current contents of the container
      $container.empty();

      //Add the fields
      _.each(keys, function(key) {
        var field = fields[key];

        $container.append(field.render().el);
      });
    });

    //Render fieldsets
    editableElements.each(function(i, el) {
      var $container = $(el),
          selection = $container.attr('data-fieldsets');

      if (_.isUndefined(selection)) return;

      _.each(self.fieldsets, function(fieldset) {
        $container.append(fieldset.render().el);
      });
    });

    return this;
  }
});

export default DistributedForm;
