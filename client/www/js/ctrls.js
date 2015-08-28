var server="http://127.0.0.1:8000";
var acct;
//acct.email='a@b.com';
//acct.password='qwe';
var matches;
var traditional_info;

var traditional_type_texts={
    '14':'14场',
    '9':'任选9'
};
var optionText=['胜','平','负','让球胜','让球平','让球负','0','1','2','3','4','5','6','7+','胜胜','胜平','胜负','平胜','平平','平负','负胜','负平','负负',
              '1:0','2:0','2:1','3:0','3:1','3:2','4:0','4:1','4:2','5;0','5:1','5:2','胜其它',
              '0:0','1:1','2:2','3:3','平其它',
              '0:1','0:2','1:2','0:3','1:3','2:3','0:4','1:4','2:4','0:5','1:5','2:5','负其它'];

function options2text(options){
    texts=[];
    var i;
    for(i=0;i<options.length;i++){
        texts.push(optionText[options[i]]);
    }
    return texts.join('/');
}

function combs2text(combs){
    texts=[];
    var i;
    for(i=0;i<combs.length;i++){
        texts.push(combs[i]+'串1');
    }
    return texts.join('/');
}

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
        $scope.go=function(next,params){
            if(acct===undefined){
                $state.go('signin');
            }
            else{
                $state.go(next,params);
            }
        };
        //$scope.accountDetail=function(){
        //    if(acct===undefined){
        //        $state.go('signin',{next:'accountDetail'});
        //    }
        //    else{
        //        $state.go('accountDetail');
        //    }
        //};
        //$scope.football=function(){
        //    if(acct===undefined){
        //        $state.go('signin',{next:'football'});
        //    }
        //    else{
        //        $state.go('football');
        //    }
        //};
        //$scope.matches14=function(){
        //    alert();
        //    //if(acct===undefined){
        //    //    $state.go('signin',{next:'football'});
        //    //}
        //    //else{
        //        $state.go('/traditional/14');
        //    //}
        //};
        //$scope.matches9=function(){
        //    if(acct===undefined){
        //        $state.go('signin',{next:'football'});
        //    }
        //    else{
        //        $state.go('traditional',{type:'9'});
        //    }
        //};
    }]);

app.controller('SigninCtrl',['$scope','$http','$cordovaToast','$state','$ionicHistory',
    function($scope,$http,$cordovaToast,$state,$ionicHistory){
        $scope.signinData = {};
        $scope.signin=function(){
            data=myhttp($http,server+'/account/signin',$scope.signinData,function(data){
                acct=data;
                $ionicHistory.goBack(-1);
            });
        };
        $scope.signinToSignup=function(){
            $state.go('signup');
        };
    }]);

