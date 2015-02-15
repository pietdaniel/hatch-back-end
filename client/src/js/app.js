App = Ember.Application.create();


var search = function(query) {
  var url = "http://localhost:5000/search?q=" + query;
  return $.getJSON(url, function(data) {
    return data;
  });
};

App.Router.map(function() {
  this.resource('search');
  this.resource('tweets', { path: '/tweets/:query' }, function() {
    this.resource('tweet', { path: ':id' });
  });
});

App.SearchController = Ember.Controller.extend({
  search: '',
  actions: {
    query: function() {
      var query = this.get('search');
      var self = this;
      search(query).then(function(data) {
        console.log(data);
        var result = { query: query, result: data };
        self.transitionToRoute('tweets', result);
      });
    }
  }
});


App.SearchRoute = Ember.Route.extend({
  model: function(params) {
    return "";
  }
});

App.TweetsRoute = Ember.Route.extend({
  model: function(params) {
    search(params.query).then(function(data) {
      return { result: data };
    });
  },
  serialize: function(model) {
    return model;
  }
});

Ember.Handlebars.helper('format-date', function(date) {
  return moment(date).fromNow();
});
