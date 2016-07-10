//var server="http://192.168.1.250:8000";
//var server="http://127.0.0.1:8000";
var server="http://121.40.86.115:8000";
var acct;
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
    var texts=[];
    var i;
    for(i=0;i<options.length;i++){
        texts.push(optionText[options[i]]);
    }
    return texts.join('/');
}

function combs2text(combs){
    var texts=[];
    var i;
    for(i=0;i<combs.length;i++){
        texts.push(combs[i]+'串1');
    }
    return texts.join('/');
}

function product(arr){
    r=1;
    var i;
    for(i=0;i<arr.length;i++){
        r*=arr[i];
    }
    return r;
}

function combinations(arr,choose){
    var n=arr.length;
    var c=[];
    var total=0;
    var inner=function(start,choose_){
        if(choose_===0){
            total+=product(c);
        }
        else{
            var i;
            for(i=start;i<=n-choose_;++i){
                c.push(arr[i]);
                inner(i+1,choose_-1);
                c.pop();
            }
        }
    };
    inner(0,choose);
    return total;
}

function myhttp($http,$ionicPopup,$ionicLoading,url,data,successfunc){
    $ionicLoading.show({
        template: '<ion-spinner></ion-spinner><p>请稍候...</p>'
    });
    $http({
        method: 'POST',
        url: url,
        data: data,
        headers: {'Content-Type':'text/plain'}
    })
    .success(function(data){
        $ionicLoading.hide();
        if(data.errmsg=='success'){
            successfunc(data);
        }
        else{
            $ionicPopup.alert({
                title: '错误',
                template: data.errmsg
            });
        }
    })
    .error(function(data){
        $ionicLoading.hide();
        $ionicPopup.alert({
            title: '错误',
            template: '网络异常'
        });
    });
}

app.controller('MenuCtrl',['$scope','$state','$ionicPopup',
    function($scope,$state,$ionicPopup){
        $scope.isSignedIn=function(){
            return acct!==undefined;
        };
        $scope.signout=function(){
            $ionicPopup.confirm({
                title: '确认注销',
                template: '是否确认注销'
            }).then(function(yes){
                if(yes){
                    acct=undefined;
                }
            });
        };
        $scope.go=function(next,params){
            if((acct===undefined)&&(next!='signin')&&(next!='signup')){
                $state.go('signin');
            }
            else{
                $state.go(next,params);
            }
        };
    }]);

app.controller('SigninCtrl',['$scope','$http','$state','$ionicHistory','$ionicLoading','$ionicPopup',
    function($scope,$http,$state,$ionicHistory,$ionicLoading,$ionicPopup){
        $scope.signinData = {};
        $scope.signin=function(){
            data=myhttp($http,$ionicPopup,$ionicLoading,server+'/account/signin',$scope.signinData,function(data){
                acct={};
                acct.phone_number=data.phone_number;
                acct.password=$scope.signinData.password;
                $ionicHistory.nextViewOptions({
                    disableBack:true
                });
                $state.go('menu');
            });
        };
        $scope.signinToSignup=function(){
            $state.go('signup');
        };
    }]);

app.controller('SignupCtrl',['$scope','$http','$state','$ionicHistory','$ionicLoading','$ionicPopup',
    function($scope,$http,$state,$ionicHistory,$ionicLoading,$ionicPopup){
        $scope.signupData = {sex:"0"};
        $scope.signup=function(){
            myhttp($http,$ionicPopup,$ionicLoading,server+'/account/signup',$scope.signupData,function(data){
                acct={};
                acct.phone_number=data.phone_number;
                acct.password=$scope.signupData.password;
                $ionicHistory.nextViewOptions({
                    disableBack:true
                });
                $state.go('menu');
            });
        };
        $scope.signupToSignin=function(){
            $state.go('signin');
        };
    }]);

