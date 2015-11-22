import {CollectionView} from 'backbone.marionette';
import Single from './single';

export default CollectionView.extend({
  className: 'people',
  childView: Single
});
