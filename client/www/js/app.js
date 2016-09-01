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
        url: "/signin",
        templateUrl: 'html/signin.html',
        controller: 'SigninCtrl'
    });
$stateProvider.state('signup', {
        url: "/signup",
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
$stateProvider.state('footballConfirm', {
        cache:false,
        url: "/footballConfirm",
        templateUrl: 'html/footballConfirm.html',
        controller: 'FootballConfirmCtrl'
    });
$stateProvider.state('footballBills', {
        cache:false,
        url: "/footballBills",
        templateUrl: 'html/footballBills.html',
        controller: 'FootballBillsCtrl'
    });
$stateProvider.state('footballBillDetail', {
        url: "/footballBillDetail/:billid",
        templateUrl: 'html/footballBillDetail.html',
        controller: 'FootballBillDetailCtrl'
    });

$stateProvider.state('traditional', {
        url: "/traditional/:type",
        templateUrl: 'html/traditional.html',
        controller: 'TraditionalCtrl'
    });
$stateProvider.state('traditionalConfirm', {
        cache:false,
        url: "/traditionalConfirm",
        templateUrl: 'html/traditionalConfirm.html',
        controller: 'TraditionalConfirmCtrl'
    });
$stateProvider.state('traditionalBills', {
        cache:false,
        url: "/traditionalBills",
        templateUrl: 'html/traditionalBills.html',
        controller: 'TraditionalBillsCtrl'
    });
$stateProvider.state('traditionalBillDetail', {
        url: "/traditionalBillDetail/:billid",
        templateUrl: 'html/traditionalBillDetail.html',
        controller: 'TraditionalBillDetailCtrl'
    });
$urlRouterProvider.otherwise('/signin');
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