app.controller('AccountDetailCtrl',['$scope','$http','$ionicPopup','$ionicLoading',
    function($scope,$http,$ionicPopup,$ionicLoading){
        myhttp($http,$ionicPopup,$ionicLoading,server+'/account/signin',acct,function(data){
            $scope.acct=data;
        });
    }]);

app.controller('FootballCtrl',['$scope','$state','$http','$ionicModal','$ionicLoading','$ionicPopup',
    function($scope,$state,$http,$ionicModal,$ionicLoading,$ionicPopup){
        $scope.categories=[
            {title:'胜平负',indices:[[0,1,2]]},
            {title:'让球胜平负',indices:[[3,4,5]]},
            {title:'总进球',indices:[[6,7,8,9],[10,11,12,13]]},
            {title:'半全场',indices:[[14,15,16],[17,18,19],[20,21,22]]},
            {title:'全场比分',indices:[[23,24,25,26],[27,28,29,30],[31,32,33,34],[35],[36,37,38,39],[40],[41,42,43,44],[45,46,47,48],[49,50,51,52],[53]]}
        ];

        $ionicModal.fromTemplateUrl('html/options.html',{
            scope:$scope
        }).then(function(modal){
            $scope.optionsModal=modal;
        });
        //$scope.optionSelected=[];
        $scope.showOptions=function(index){
            $scope.match=$scope.matches[index];
            $scope.currentSelectedOptions=$scope.match.selectedOptions===undefined?[]:$scope.match.selectedOptions.slice(0);
            //for(i=0;i<54;i++){
            //    $scope.optionSelected[i]=false;
            //}
            //var selectedOptions=$scope.match.selectedOptions;
            //if(selectedOptions!==undefined){
            //    for(i=0;i<selectedOptions.length;i++){
            //        $scope.optionSelected[selectedOptions[i]]=true;
            //    }
            //}
            $scope.optionsModal.show();
        };
        $scope.closeOptions=function(){
            $scope.optionsModal.hide();
        };
        $scope.confirmOptions=function(){
            if($scope.currentSelectedOptions.length===0){
                $scope.match.selectedOptions=undefined;
                $scope.match.selectedOptionsText=undefined;
            }
            else{
                $scope.match.selectedOptions=$scope.currentSelectedOptions.sort(function(a,b){
                    return a>b?1:-1;
                });
                $scope.match.selectedOptionsText=options2text($scope.match.selectedOptions);
            }
            //var selectedOptions=[];
            //var i;
            //for(i=0;i<54;i++){
            //    if($scope.optionSelected[i]){
            //        selectedOptions.push(i);
            //    }
            //}
            //if(selectedOptions.length>0){
            //    $scope.match.selectedOptions=selectedOptions;
            //    $scope.match.selectedOptionsText=options2text(selectedOptions);
            //}
            //else{
            //    delete $scope.match.selectedOptions;
            //    delete $scope.match.selectedOptionsText;
            //}
            $scope.optionsModal.hide();
        };
        $scope.optionPressed=function(option){
            //$scope.optionSelected[option]=!$scope.optionSelected[option];
            index=$scope.currentSelectedOptions.indexOf(option);
            if(index==-1){
                $scope.currentSelectedOptions.push(option);
            }
            else{
                $scope.currentSelectedOptions.splice(index,1);
            }
        };
        $scope.isOptionSelected=function(option){
            return $scope.currentSelectedOptions.indexOf(option)==-1?false:true;
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
            myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getMatchInfo',acct,function(data){
                $scope.matches=data.matches;
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
        $scope.doRefresh();
    }]);

app.controller('FootballConfirmCtrl',['$scope','$state','$http','$ionicModal','$ionicHistory','$ionicPopup','$ionicLoading',
    function($scope,$state,$http,$ionicModal,$ionicHistory,$ionicPopup,$ionicLoading){
        $scope.selectedMatches=[];
        var i;
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

        arr=[];
        for(i=0;i<$scope.selectedMatches.length;i++){
            arr.push($scope.selectedMatches[i].selectedOptions.length);
        }
        $scope.combs=[];
        for(i=1;i<=$scope.selectedMatches.length;i++){
            $scope.combs.push({num:i,selected:false,bet_count:combinations(arr,i)});
        }
        $scope.total_bet_count=function(){
            total=0;
            var i;
            for(i=0;i<$scope.combs.length;i++){
                if($scope.combs[i].selected){
                    total+=$scope.combs[i].bet_count;
                }
            }
            return total;
        };

        $ionicModal.fromTemplateUrl('html/comb.html',{
            scope:$scope
        }).then(function(modal){
            $scope.combModal=modal;
        });
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
                $ionicPopup.alert({
                    title: '错误',
                    template: '请选择串关方式！'
                });
                return;
            }
            if(!$scope.multiple||$scope.multiple<1||$scope.multiple>99){
                $ionicPopup.alert({
                    title: '错误',
                    template: "倍数必须在1－99之间！" 
                });
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
                billInfo.phone_number=acct.phone_number;
                billInfo.password=acct.password;
                billInfo.multiple=$scope.multiple;
                billInfo.combs=selectedCombs;
                billInfo.matches=[];
                var i;
                for(i=0;i<$scope.selectedMatches.length;i++){
                    match=$scope.selectedMatches[i];
                    billInfo.matches.push({
                        'id':match.id,
                        'selectedOptions':match.selectedOptions
                    });
                }

                myhttp($http,$ionicPopup,$ionicLoading,server+'/football/createBill',billInfo,function(data){
                    backBackViewId=$ionicHistory.backView().backViewId;
                    backBackView=$ionicHistory.viewHistory().views[backBackViewId];
                    $ionicHistory.currentView(backBackView);
                    $ionicHistory.clearCache();
                    $state.go('footballBillDetail',{billid:data.billid},{location:'replace'});
                });
            });
        };
    }]);

