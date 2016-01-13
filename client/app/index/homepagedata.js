import faker from 'shared/utilities/faker';
import _ from 'underscore';

const fakeRecording = _.extend({ type: 'recording' }, faker.fakeRecording);
const fakePerson = _.extend({ type: 'person' }, faker.fakePerson);
const fakeHelpRequest = _.extend({ type: 'helprequest' }, faker.fakeHelpRequest);

export default [
  ...faker.replicate(fakeRecording, 4),
  ...faker.replicate(fakePerson, 2),
  ...faker.replicate(fakeHelpRequest, 3)
];