app.controller('SignupCtrl',['$scope','$http','$cordovaToast','$state','$ionicHistory',
    function($scope,$http,$cordovaToast,$state,$ionicHistory){
        $scope.signupData = {sex:"0"};
        $scope.signup=function(){
            myhttp($http,server+'/account/signup',$scope.signupData,function(data){
                acct=data;
                $ionicHistory.goBack(-2);
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

        $ionicModal.fromTemplateUrl('html/options.html',{
            scope:$scope
        }).then(function(modal){
            $scope.optionsModal=modal;
        });
        $scope.optionSelected=[];
        $scope.showOptions=function(index){
            $scope.match=$scope.matches[index];
            for(i=0;i<54;i++){
                $scope.optionSelected[i]=false;
            }
            selectedOptions=$scope.match.selectedOptions;
            if(selectedOptions!==undefined){
                for(i=0;i<selectedOptions.length;i++){
                    $scope.optionSelected[selectedOptions[i]]=true;
                }
            }
            $scope.optionsModal.show();
        };
        $scope.closeOptions=function(){
            $scope.optionsModal.hide();
        };
        $scope.confirmOptions=function(){
            selectedOptions=[];
            for(i=0;i<54;i++){
                if($scope.optionSelected[i]){
                    selectedOptions.push(i);
                }
            }
            if(selectedOptions.length>0){
                $scope.match.selectedOptions=selectedOptions;
                $scope.match.selectedOptionsText=options2text(selectedOptions);
            }
            else{
                delete $scope.match.selectedOptions;
                delete $scope.match.selectedOptionsText;
            }
            $scope.optionsModal.hide();
        };
        $scope.optionPressed=function(option){
            $scope.optionSelected[option]=!$scope.optionSelected[option];
        };
        $scope.isOptionSelected=function(option){
            return $scope.optionSelected[option];
        };
        $scope.optionText=optionText;
        $scope.matchSelected=function(index){
            return $scope.matches[index].selectedOptions!==undefined;
        };
        $scope.goNext=function(){
            matches=$scope.matches;
            $state.go('footballConfirm');
        };
        $scope.doRefresh=function(){
            myhttp($http,server+'/football/getMatchInfo',{email:acct.email,password:acct.password},function(data){
                $scope.matches=data['matches'];
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
        $scope.doRefresh();
    }]);

app.controller('FootballConfirmCtrl',['$scope','$state','$http','$ionicModal','$ionicHistory','$ionicPopup',
    function($scope,$state,$http,$ionicModal,$ionicHistory,$ionicPopup){
        $scope.selectedMatches=[];
        for(i=0;i<matches.length;i++){
            match=matches[i];
            if(match.selectedOptions!==undefined){
                $scope.selectedMatches.push(match);
            }
        }

        $scope.multiple=1;
        $scope.plus=function(){
            if($scope.multiple<99){
                $scope.multiple+=1;
            }
        };
        $scope.minus=function(){
            if($scope.multiple>1){
                $scope.multiple-=1;
            }
        };
        $ionicModal.fromTemplateUrl('html/comb.html',{
            scope:$scope
        }).then(function(modal){
            $scope.combModal=modal;
        });
        $scope.combs=[
            {num:2,selected:false,text:'2串1'},
            {num:3,selected:false,text:'3串1'},
            {num:4,selected:false,text:'4串1'}
        ];
        $scope.showComb=function(){
            $scope.combModal.show();
        };
        $scope.confirmComb=function(){
            $scope.combModal.hide();
        };
        $scope.selectedCombsText=function(){
            var i;
            var selectedCombs=[];
            for(i=0;i<$scope.combs.length;i++){
                if($scope.combs[i].selected){
                    selectedCombs.push($scope.combs[i].num);
                }
            }
            return combs2text(selectedCombs);
        };

        $scope.createBill=function(){
            if($scope.selectedMatches.length===0){
                alert('no match selected');
                return;
            }
            selectedCombs=[];
            for(i=0;i<$scope.combs.length;i++){
                if($scope.combs[i].selected){
                    selectedCombs.push($scope.combs[i].num);
                }
            }
            if(selectedCombs.length===0){
                alert('no comb selected');
                return;
            }
            if(!$scope.multiple||$scope.multiple<1||$scope.multiple>99){
                alert("multiple:1-99");
                return;
            }

            $ionicPopup.confirm({
                title: '确认下单',
                template: '是否确认下单？'
            }).then(function(yes){
                if(!yes){
                    return;
                }
                billInfo={};
                billInfo.email=acct.email;
                billInfo.password=acct.password;
                billInfo.multiple=$scope.multiple;
                billInfo.combs=selectedCombs;
                billInfo.matches=[];
                for(i=0;i<$scope.selectedMatches.length;i++){
                    match=$scope.selectedMatches[i];
                    billInfo.matches.push({
                        'id':match.id,
                        'selectedOptions':match.selectedOptions
                    });
                }

                myhttp($http,server+'/football/createBill',billInfo,function(data){
                    backBackViewId=$ionicHistory.backView()['backViewId'];
                    backBackView=$ionicHistory.viewHistory()['views'][backBackViewId];
                    $ionicHistory.currentView(backBackView);
                    $ionicHistory.clearCache();
                    $state.go('footballBillDetail',{billid:data.billid},{location:'replace'});
                });
            });
        };
    }]);

app.controller('FootballBillsCtrl',['$scope','$state','$http',
    function($scope,$state,$http){
        myhttp($http,server+'/football/getFootballBills',{email:acct.email,password:acct.password},function(data){
            $scope.fbills=data.bills.reverse();
            //if($state.params['forward']=='true'){
            //    $state.go('footballBillDetail',{billid:$scope.fbills[0].id});
            //}
        });
        $scope.showDetail=function(index){
            $state.go('footballBillDetail',{billid:$scope.fbills[index].id});
        };
    }]);

app.controller('FootballBillDetailCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory',
    function($scope,$state,$ionicPopup,$http,$ionicHistory){
        billid=$state.params['billid'];
        myhttp($http,server+'/football/getFootballBillDetail',{email:acct.email,password:acct.password,billid:billid},function(data){
            $scope.fbill=data.bill;
            for(i=0;i<$scope.fbill.matches.length;i++){
                options=JSON.parse($scope.fbill.matches[i].selectedOptions);
                $scope.fbill.matches[i].selectedOptionsText=options2text(options);
            }
            combs=JSON.parse($scope.fbill.comb_type);
            $scope.fbill.combsText=combs2text(combs);
        });

        $scope.pay=function(){
            money=2*$scope.fbill.bet_count*$scope.fbill.multiple;
            $ionicPopup.confirm({
                title: '确认付款',
                template: '是否确认付款'+money+'元？'
            }).then(function(yes){
                if(yes){
                    billid=$scope.fbill.id;
                    payInfo={};
                    payInfo.billid=billid;
                    payInfo.email=acct.email;
                    payInfo.password=acct.password;
                    myhttp($http,server+'/football/payFootball',payInfo,function(data){
                        $scope.fbill.is_payed=true;
                        $ionicPopup.alert({
                            title: '付款成功',
                            template: '付款成功！'
                        });
                    });
                }
            });
        };

        $scope.del=function(){
            $ionicPopup.confirm({
                title: '确认删除订单',
                template: '是否确认删除订单？'
            }).then(function(yes){
                if(yes){
                    delInfo={};
                    delInfo.email=acct.email;
                    delInfo.password=acct.password;
                    delInfo.billid=$scope.fbill.id;
                    myhttp($http,server+'/football/delFootballBill',delInfo,function(data){
                        $ionicPopup.alert({
                            title: '删除成功',
                            template: '删除成功！'
                        }).then(function(){
                            $ionicHistory.goBack(-1);
                        });
                    });
                }
            });
        };
    }]);

app.controller('TraditionalCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory',
    function($scope,$state,$ionicPopup,$http,$ionicHistory){
        $scope.traditional_info={};
        $scope.traditional_info.type=$state.params.type;
        $scope.selected=[];
        for(i=0;i<14;i++){
            $scope.selected.push([false,false,false]);
        }

        $scope.press=function(m,i){
            $scope.selected[m][i]=!$scope.selected[m][i];
        };
        $scope.isSelected=function(m,i){
            return $scope.selected[m][i];
        };
        $scope.goNext=function(){
            var i,j,n=0;
            for(i=0;i<$scope.selected.length;i++){
                var selectedOptions=[];
                for(j=0;j<3;j++){
                    if($scope.selected[i][j]){
                        selectedOptions.push(j);
                    }
                }
                if(selectedOptions.length!==0){
                    n++;
                }
                $scope.traditional_info.matches[i].selectedOptions=selectedOptions;
            }
            if(n<parseInt($scope.traditional_info.type,10)){
                $ionicPopup.alert({
                    title:'错误',
                    template:'请至少选择'+$scope.traditional_info.type+'场'
                });
            }
            else{
                traditional_info=$scope.traditional_info;
                $state.go("traditionalConfirm");
            }
        };
        $scope.doRefresh=function(){
            myhttp($http,server+'/football/getTraditionalInfo',{email:acct.email,password:acct.password},function(data){
                $scope.traditional_info.id=data.id;
                $scope.traditional_info.SN=data.SN;
                $scope.traditional_info.deadline=data.deadline;
                $scope.traditional_info.matches=data.matches;
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
        $scope.doRefresh();
    }]);

app.controller('TraditionalConfirmCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory',
    function($scope,$state,$ionicPopup,$http,$ionicHistory){
        $scope.traditional_info=traditional_info;
        $scope.type_text=traditional_type_texts[$scope.traditional_info.type];
        $scope.options2text=options2text;

        $scope.traditional_info.multiple=1;
        $scope.plus=function(){
            if($scope.traditional_info.multiple<99){
                $scope.traditional_info.multiple+=1;
            }
        };
        $scope.minus=function(){
            if($scope.traditional_info.multiple>1){
                $scope.traditional_info.multiple-=1;
            }
        };

        $scope.createBill=function(){
            $ionicPopup.confirm({
                title: '确认下单',
                template: '是否确认下单？'
            }).then(function(yes){
                if(!yes){
                    return;
                }
                billInfo={};
                billInfo.email=acct.email;
                billInfo.password=acct.password;
                billInfo.id=$scope.traditional_info.id;
                billInfo.multiple=$scope.traditional_info.multiple;
                billInfo.type=$scope.traditional_info.type;
                billInfo.matches=[];
                var i;
                for(i=0;i<traditional_info.matches.length;i++){
                    match=traditional_info.matches[i];
                    billInfo.matches.push(match.selectedOptions);
                }

                myhttp($http,server+'/football/createTraditionalBill',billInfo,function(data){
                    $ionicPopup.alert({
                        title:'下单成功',
                        template:'下单成功！'
                    }).then(function(){
                        backBackViewId=$ionicHistory.backView()['backViewId'];
                        backBackView=$ionicHistory.viewHistory()['views'][backBackViewId];
                        $ionicHistory.currentView(backBackView);
                        $ionicHistory.clearCache();
                        $state.go('traditionalBills',{forward:true},{location:'replace'});
                    });
                });
            });
        };
    }]);

app.controller('TraditionalBillsCtrl',['$scope','$state','$http',
    function($scope,$state,$http){
        $scope.type_texts=traditional_type_texts;
        myhttp($http,server+'/football/getTraditionalBills',{email:acct.email,password:acct.password},function(data){
            $scope.bills=data.bills.reverse();
        });
        $scope.showDetail=function(index){
            $state.go('traditionalBillDetail',{billid:$scope.bills[index].id});
        };
    }]);

app.controller('TraditionalBillDetailCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory',
    function($scope,$state,$ionicPopup,$http,$ionicHistory){
        $scope.options2text=options2text;
        billid=$state.params.billid;
        myhttp($http,server+'/football/getTraditionalBillDetail',{email:acct.email,password:acct.password,billid:billid},function(data){
            $scope.bill=data.bill;
        });

        $scope.pay=function(){
            money=2*$scope.bill.bet_count*$scope.bill.multiple;
            $ionicPopup.confirm({
                title: '确认付款',
                template: '是否确认付款'+money+'元？'
            }).then(function(yes){
                if(yes){
                    billid=$scope.bill.id;
                    payInfo={};
                    payInfo.billid=billid;
                    payInfo.email=acct.email;
                    payInfo.password=acct.password;
                    myhttp($http,server+'/football/payTraditionalBill',payInfo,function(data){
                        $scope.bill.is_payed=true;
                        $ionicPopup.alert({
                            title: '付款成功',
                            template: '付款成功！'
                        });
                    });
                }
            });
        };

        $scope.del=function(){
            $ionicPopup.confirm({
                title: '确认删除订单',
                template: '是否确认删除订单？'
            }).then(function(yes){
                if(yes){
                    delInfo={};
                    delInfo.email=acct.email;
                    delInfo.password=acct.password;
                    delInfo.billid=$scope.bill.id;
                    myhttp($http,server+'/football/delTraditionalBill',delInfo,function(data){
                        $ionicPopup.alert({
                            title: '删除成功',
                            template: '删除成功！'
                        }).then(function(){
                            $ionicHistory.goBack(-1);
                        });
                    });
                }
            });
        };
    }]);