app.controller('FootballBillsCtrl',['$scope','$state','$http','$ionicLoading','$ionicPopup',
    function($scope,$state,$http,$ionicLoading,$ionicPopup){
        myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getFootballBills',{phone_number:acct.phone_number,password:acct.password},function(data){
            $scope.fbills=data.bills.reverse();
        });
        $scope.showDetail=function(index){
            $state.go('footballBillDetail',{billid:$scope.fbills[index].id});
        };
    }]);

app.controller('FootballBillDetailCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory','$ionicLoading',
    function($scope,$state,$ionicPopup,$http,$ionicHistory,$ionicLoading){
        var billid=$state.params.billid;
        myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getFootballBillDetail',{phone_number:acct.phone_number,password:acct.password,billid:billid},function(data){
            $scope.fbill=data.bill;
            var i;
            for(i=0;i<$scope.fbill.matches.length;i++){
                var options=JSON.parse($scope.fbill.matches[i].selectedOptions);
                $scope.fbill.matches[i].selectedOptionsText=options2text(options);
            }
            var combs=JSON.parse($scope.fbill.comb_type);
            $scope.fbill.combsText=combs2text(combs);
        });

        $scope.pay=function(){
            var money=2*$scope.fbill.bet_count*$scope.fbill.multiple;
            $ionicPopup.confirm({
                title: '确认付款',
                template: '是否确认付款'+money+'元？'
            }).then(function(yes){
                if(yes){
                    var billid=$scope.fbill.id;
                    var payInfo={};
                    payInfo.billid=billid;
                    payInfo.phone_number=acct.phone_number;
                    payInfo.password=acct.password;
                    myhttp($http,$ionicPopup,$ionicLoading,server+'/football/payFootball',payInfo,function(data){
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
                    delInfo.phone_number=acct.phone_number;
                    delInfo.password=acct.password;
                    delInfo.billid=$scope.fbill.id;
                    myhttp($http,$ionicPopup,$ionicLoading,server+'/football/delFootballBill',delInfo,function(data){
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

app.controller('TraditionalCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory','$ionicLoading',
    function($scope,$state,$ionicPopup,$http,$ionicHistory,$ionicLoading){
        $scope.traditional_info={};
        $scope.traditional_info.type=$state.params.type;
        $scope.selected=[];
        var i;
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
            myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getTraditionalInfo',{phone_number:acct.phone_number,password:acct.password},function(data){
                $scope.traditional_info.id=data.id;
                $scope.traditional_info.SN=data.SN;
                $scope.traditional_info.deadline=data.deadline;
                $scope.traditional_info.matches=data.matches;
                $scope.$broadcast('scroll.refreshComplete');
            });
        };
        $scope.doRefresh();
    }]);

app.controller('TraditionalConfirmCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory','$ionicLoading',
    function($scope,$state,$ionicPopup,$http,$ionicHistory,$ionicLoading){
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
                var billInfo={};
                billInfo.phone_number=acct.phone_number;
                billInfo.password=acct.password;
                billInfo.id=$scope.traditional_info.id;
                billInfo.multiple=$scope.traditional_info.multiple;
                billInfo.type=$scope.traditional_info.type;
                billInfo.matches=[];
                var i;
                for(i=0;i<traditional_info.matches.length;i++){
                    var match=traditional_info.matches[i];
                    billInfo.matches.push(match.selectedOptions);
                }

                myhttp($http,$ionicPopup,$ionicLoading,server+'/football/createTraditionalBill',billInfo,function(data){
                    $ionicPopup.alert({
                        title:'下单成功',
                        template:'下单成功！'
                    }).then(function(){
                        backBackViewId=$ionicHistory.backView().backViewId;
                        backBackView=$ionicHistory.viewHistory().views[backBackViewId];
                        $ionicHistory.currentView(backBackView);
                        $ionicHistory.clearCache();
                        $state.go('traditionalBillDetail',{billid:data.billid},{location:'replace'});
                        //$state.go('traditionalBills',{forward:true},{location:'replace'});
                    });
                });
            });
        };
    }]);

