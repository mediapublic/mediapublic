import TextEditor from './text';
import _ from 'underscore';
import $ from 'jquery';

var numTinyMceRetries = 100;
var tinyMCELoaded = false;
var renderedMap = {};

export default TextEditor.extend({
  tagname: 'div',
  overlaid: true,
  render() {
    if (!tinyMCELoaded) {
      loadTinyMCE().done(_.bind(this.render, this));
      return this;
    }

    // Failure.
    if (numTinyMceRetries === 0) {
      return this;
    }

    // If the variable isn't loaded, give it a tenth of a second and try again.
    // Per http://api.jquery.com/jQuery.getScript/ the success callback can
    // be fired before the script has finished executing.
    if (!window.tinyMCE) {
      numTinyMceRetries--;
      _.delay(_.bind(this.render, this), 100);
      return this;
    }

    this.$el.attr('id', this.id);
    var self = this;

    // Defer so that this element gets added to the dom before tinyMCE goes
    // looking for it.
    _.defer(function() {
      if (renderedMap[self.id]) {
        window.tinyMCE.EditorManager.execCommand('mceRemoveEditor', false, self.id);
        window.tinyMCE.EditorManager.execCommand('mceAddEditor', true, self.id);
      } else {
        window.tinyMCE.init({
          selector: '#' + self.id,
          // TODO(gabeisman): investigate this further. Seemed to cause some strange and
          // hard to predict bugs. Definitely a little bit nicer experience, but
          // risky at this point IMO.
          // inline: true
        });
      }

      renderedMap[self.id] = true;
    });

    return this;
  },

  getValue() {
    return window.tinyMCE.get(this.id).getContent();
  },

  setValue(value) {
    this.value = value;
    window.tinyMCE.get(this.id).setContent(value);
  }
});


function loadTinyMCE() {
  tinyMCELoaded = true;
  return $.getScript('//cdn.tinymce.com/4/tinymce.min.js')
    .fail(function() {
      tinyMCELoaded = false;
    });
}
