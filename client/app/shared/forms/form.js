import BackboneForm from 'backbone-forms/distribution/backbone-forms.js';
import templates from './templates';
import _ from 'underscore';

BackboneForm.validators.phone = function(options) {
  options = _.extend({
    type: 'phone',
    message: 'Invalid phone number.',
    // Taken from http://stackoverflow.com/questions/123559/a-comprehensive-regex-for-phone-number-validation
    regexp: /^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$/i
  }, options);

  return BackboneForm.validators.regexp(options);
};

BackboneForm.validators.zip = function(options) {
  options = _.extend({
    type: 'zipcode',
    message: 'Invalid zipcode.',
    regexp: /^[0-9]{5}(-[0-9]{4})?$/i
  }, options);

  return BackboneForm.validators.regexp(options);
};

BackboneForm.validators.state = function(options) {
  options = _.extend({
    type: 'state',
    message: 'Invalid two-letter state code.',
    // Lifted from http://regexlib.com/REDetails.aspx?regexp_id=1574
    regexp: /^(?:(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY]))$/i
  }, options);

  return BackboneForm.validators.regexp(options);
};

export default BackboneForm;
