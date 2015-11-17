import {CollectionView} from 'backbone.marionette';
import template from './template.jade';
import CardView from './cardview';

export default CollectionView.extend({
  className: 'index',
  childView: CardView
});
