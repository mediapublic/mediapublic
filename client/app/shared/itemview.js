import {ItemView} from 'backbone.marionette';
import {Model} from 'backbone';
import _ from 'underscore';
import Form from 'shared/forms/distributed';


/**
 * Standard ItemView, extended to include the model cid in all serialized data.
 */
export default ItemView.extend({

  initialize: function(options) {
    this.state = new Model({
      editing: options.editing || false
    });
    this.listenTo(this.state, 'change', this.render);
    this.editor = null;
    return ItemView.prototype.initialize.apply(this, arguments);
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
    this.state.set('editing', true);
  },


  saveChanges: function() {
    var self = this;
    var errors = this.editor.commit({ validate: true });
    if (!errors) {
      this.trigger('saving:started', self);
      this.model.save().done(function() {
        self.state.set('editing', false);
        self.trigger('saving:done', self);
      });
    } else {
      console.log(errors);
    }
  }
});
