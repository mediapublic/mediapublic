import CompositeView from 'shared/views/compositeview';
import SingleView from './singleview';
import Model from './model';
import template from './collectiontemplate.jade';

export default CompositeView.extend({
  template,
  className: 'organization',
  childView: SingleView,
  childViewContainer: '.organizations-list'
});
