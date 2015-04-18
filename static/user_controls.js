

function callApi( event) {
	event.preventDefault();
	console.log('API func running');

	var zipcode = $('#territoryName').val();
	console.log(zipcode);

	  $.ajax('get_tariffs_by_zip', {
	    type: 'POST',
	    data: JSON.stringify(zipcode),
	    contentType: 'application/json',
	    success: function(data, status, result){
	    	console.log("ajax call worked!");
	      scenario_result = JSON.parse(result.responseText);
	      console.log(scenario_result);
	      $("#resultContainer").html(scenario_result)
	    }
	  });
}

$("#submitBtn").on('click', callApi);