var copa = angular.module('copaapp', ['ngRoute']);

var original_data = null;

function pie(selector, data) {
    $(selector).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                showInLegend: true,
                dataLabels: {
                    enabled: false,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            },
            series: {
                turboThreshold: 0
            }
        },
        legend: {
            layout: 'vertical',
            align: 'center',
            verticalAlign: 'bottom',
            backgroundColor: '#f3f3f3',
            borderWidth: 0,
            useHTML: true,
            labelFormatter: function () {
                return '<div style="width:400px;"><span style="float:left">' + this.name + '</span><span style="float:right">' + this.percentage.toFixed(0) + '%</span><span style="float:right; margin-right:15%">$' + Highcharts.numberFormat(this.y, 0) + '</span></div>';
                
            }

        },
        series: [{
            type: 'pie',
            name: '',
            data: data
        }]
    });
}

copa.controller('CopaController',
    function($scope, $http) {
        $scope.show_main = true;
        $scope.show_r1 = false;
        $scope.show_favo = false;
        $scope.init = function(route) {
            $("#li_main").addClass('active');
            $("#li_r1").removeClass('active');
            $("#li_favo").removeClass('active');
            $scope.show_r1 = false;
            $scope.show_main = true;
            $scope.show_favo = false;
            $http({
                url: '/data.json',
                method: 'GET'
            }).success(function(data, status, header, config) {
                $scope.total = data.total;
                $scope.total_sem_ref_lic = data.total_sem_ref_lic;
                $scope.total_com_ref_lic = data.total_com_ref_lic;
                $scope.percentual_dados_desconsiderados = data.percentual_dados_desconsiderados;
                $scope.atualizado = data.atualizado;
                $scope.total_contrapartida = data.total_contrapartida;
                d_total_sem_ref_lic = data.d_total_sem_ref_lic;
                d_total_com_ref_lic = data.d_total_com_ref_lic;
            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });
        };
        $scope.init();
    }
);

d_total_sem_ref_lic = null;
d_total_com_ref_lic = null;

copa.controller('R1Controller',
    function($scope, $http) {
        $scope.show_report_1 = function() {
            $("#li_r1").addClass('active');
            $("#li_main").removeClass('active');
            $("#li_favo").removeClass('active');
            $scope.show_r1 = true;
            $scope.show_main = false;
            $scope.show_favo = false;

            $http({
                url: '/data.json',
                method: 'GET'
            }).success(function(data, status, header, config) {
                $scope.total = data.total;
                $scope.total_sem_ref_lic = data.total_sem_ref_lic;
                $scope.total_com_ref_lic = data.total_com_ref_lic;
                $scope.percentual_dados_desconsiderados = data.percentual_dados_desconsiderados;
                $scope.atualizado = data.atualizado;
                $scope.total_contrapartida = data.total_contrapartida;
                d_total_sem_ref_lic = data.d_total_sem_ref_lic;
                d_total_com_ref_lic = data.d_total_com_ref_lic;
                data = [{"name":"Sem Ref. Licitação", "y": d_total_sem_ref_lic},
                        {"name":"Com Ref. Licitação", "y": d_total_com_ref_lic}];
                pie("#pizza1", data);
            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });

        };

        $scope.show_report_1();
});

copa.controller('R2Controller',
    function($scope, $http) {
        $scope.show_report_favo = function() {
            $("#li_favo").addClass('active');
            $("#li_r1").removeClass('active');
            $("#li_main").removeClass('active');
            $scope.show_r1 = false;
            $scope.show_main = false;
            $scope.show_favo = true;

            if (!original_data) { 
                $http({
                    url: '/data_favo.json',
                    method: 'GET'
                }).success(function(data, status, header, config) {
                    original_data = data;
                    data = _.filter(original_data, function(el) {
                        return el.y > 1000000000;
                    });

                    $scope.total_1_b = _.reduce(data,
                        function (x, w) {
                            return {y: x.y + w.y};
                        }, {y: 0}).y / 1000000000;

                    pie("#pizza2", data);
                    data = _.filter(original_data, function(el) {
                        return el.y > 500000000 && el.y < 1000000000;
                    });
                    pie("#pizza21", data);
                    $scope.M_data = _.sortBy(_.filter(original_data, function(el) {
                        return el.y > 100000000 && el.y < 500000000;
                    }), function(el) {return el.y; }).reverse();
                    $scope.m_data = _.sortBy(_.filter(original_data, function(el) {
                        return el.y > 10000000 && el.y < 100000000;
                    }), function(el) {return el.y; }).reverse();
                }).error(function(data, status, header, config) {
                    alert('API ERROR');
                });
            } else {
                data = _.filter(original_data, function(el) {
                    return el.y > 1000000000;
                });
                $scope.total_1_b = _.reduce(data,
                    function (x, w) {
                        return {y: x.y + w.y};
                    }, {y: 0}).y / 1000000000;

                pie("#pizza2", data);
                data = _.filter(original_data, function(el) {
                    return el.y > 500000000 && el.y < 1000000000;
                });
                pie("#pizza21", data);
                $scope.M_data = _.sortBy(_.filter(original_data, function(el) {
                    return el.y > 100000000 && el.y < 500000000;
                }), function(el) {return el.y; }).reverse();
                $scope.m_data = _.sortBy(_.filter(original_data, function(el) {
                    return el.y > 10000000 && el.y < 100000000;
                }), function(el) {return el.y; }).reverse();            
            }
        };
        $scope.show_report_favo();
});


copa.config(function ($routeProvider) {
    $routeProvider.when('/inicio', {templateUrl: 'inicio.html',
                                    controller: 'CopaController'})
                  .when('/ExecucaoXLicitacao', {templateUrl: 'r1.html',
                                    controller: 'R1Controller'})
                  .when('/Contratados', {templateUrl: 'r2.html',
                                    controller: 'R2Controller'})
                   .otherwise({redirectTo: '/inicio'});
});
