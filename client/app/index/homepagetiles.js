import {CollectionView} from 'backbone.marionette';
import RecordingView from 'shared/recordings/singleview';
import HowtoView from 'shared/howtos/singleview';
import HelpRequestView from 'shared/helprequests/singleview';
import PersonView from 'shared/people/singleview';

export default CollectionView.extend({
  getChildView(model) {
    switch(model.urlRoot()) {
      case('/recordings'):
        console.log('recordings');
        return RecordingView;
      case('/howtos'):
        console.log('howt');
        return HowtoView;
      case('/users'):
        console.log('p');
        return PersonView;
      case('/help-requests'):
        console.log('hr');
        return HelpRequestView;
      case('/people'):
      case('/users'):
        return PersonView;
      default:
        console.log(model.urlRoot());
        return null;
    }
  }
});