app.controller('TraditionalBillsCtrl',['$scope','$state','$http','$ionicLoading','$ionicPopup',
    function($scope,$state,$http,$ionicLoading,$ionicPopup){
        $scope.type_texts=traditional_type_texts;
        myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getTraditionalBills',{phone_number:acct.phone_number,password:acct.password},function(data){
            $scope.bills=data.bills.reverse();
        });
        $scope.showDetail=function(index){
            $state.go('traditionalBillDetail',{billid:$scope.bills[index].id});
        };
    }]);

app.controller('TraditionalBillDetailCtrl',['$scope','$state','$ionicPopup','$http','$ionicHistory','$ionicLoading',
    function($scope,$state,$ionicPopup,$http,$ionicHistory,$ionicLoading){
        $scope.options2text=options2text;
        var billid=$state.params.billid;
        myhttp($http,$ionicPopup,$ionicLoading,server+'/football/getTraditionalBillDetail',{phone_number:acct.phone_number,password:acct.password,billid:billid},function(data){
            $scope.bill=data.bill;
        });

        $scope.pay=function(){
            var money=2*$scope.bill.bet_count*$scope.bill.multiple;
            $ionicPopup.confirm({
                title: '确认付款',
                template: '是否确认付款'+money+'元？'
            }).then(function(yes){
                if(yes){
                    var billid=$scope.bill.id;
                    var payInfo={};
                    payInfo.billid=billid;
                    payInfo.phone_number=acct.phone_number;
                    payInfo.password=acct.password;
                    myhttp($http,$ionicPopup,$ionicLoading,server+'/football/payTraditionalBill',payInfo,function(data){
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
                    var delInfo={};
                    delInfo.phone_number=acct.phone_number;
                    delInfo.password=acct.password;
                    delInfo.billid=$scope.bill.id;
                    myhttp($http,$ionicPopup,$ionicLoading,server+'/football/delTraditionalBill',delInfo,function(data){
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
