var copa = angular.module('copaapp', []);

copa.controller('CopaController',
    function($scope, $http, $interval, $location) {
        $scope.show_main = true;
        $scope.show_r1 = false;
        $scope.show_favo = false;

        $scope.show_report_favo = function() {
            $("#li_favo").addClass('active');
            $("#li_r1").removeClass('active');
            $("#li_main").removeClass('active');
            d3.select("#pizza2").selectAll("svg").remove();
            $scope.show_r1 = false;
            $scope.show_main = false;
            $scope.show_favo = true;

            $http({
                url: '/data_favo.json',
                method: 'GET'
            }).success(function(data, status, header, config) {
                var w = 600,                        //width
                h = 800,                            //height
                r = 300,                            //radius
                color = d3.scale.category20c();     //builtin range of colors

                var vis = d3.select("#pizza2")
                    .append("svg:svg")              //create the SVG element inside the <body>
                    .data([data])                   //associate our data with the document
                        .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
                        .attr("height", h)
                    .append("svg:g")                //make a group to hold our pie chart
                        .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius

                var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
                    .outerRadius(r);

                var pie = d3.layout.pie()           //this will create arc data for us given a list of values
                    .value(function(d) { return d.value; });    //we must tell it out to access the value of each element in our data array

                var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
                    .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
                    .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
                        .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
                            .attr("class", "slice");    //allow us to style things in the slices (like text)

                    arcs.append("svg:path")
                            .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
                            .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

                    arcs.append("svg:text")                                     //add a label to each slice
                            .attr("transform", function(d) {                    //set the label's origin to the center of the arc
                            //we have to make sure to set these before calling arc.centroid
                            d.innerRadius = 0;
                            d.outerRadius = r;
                            return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
                        })
                        .attr("text-anchor", "middle")                          //center the text on it's origin
                     .text(function(d, i) { return data[i].label; });
            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });

        };

        $scope.show_report_1 = function() {
            $("#li_r1").addClass('active');
            $("#li_main").removeClass('active');
            $("#li_favo").removeClass('active');
            d3.select("#pizza1").selectAll("svg").remove();
            $scope.show_r1 = true;
            $scope.show_main = false;
            $scope.show_favo = false;
            var w = 200,                        //width
            h = 300,                            //height
            r = 100,                            //radius
            color = d3.scale.category20c();     //builtin range of colors

            data = [{"label":"Sem Ref. Licitação", "value": $scope.d_total_sem_ref_lic},
                    {"label":"Com Ref. Licitação", "value": $scope.d_total_com_ref_lic}];

            var vis = d3.select("#pizza1")
                .append("svg:svg")              //create the SVG element inside the <body>
                .data([data])                   //associate our data with the document
                    .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
                    .attr("height", h)
                .append("svg:g")                //make a group to hold our pie chart
                    .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius

            var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
                .outerRadius(r);

            var pie = d3.layout.pie()           //this will create arc data for us given a list of values
                .value(function(d) { return d.value; });    //we must tell it out to access the value of each element in our data array

            var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
                .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
                .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
                    .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
                        .attr("class", "slice");    //allow us to style things in the slices (like text)

                arcs.append("svg:path")
                        .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
                        .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

                arcs.append("svg:text")                                     //add a label to each slice
                        .attr("transform", function(d) {                    //set the label's origin to the center of the arc
                        //we have to make sure to set these before calling arc.centroid
                        d.innerRadius = 0;
                        d.outerRadius = r;
                        return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
                    })
                    .attr("text-anchor", "middle")                          //center the text on it's origin
                    .text(function(d, i) { return data[i].label; });        //get the label from our original data array

        };

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
                $scope.d_total_sem_ref_lic = data.d_total_sem_ref_lic;
                $scope.d_total_com_ref_lic = data.d_total_com_ref_lic;
                $scope.atualizado = data.atualizado;

            }).error(function(data, status, header, config) {
                alert('API ERROR');
            });
        };

        $scope.init();
    }
);
