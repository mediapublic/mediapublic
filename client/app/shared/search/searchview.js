import {ItemView} from 'backbone.marionette';
import datasets from 'shared/search/datasets';
import template from './searchtemplate.jade';

export default ItemView.extend({
  template,
  className: 'search-view',
  onAttach() {
    this.$('input[type=text]').typeahead(datasets.organizations);
  }
});
