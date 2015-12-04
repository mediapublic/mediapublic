import TextEditor from './text';

export default TextEditor.extend({
  tagname: 'div',
  overlaid: true,
  render() {
    this.$el.attr('id', this.id);
    window.tinyMCE.init({
      selector: '#' + this.id,
      // TODO(gabeisman): investigate this further. Seemed to cause some strange and
      // hard to predict bugs. Definitely a little bit nicer experience, but
      // risky at this point IMO.
      // inline: true
    });
  },

  getValue() {
    return window.tinyMCE.get(this.id).getContent();
  },

  setValue(value) {
    this.value = value;
    window.tinyMCE.get(this.id).setContent(value);
  }
});
