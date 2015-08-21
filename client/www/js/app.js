// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'

var app=angular.module('starter', ['ionic','ui.router','ngCordova','validation.match']);

app.config(['$stateProvider','$urlRouterProvider',function($stateProvider,$urlRouterProvider){
$stateProvider.state('menu', {
        url: "/menu",
        templateUrl: 'html/menu.html',
        controller: 'MenuCtrl'
    });
$stateProvider.state('signin', {
        url: "/signin/:next",
        templateUrl: 'html/signin.html',
        controller: 'SigninCtrl'
    });
$stateProvider.state('signup', {
        url: "/signup/:next",
        templateUrl: 'html/signup.html',
        controller: 'SignupCtrl'
    });
$stateProvider.state('accountDetail', {
        url: "/accountDetail",
        templateUrl: 'html/accountDetail.html',
        controller: 'AccountDetailCtrl'
    });
$stateProvider.state('football', {
        url: "/football",
        templateUrl: 'html/football.html',
        controller: 'FootballCtrl'
    });
$stateProvider.state('football2', {
        url: "/football2",
        templateUrl: 'html/football2.html',
        controller: 'Football2Ctrl'
    });
$stateProvider.state('footballBills', {
        url: "/footballBills",
        templateUrl: 'html/footballBills.html',
        controller: 'FootballBillsCtrl'
    });
$stateProvider.state('footballBillDetail', {
        url: "/footballBillDetail/:index",
        templateUrl: 'html/footballBillDetail.html',
        controller: 'FootballBillDetailCtrl'
    });
$urlRouterProvider.otherwise('/menu');
}]);

app.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
});
