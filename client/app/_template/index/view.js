import {CollectionView} from 'backbone.marionette';
import CardView from './cardview';

export default CollectionView.extend({
  className: 'index',
  childView: CardView
});
