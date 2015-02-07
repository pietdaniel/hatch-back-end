App = Ember.Application.create();

App.Router.map(function() {
  this.resource('query');

  this.resource('tweets', function() {
    this.resource('tweet', {path: ':id'});
  });

});

App.TweetsRoute = Ember.Route.extend({
  model: function() {
    return statuses;
  }
});

App.TweetRoute = Ember.Route.extend({
  model: function(params) {
    return $.getJSON("js/tweet_test.json").then(function(data) {
      for (var i=0;i<data.length;i++) {
        if (data[i]['id'] == params.id) {
          console.log(data[i]);
          return data[i];
        }
      }
    });
  }
});


Ember.Handlebars.helper('format-date', function(date) {
  return moment(date).fromNow();
});

var statuses = $.getJSON("js/tweet_test.json", function(data) {
  return data;
});

