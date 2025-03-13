/***********************************

This file contains some utility functions used by other parts of the application

***********************************/


// Execute an HTTP GET request
// May want to investigate if async execution is better and add error handling for a bad XMLHttpRequest
function xmlhttp_get(url) {
    var xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function() {
        if (this.readyState == 4) {
            responseData = JSON.parse(xhr.responseText.split(/(?=[$<])/)[0]);
        }
    };
    
    xhr.open('GET', url, false);
    xhr.send(null);

    return responseData;
}


// Execute an HTTP POST requuest
function xmlhttp_post(url, data) {
    var xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function() {
        if (this.readyState == 4) {
            responseData = this.responseText.split(/(?=[$<])/)[0];
        }
    };
    
    xhr.open('POST', url, false);
    xhr.send(data);

    return responseData;
}


//Populate modal form dropdowns ; requires: ('element name' & 'options Array')
function popSelectionElem(selectElem, optionsArr) {	
	//Clear current dropdown selection contents
	var i, L = selectElem.options.length - 1;
	for (i = L; i >= 0; i--) {
		selectElem.remove(i);
	}

	//Add a default blank option
	option = new Option("-", "-", true, true);
	option.setAttribute("disabled", true);
	selectElem.add(option);

	//Populate selection list within select element argument
    if(optionsArr) {
        arrLen = optionsArr.length;
        for (let i = 0; i < arrLen; i++) {
		    selectElem.add(new Option(optionsArr[i], optionsArr[i]));
        }
	}
};