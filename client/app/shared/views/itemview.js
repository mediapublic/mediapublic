import {ItemView} from 'backbone.marionette';
import Backbone from 'backbone';
import {Model} from 'backbone';
import _ from 'underscore';
import Form from 'shared/forms/distributed';


/**
 * Standard ItemView, extended to include the model cid in all serialized data.
 */
export default ItemView.extend({

  initialize: function(options) {
    if (_.isUndefined(options.editing)) {
      options.editing = options.model && options.model.isNew();
    }

    this.state = new Model({
      editing: options.editing || false,
      flashSuccess: options.flashSuccess || undefined,
      flashError: options.flashError || undefined,
      flashInfo: options.flashInfo || undefined,
      flashWarning: options.flashWarning || undefined
    });

    this.listenTo(this.state, 'change', this.render);
    this.editor = null;

    if (this.model && this.model.isNew()) {
      this.listenToOnce(this.model, 'sync', this.navigateToModel);
    }

    return ItemView.prototype.initialize.apply(this, arguments);
  },


  events: {
    'click .edit': 'renderEditor',
    'click .save': 'saveChanges',
    'click .cancel': 'cancelEditing'
  },


  serializeData: function() {
    var data = ItemView.prototype.serializeData.apply(this, arguments);
    if (data.viewState) {
      throw new Error('viewState is a reserved data keyword');
    }
    data.viewState = this.state.toJSON();
    return data;
  },


  serializeCollection: function(collection) {
    var args = arguments;
    return _.map(collection, function(model) {
      return _.extend({}, model.toJSON.apply(model, _.rest(args)), {
        cid: model.cid
      });
    });
  },


  serializeModel: function(model) {
    return _.extend({}, this.model.toJSON.apply(model, _.rest(arguments)), {
      cid: model.cid
    });
  },


  render: function() {
    ItemView.prototype.render.apply(this, arguments);
    var self = this;

    if (this.state.get('editing')) {
      _.defer(function() {
        self.editor = new Form({
          model: self.model,
          modelCid: self.model.cid,
          el: self.el
        });

        self.editor.render();
        self.trigger('editing');
      });
    }
    return this;
  },


  renderEditor: function() {
    this.clearFlash({ silent: true });
    this.state.set('editing', true);
  },


  saveChanges: function() {
    var self = this;
    var errors = this.editor.commit({ validate: true });
    if (!errors) {
      this.trigger('saving:started', self);
      this.model.save().done(function() {
        self.state.set({
          editing: false,
          flashSuccess: 'Your changes have been saved!'
        });
        self.trigger('saving:done', self);
        self.model.trigger('editing:done');
      });
    } else {
      console.log(errors);
    }
  },


  cancelEditing: function() {
    this.state.set('editing', false);
    this.model.trigger('editing:cancel');
  },


  navigateToModel: function(model, options) {
    model = model || this.model;
    if (!model) {
      throw new Error('No model specified to navigate to.');
    }

    var fragment = _.result(model, 'permalink');

    if (_.isUndefined(fragment)) {
      throw new Error('No permalink specified on the model');
    }

    Backbone.history.navigate(fragment, options);
  },


  clearFlash(options) {
    this.state.set({
      flashSuccess: undefined,
      flashError: undefined,
      flashInfo: undefined,
      flashWarning: undefined,
    }, options);
  }
});
