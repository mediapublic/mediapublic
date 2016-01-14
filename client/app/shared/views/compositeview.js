import {CompositeView} from 'backbone.marionette';
import {Model} from 'backbone';

export default CompositeView.extend({
  initialize(options) {
    this.state = new Model({
      more: options.more || false,
    });
    this.updateState();
    this.listenTo(this.state, 'change', this.render);
    this.listenTo(this.collection, 'sync', this.updateState);
  },

  numModels: 10,

  events: {
    'click .load-more': 'loadMore',
    'click .load-less': 'loadLess'
  },

  loadMore() {
    this.state.set('more', true);
  },

  loadLess() {
    this.state.set('more', false);
  },

  serializeData() {
    var data = CompositeView.prototype.serializeData.apply(this, arguments);
    if (data.viewState) {
      throw new Error('viewState is a reserved data keyword');
    }
    data.viewState = this.state.toJSON();

    data.items = this.collection ? this.collection.toJSON() : [];

    return data;
  },

  filter(child, index) {
    return this.state.get('more') || index < this.numModels;
  },

  updateState() {
    this.state.set({
      hasMore: this.collection && this.collection.length > this.numModels,
      isEmpty: !this.collection ||
          (!this.collection.fetchInProgress && this.collection.length === 0)
    });
  }
});
