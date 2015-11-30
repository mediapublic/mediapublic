import colorbrewer from '../colors/colorbrewer';

export default {
  randomColor(cid, palette, tones) {
    var palette = colorbrewer[palette || 'Spectral'][tones || 9];
    var index = parseInt(cid.replace('c', ''), 10) % palette.length;
    return palette[index];
  }
};
