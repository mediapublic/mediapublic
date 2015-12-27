import {Route} from 'backbone-routing';
import View from '../show/view';
import Model from 'shared/recordings/model';

function retrieveList(){


}

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render(params) {
    var _model = new Model();
    var hostName;
    if(params){
      params = params.split("&").map(function(pair){
        return pair.split("=");
      });
      for(var i = 0; i < params.length; i++){
        switch(params[i][0]){
          case "title":
            _model.attributes["title"] = params[i][1];
            break;
          case "url":
            _model.attributes["url"] = params[i][1];
            hostName = new URL(params[i][1]).host;
            break;
        }
      }
    }
    if(hostName){
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "http://localhost:6543/organizations?url=" + hostName, false); // ...
      xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
          if(xhr.responseText == "{}"){
            var list = retrieveList();
            _model.attributes["organizationList"] = list;
          } else {
            var organizationData = JSON.parse(xhr.responseText);
            _model.attributes["organizationName"] = organizationData["name"];
            _model.attributes["organizationID"] = organizationData["id"];
          }
        }
      };
      xhr.send();
    }
    this.view = new View({
      model: _model,
    });
    this.container.show(this.view);
  }
});
