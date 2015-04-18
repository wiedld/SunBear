
function callApi( event ) {
	event.preventDefault();
	console.log("callApi is running");

// 	$("#submitBtn").('/get_zipcode_info');
// };

	  $.ajax('get_zipcode_info', {
	    type: 'GET',
	    data: "",
	    contentType: 'application/json',
	    success: function(data, status, result){
	    	console.log("ajax call worked!");
	      scenario_result = JSON.parse(result.responseText);
	      console.log(scenario_result);
	      $("#resultContainer").html(scenario_result)
	    }
	  });

$("#submitBtn").on('click', callApi);