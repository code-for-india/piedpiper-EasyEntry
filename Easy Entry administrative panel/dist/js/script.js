function checkStatus(ticketID){
	$.ajax({
		url: "/api/status/"+ ticketID,
		success: function(data){
			updateStatus(ticketID, data);
		},
		error: function(){
			console.log("checkStatus failed");
		}
	});
}

function updateStatus(ticketID, data){
	var w = $("div[data-ticket='" + ticketID + "']")[0];
	if(w.data("status") == parseInt(data.status))
		return;

	if(data.status == -1){
		updatePanel(ticketID, -1);
	} else if(data.status == 0){
		updatePanel(ticketID, 0);
	} else if(data.status == 1)
		updatePanel(ticketID, 1);
}

function updatePanel(tID, status){
	var w = $("div[data-ticket='" + ticketID + "']")[0];
	$.ajax({
		url: "/api/data/" + ticketID,
		success: function(data){
			createPanel(ticketID, data, w);
		},
		error: function(){
			console.log("updatePanel failed");
		}
	});
}

function createPanel(ticketID, d, elem=null){
	var red = "", yellow="", green="",gicon="", ricon="", yicon="", ycolor="", rcolor="", ytext="", rtext="", gtext="";
	if(d.status == -1){
		yellow = "yellow";
		ycolor = 'style="color: #df8a13;"';
		ytext = 'Authenticating...';
	} else if(d.status == 1){
		red="red";
		ricon = "times";
		rcolor = 'style="color: #b52b27;"';
		rtext = "Intercepted!"
	} else if(d.status == 0){
		green = "green";
		gicon = "check";
		gtext = "Confirmed";
	}

	if(elem == null){

		elem = '<div class="col-lg-4" data-ticket="' + ticketID + '" data-status="' + d.status + '">\
                    <div class="panel panel-'+ red + green + yellow +'">\
                        <div class="panel-heading">\
                            T-#: ' + d.ticketID + '<i class="fa ffa-lg fa-' + gicon + ricon + yicon + 'circle-o pull-right"></i>\
                        </div>\
                        <div class="panel-body text-center">\
                                    <div class="profile-blog blog-border">\
                                <img class="rounded-x" src="' + d.image + '" alt=""><br /><br />\
                                <div class="name-location">\
                                    <strong>' + d.name + '</strong>\
                                    <span><i class="fa fa-map-marker"> </i> <a href="#">' + d.city + ',</a> <a href="#">' + d.country + '</a></span>\
                                </div>\
                                <div class="clearfix margin-bottom-20"></div>    \
                                <p><strong>Gender:</strong> ' + d.gender + '</p>\
                                <p><strong>Age:</strong> ' + d.age + '</p>\
                                <hr>\
                                <ul class="list-inline share-list">\
                                    <li><i class="fa fa-bell" ' + rcolor + ycolor + '></i>\
                                        <button type="button" class="btn btn-default">\
                                            <a href="#">' + rtext + ytext + gtext + '</a>\
                                        </button>\
                                    </li>\
                                </ul>\
                            </div>\
                        </div>\
                        <div class="panel-footer">\
                            ' + d.time + '\
                        </div>\
                    </div>\
                </div>';

        $("#list").html($("#list").html() + elem);

	} else {
		var str = '<div class="panel panel-'+ red + green + yellow +'">\
                        <div class="panel-heading">\
                            T-#: ' + d.ticketID + '<i class="fa ffa-lg fa-' + gicon + ricon + yicon + 'circle-o pull-right"></i>\
                        </div>\
                        <div class="panel-body text-center">\
                                    <div class="profile-blog blog-border">\
                                <img class="rounded-x" src="' + d.image + '" alt=""><br /><br />\
                                <div class="name-location">\
                                    <strong>' + d.name + '</strong>\
                                    <span><i class="fa fa-map-marker"> </i> <a href="#">' + d.city + ',</a> <a href="#">' + d.country + '</a></span>\
                                </div>\
                                <div class="clearfix margin-bottom-20"></div>    \
                                <p><strong>Gender:</strong> ' + d.gender + '</p>\
                                <p><strong>Age:</strong> ' + d.age + '</p>\
                                <hr>\
                                <ul class="list-inline share-list">\
                                    <li><i class="fa fa-bell" ' + rcolor + ycolor + '></i>\
                                        <button type="button" class="btn btn-default">\
                                            <a href="#">' + rtext + ytext + gtext + '</a>\
                                        </button>\
                                    </li>\
                                </ul>\
                            </div>\
                        </div>\
                        <div class="panel-footer">\
                            ' + d.time + '\
                        </div>\
                    </div>';

        elem.html(str);
        elem.data("success", d.success);
	}
}

function init(){

	$.ajax({
		url: "/api/getNewTicket",
		success: function(d){
			createPanel(d.ticketID, d.data, null);
		},
		error: function(){
			console.log("init error");
		}
	})

	window.setTimeout(function(){
		init();
	}, 1000);
}

$(document).ready(function(){
	init();
});