angular.module('AppChat').controller('NewChatController', ['$http', '$log', '$scope', '$location', '$routeParams',
    function($http, $log, $scope, $location, $routeParams) {
        // This variable lets you access this controller
        // from within the callbacks of the $http object

        var thisCtrl = this;

        // This variable hold the information on the part
        // as read from the REST API

        this.newChat = function(){
            // Now create the url with the route to talk with the rest API
            var reqURL = "http://localhost:5000/ChatApp/chat";
            var cgid;
            console.log("reqURL: " + reqURL);
            // Now issue the http request to the rest API
            $http.post(reqURL, {
                'chatname': $scope.chatname
            }).then(
                // Success function
                function (response) {
                    console.log("data: " + JSON.stringify(response.data));
                    // assing the part details to the variable in the controller
                    cgid = response.data["Chat"]["cgid"]
                    reqURL = "http://localhost:5000/ChatApp/chat/" + cgid;
                    $http.post(reqURL, {
                        'cgid' : cgid
                    }).then(
                        // Success function
                        function (response) {
                            console.log("data: " + JSON.stringify(response.data));
                            // Passing the part details to the variable in the controller
                            $location.url('/chat/' + cgid);
                        }, //Error function
                        function (response) {
                            // This is the error function
                            // If we get here, some error occurred.
                            // Verify which was the cause and show an alert.
                            var status = response.status;
                            //console.log("Error: " + reqURL);
                            //alert("Cristo");
                            console.log(status)
                            if (status == 0) {
                                alert("No hay conexion a Internet");
                            }
                            else if (status == 400) {
                                alert(status.Error);
                            }
                            else if (status == 401) {
                                alert("Su sesion expiro. Conectese de nuevo.");
                            }
                            else if (status == 403) {
                                alert("No esta autorizado a usar el sistema.");
                            }
                            else if (status == 404) {
                                alert("No se encontro la informacion solicitada.");
                            }
                            else {
                                alert("Error interno del sistema.");
                            }
                        }
                    );
                }, //Error function
                function (response) {
                    // This is the error function
                    // If we get here, some error occurred.
                    // Verify which was the cause and show an alert.
                    var status = response.status;
                    //console.log("Error: " + reqURL);
                    //alert("Cristo");
                    console.log(status)
                    if (status == 0) {
                        alert("No hay conexion a Internet");
                    }
                    else if (status == 400) {
                        alert(status.Error);
                    }
                    else if (status == 401) {
                        alert("Su sesion expiro. Conectese de nuevo.");
                    }
                    else if (status == 403) {
                        alert("No esta autorizado a usar el sistema.");
                    }
                    else if (status == 404) {
                        alert("No se encontro la informacion solicitada.");
                    }
                    else {
                        alert("Error interno del sistema.");
                    }
                }
            );
        };
    }
]);