var server="http://127.0.0.1:8000";
var acct;
var matches;

function myhttp($http,url,data,successfunc){
    $http({
        method: 'POST',
        url: url,
        data: data,
        headers: {'Content-Type':'text/plain'}
    })
    .success(function(data){
        if(data['errmsg']=='success'){
            successfunc(data);
        }
        else
            alert(data['errmsg']);
    })
    .error(function(data){
        alert('http error');
    });
}

app.controller('MenuCtrl',['$scope','$state',
    function($scope,$state){
        $scope.accountDetail=function(){
            if(acct===undefined){
                $state.go('signin',{next:'accountDetail'});
            }
            else{
                $state.go('accountDetail');
            }
        }
        $scope.football=function(){
            if(acct===undefined){
                $state.go('signin',{next:'football'});
            }
            else{
                $state.go('football',{},{reload:true});
            }
        }
    }]);

app.controller('SigninCtrl',['$scope','$http','$cordovaToast','$state','$ionicHistory',
    function($scope,$http,$cordovaToast,$state,$ionicHistory){
        $scope.signinData = {};
        $scope.signin=function(){
            data=myhttp($http,server+'/account/signin',{email:$scope.signinData.email,password:$scope.signinData.password},function(data){
                acct=data;
                next=$state.params['next'];
                if(next=='prev'){
                    $ionicHistory.goBack(-1);
                }
                else{
                    $ionicHistory.currentView($ionicHistory.backView());
                    $state.go(next,{},{location:'replace'});
                }
            });
        };
        $scope.signinToSignup=function(){
            $state.go('signup',{next:$state.params['next']});
        };
    }]);

app.controller('SignupCtrl',['$scope','$http','$cordovaToast','$state','$ionicHistory',
    function($scope,$http,$cordovaToast,$state,$ionicHistory){
        $scope.signupData = {sex:"0"};
        $scope.signup=function(){
            myhttp($http,server+'/account/signup',$scope.signupData,function(data){
                acct=data;
                next=$state.params['next'];
                if(next=='prev'){
                    $ionicHistory.goBack(-2);
                }
                else{
                    backBackViewId=$ionicHistory.backView()['backViewId'];
                    backBackView=$ionicHistory.viewHistory()['views'][backBackViewId];
                    $ionicHistory.currentView(backBackView);
                    $state.go(next,{},{location:'replace'});
                }
            });
        };
        $scope.signupToSignin=function(){
            $ionicHistory.goBack(-1);
        };
    }]);

app.controller('AccountDetailCtrl',['$scope','$state','$ionicHistory',
    function($scope,$state,$ionicHistory){
        if(acct===undefined){
            alert('no account');
        }
        else{
            $scope.acct=acct;
        }
    }]);

app.controller('FootballCtrl',['$scope','$state','$http','$ionicModal',
    function($scope,$state,$http,$ionicModal){
        //if(acct==undefined){
        //    alert('no account');
        //    return;
        //}
        $scope.categories=[
            {title:'胜平负',indices:[[0,1,2]]},
            {title:'让球胜平负',indices:[[3,4,5]]},
            {title:'总进球',indices:[[6,7,8,9],[10,11,12,13]]},
            {title:'半全场',indices:[[14,15,16],[17,18,19],[20,21,22]]},
            {title:'全场比分',indices:[[23,24,25,26,27,28],[29,30,31,32,33,34],[35],[36,37,38,39],[40],[41,42,43,44,45,46],[47,48,49,50,51,52],[53]]}
        ];
        $scope.range=function(n){
            r=[];
            for(i=0;i<n;i++){
                r.push(i);
            }
            return r;
        };
        $scope.labels=['胜','平','负','让球胜','让球平','让球负','0','1','2','3','4','5','6','7+','胜胜','胜平','胜负','平胜','平平','平负','负胜','负平','负负',
                      '1:0','2:0','2:1','3:0','3:1','3:2','4:0','4:1','4:2','5;0','5:1','5:2','胜其它',
                      '0:0','1:1','2:2','3:3','平其它',
                      '0:1','0:2','1:2','0:3','1:3','2:3','0:4','1:4','2:4','0:5','1:5','2:5','负其它'];

        $ionicModal.fromTemplateUrl('html/options.html',{
            scope:$scope
        }).then(function(modal){
            $scope.optionsModal=modal;
        });
        $scope.showOptions=function(index){
            $scope.match=$scope.matches[index];
            if($scope.match.selected===undefined){
                $scope.selectedTemp={};
            }
            else{
                $scope.selectedTemp=JSON.parse(JSON.stringify($scope.match.selected));
            }
            $scope.optionsModal.show();
        };
        $scope.closeOptions=function(){
            $scope.match=null;
            $scope.selectedTemp=null;
            $scope.optionsModal.hide();
        };
        $scope.confirmOptions=function(){
            if(Object.keys($scope.selectedTemp).length>0){
                $scope.match.selected=$scope.selectedTemp;
            }
            else{
                delete $scope.match.selected;
            }
            $scope.match=null;
            $scope.selectedTemp=null;
            $scope.optionsModal.hide();
        };
        $scope.select=function(option){
            if(option in $scope.selectedTemp){
                delete $scope.selectedTemp[option];
            }
            else{
                $scope.selectedTemp[option]=true;
            }
        };
        $scope.isSelected=function(option){
            return option in $scope.selectedTemp;
        };

        $scope.goNext=function(){
            matches=$scope.matches;
            $state.go('football2',{},{reload:true});
        };
        $scope.doRefresh=function(){
            myhttp($http,server+'/football/getMatchInfo','',function(data){
                $scope.matches=data['matches'];
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
        $scope.doRefresh();
    }]);

app.controller('Football2Ctrl',['$scope','$state','$http','$ionicModal',
    function($scope,$state,$http,$ionicModal){
        $scope.buy=function(){
            $state.go('football');
        };

        $scope.selectedMatchNumber=0;
        $scope.selectedMatches=[];
        for(i=0;i<matches.length;i++){
            match=matches[i];
            if(match.selected===undefined){
                continue;
            }
            n=Object.keys(match.selected).length;
            match['selectedNum']=n;
            $scope.selectedMatchNumber++;
            $scope.selectedMatches.push(match);
        }
    }]);
