/****************************
 * 
 * This file contains the JS code concerning modal functionality
 * 
****************************/



// Global variables
var ownerID;
var subModal;
var subModal_2;
var fieldName_MDL = "field";
var applicationName_MDL = "application";
var tankmixName_MDL = "tankmix";
var contFunct = false;
var saved = false;

var farmNameSel;
var fieldNameSel;

var productArr = new Array();
var productMix;

var editingApplication = false;
var backToEditing = false;
var editingApplicationID = -1;






/****************************************
 *  Buttons in the left menu 			*
****************************************/
//  Note: Clear all values before showing the modals!!!
//-- Add Farm Modal
// $("#addFarm").click(function() {
//     $("#addFarmModal").modal("show");
// });

//-- Add Field Modal
// $("#addField").click(function() {
//     $("#addFieldModal").modal("show");
// });

//-- Add Boundary Modal
// $("#addBoundary").click(function() {
//     $("#addBoundaryModal").modal("show");
// });

//-- Add Application Modal
$("#overall_body").on("click", "#addApplication", function() {
    $("#addApplicationModal").modal("show");
});


//-- pList Modal Close Button
// $(document).on("click", "#closePList_Modal", function() {
// 	$("#pListModal").modal("hide");
// });

//-- Update Modal Style
// $("#pListModal").on("shown.bs.modal",function() {
// 	//set element style and name 
// 	modal = document.getElementById('pListModal');
// 	modal.style="display: block; height: -webkit-fill-available;"
// });

//-- Update Modal Style
// $("#addProductMixModal").on("shown.bs.modal", function() {
// 	//set element style and  name 
// 	modal = document.getElementById('addProductMixModal');
// 	modal.style="max-height:100%; display: block; overflow:auto;"
// });









/****************************************
 *  Individual Modals					*
****************************************/

/*********** ADD FARM MODAL ***********/

// May rework loading functionality for all modals if async execution is used for HTTP requests
$("#addFarmModal").on("hide.bs.modal", function() {
	$('#addFarmModalLoading').fadeIn();
	resetFarmModal();
});


$("#addFarmModal").on("shown.bs.modal",function() {
	// Populate farm organization dropdown selection
	var url = '/getAllOrgNames';
	allOrgNames = xmlhttp_get(url);

	farmOrgSel = document.getElementById('farm_FarmOrg_Sel');
	popSelectionElem(farmOrgSel, allOrgNames);

	$('#addFarmModalLoading').fadeOut();
});	


function resetFarmModal() {
	// Clear input values
	document.getElementById('farm_FarmName_Input').value = "";
	document.getElementById('farm_FarmOrg_Sel').value = "-";
	document.getElementById('farm_FarmStatus_Sel').value = "-";

	// Clear alerts
	document.getElementById("farm_FarmName_Alert").innerHTML = "";
	document.getElementById("farm_FarmOrgSel_Alert").innerHTML = "";
	document.getElementById("farm_FarmStatusSel_Alert").innerHTML = "";
	document.getElementById("farm_FarmSave_Alert").innerHTML = "";
};


// Close farm modal button
$(document).on("click", "#closeFRM_Modal",function() {
	$("#addFarmModal").modal("hide");
	if(backToEditing) {
		editingApplication = true;
	}

	$("#addApplicationModal").modal("show");
});	



// Save farm modal Button
$(document).on("click","#saveFRM_Modal", function() {

	// Reset alerts to begin with
	document.getElementById("farm_FarmSave_Alert").innerHTML = "";
	document.getElementById("farm_FarmName_Alert").innerHTML = "";
	document.getElementById("farm_FarmStatusSel_Alert").innerHTML = "";

	// // Get inputs
	farmName = document.getElementById('farm_FarmName_Input').value;
	farmOrg = document.getElementById('farm_FarmOrg_Sel').value;
	farmStatus = document.getElementById('farm_FarmStatus_Sel').value;


	//Check for valid values
	contFunct = true;

	if(farmName.trim() == "") {
		document.getElementById("farm_FarmName_Alert").innerHTML = "* Farm Name Required";
		contFunct = false;
	}

	if(farmOrg == "-") {
		document.getElementById("farm_FarmOrgSel_Alert").innerHTML = "* Farm Organization Required";
		contFunct = false;
	} 

	if(farmStatus == "-") {
		document.getElementById("farm_FarmStatusSel_Alert").innerHTML = "* Farm Status Required";
		contFunct = false;
	} 

	//Check for valid input data values and continue to database input function
	if (contFunct == true) { 

		console.log("sending");

		//Send variable data to sql query and store new entry in the database
		var url = '/saveNewFarm'

		var data = new FormData();
		data.append("farmName", farmName);
		data.append("farmOrg", farmOrg);
		data.append("farmStatus", farmStatus);

		responseText = xmlhttp_post(url, data);
		console.log("responseText");
		console.log(responseText);

		if(responseText.toUpperCase().match('TRUE')) {
			document.getElementById("farm_FarmSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
			document.getElementById("farm_FarmSave_Alert").innerHTML = "Farm successfully added";
			console.log("Farm added");
		}
		else if(responseText.toUpperCase().match('FALSE')) {
			document.getElementById("farm_FarmSave_Alert").style.color = 'rgb(241,8,8)';

			if(responseText.toUpperCase().match('DUPLICATE')) {
				document.getElementById("farm_FarmSave_Alert").innerHTML = "Farm already exists in this organization";
			}
			else {
				document.getElementById("farm_FarmSave_Alert").innerHTML = "Failed to add farm";
			}
		}
	}
});





/*********** ADD FIELD MODAL ***********/
$("#addFieldModal").on("hide.bs.modal", function() {
	$('#addFieldModalLoading').fadeIn();

	$("#field_FieldSave_Alert").text("");
});


$("#addFieldModal").on("shown.bs.modal", function() {
	//Populate farm dropdown selection
	var url = '/getAllFarmNames'
	allFarmNames = xmlhttp_get(url);

	farmNameSel = document.getElementById('field_FarmName_Sel');
	popSelectionElem(farmNameSel, allFarmNames);

	$('#addFieldModalLoading').fadeOut();
});	

$(document).on("click", "#drawBoundarybtn", function() {
	$("#addFieldModal").modal("hide");
	subModal = fieldName_MDL;
	drawBoundary(); // defined in userMain_JS
});

// Upload Boundary Button
$(document).on("click", "#uploadBoundarybtn", function() {
	$("#addFieldModal").modal("hide");
	document.getElementById("fileDirLocation_tb").value = "";
	document.getElementById("uploadStatus_heading").innerHTML = "";
	$("#uploadBoundaryModal").modal("show");
});

// Browse Directory for file
$(document).on("click", "UpLd_uploadBound_btn", function() {
	//TODO: implement this function to access the file from browseDir_btn and read from it
});

// Close Add Boundary Modal Button
$(document).on("click", "#closeUploadBND_Modal", function() {
	$("#uploadBoundaryModal").modal("hide");
});

var field_geometry = null;
function finishedDrawing(geometry) {
	// console.log("finishDrawing");
	field_geometry = geometry;

	$('#drawBoundarybtn').css('display', 'none');
	$('#uploadBoundarybtn').css('display', 'none');
	$('#deleteBoundarybtn').css('display', '');


	$('#addField_boundary_alert').css('color', 'rgba(8, 75, 199, 0.808)');
	$('#addField_boundary_alert').text("Field Successfully Drawn");

	$('#addFieldModal').modal("show");
}


$(document).on("click", "#deleteBoundarybtn", function() {
	field_geometry = null;

	$('#drawBoundarybtn').css('display', '');
	$('#uploadBoundarybtn').css('display', '');
	$('#deleteBoundarybtn').css('display', 'none');

	$('#addField_boundary_alert').text("");
});



// Add farm button
// $(document).on("click", "#fieldAddFarmbtn", function() {
// 	$("#addFieldModal").modal("hide");
// 	subModal=fieldName_MDL;
// 	$("#addFarmModal").modal("show");
// });


//close field modal button
$(document).on("click", "#closeFLD_Modal", function() {
	$("#addFieldModal").modal("hide");

	if(backToEditing) {
		editingApplication = true;
	}

	if (subModal == applicationName_MDL) {
		$("#addApplicationModal").modal("show");
	}


	//clear input values
	document.getElementById('field_FarmName_Sel').value = "-";
	document.getElementById('field_FieldName_Input').value = "";
	document.getElementById("field_FieldSave_Alert").value = "";


	//clear alerts
	document.getElementById("field_FarmNameSel_Alert").innerHTML = "";
	document.getElementById("field_FieldName_Alert").innerHTML = "";
	document.getElementById("field_FieldSave_Alert").innerHTML = "";
});


//Save field modal Button
$(document).on("click", "#saveFLD_Modal", function() {
	farmName = document.getElementById('field_FarmName_Sel').value;
	fieldName = document.getElementById('field_FieldName_Input').value;

	contFunct = true;
	//check for valid values
	if(farmName == "-") {
		document.getElementById("field_FarmNameSel_Alert").innerHTML = "* Farm Name Required";
		contFunct = false;
	} else {
		document.getElementById("field_FarmNameSel_Alert").innerHTML = "";
	}	

	if(fieldName == "") {
		document.getElementById("field_FieldName_Alert").innerHTML = "* Field Name Required";
		contFunct = false;
	} else {
		document.getElementById("field_FieldName_Alert").innerHTML = "";
	}

	if(field_geometry == null) {
		$('#addField_boundary_alert').css('color', 'rgb(241,8,8)');
		$('#addField_boundary_alert').text("* Boundary Required");
		contFunc = false;
	}


	//check for valid input data values and continue to database input function
	if (contFunct == true) {
		// send variable data to sql query and store new entry in the database

		//Send variable data to sql query and store new entry in the database
		var url = '/saveNewField'

		var data = new FormData();
		data.append("farmName", farmName);
		data.append("fieldName", fieldName);
		data.append("geometry", JSON.stringify(field_geometry));

		responseText = xmlhttp_post(url, data);

		if(responseText.toUpperCase().match('TRUE')) {

			$('#drawBoundarybtn').css('display', '');
			$('#uploadBoundarybtn').css('display', '');
			$('#deleteBoundarybtn').css('display', 'none');
		
			$('#addField_boundary_alert').text("");

			document.getElementById("field_FieldSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
			document.getElementById("field_FieldSave_Alert").innerHTML = "Field successfully added";
			document.getElementById("field_FieldName_Input").value = "";

			document.getElementById("field_FieldName_Input").value = "";
			$("#deleteBoundarybtn").click();
		}
		else if(responseText.toUpperCase().match('FALSE')) {
			document.getElementById("field_FieldSave_Alert").style.color = 'rgb(241,8,8)';

			if(responseText.toUpperCase().match('DUPLICATE')) {
				document.getElementById("field_FieldSave_Alert").innerHTML = "Field name already exists on this farm";
			}
			else {
				document.getElementById("field_FieldSave_Alert").innerHTML = "Failed to add field";
			}
		}
	}
});










// Populate add field drop down based on farm selection
$("#app_FarmName_Sel").change( function() {
	//Get selected farm name
	farmNameSel = document.getElementById('app_FarmName_Sel');
	farmName = farmNameSel.options[farmNameSel.selectedIndex].text

	//Populate field dropdown selection
	fieldNameSel = document.getElementById('app_FieldName_Sel');
	var url = '/getAllFieldNames?farmName=' + farmName;
	allFieldNames = xmlhttp_get(url);

	popSelectionElem(fieldNameSel, allFieldNames);
});





//-- Add/Edit Application Modal




//TODO: look into removing if async execution is used
$("#addApplicationModal").on("hide.bs.modal", function() {
	$('#addApplicationModalLoading').fadeIn();


	resetAppModal();
	document.getElementById("ApplicationSave_Alert").innerHTML = "";

	$('#deleteApp_btn').hide();
	editingApplication = false;
});

$("#addApplicationModal").on("shown.bs.modal", function() {
	//Populate farm dropdown selection
	farmNameSel = document.getElementById('app_FarmName_Sel');
	var url = '/getAllFarmNames';
	allFarmNames = xmlhttp_get(url);

	popSelectionElem(farmNameSel, allFarmNames);


	//Populate applicator dropdown selection
	applicatorNameSel = document.getElementById('app_Applicator_Sel');
	var url = '/getAllApplicatorNames';
	allApplicatorNames = xmlhttp_get(url);

	popSelectionElem(applicatorNameSel, allApplicatorNames);


	//Populate tank mix dropdown selection
	tankMixSel = document.getElementById('app_TankMix_Sel');
	var url = '/getAllTankMixNames';
	allTankMixNames = xmlhttp_get(url);

	popSelectionElem(tankMixSel, allTankMixNames);


	if(editingApplication) {

		$('#deleteApp_btn').show();

		var url = '/getApplicationDetailsByID?appID=' + editingApplicationID;
		applicationDetailsWrapper = xmlhttp_get(url);
		applicationDetails = applicationDetailsWrapper[0];

		
		farmName = applicationDetails[0];
		fieldName = applicationDetails[1];
		applicatorString = applicationDetails[2];

		dateTimeString = applicationDetails[3];
		dateTime = dateTimeString.split('T');
		date = dateTime[0];
		time = dateTime[1].slice(0, -3);

		tankMixName = applicationDetails[4];
		appType = applicationDetails[5];
		equipmentName = applicationDetails[6];


		$("#app_FarmName_Sel").val(farmName).change();
		$("#app_FieldName_Sel").val(fieldName);

		$("#app_Applicator_Sel").val(applicatorString);


		$("#app_Date_Input").val(date);
		$("#app_Time_Input").val(time);

		$("#app_TankMix_Sel").val(tankMixName);
		$("#app_AppType_Sel").val(appType);
		$("#app_EquipName_Input").val(equipmentName);

	}



	$('#addApplicationModalLoading').fadeOut();
});




//Add farm button
$(document).on("click", "#appAddFarmbtn", function() {
	if(editingApplication) {
		backToEditing = true;
	}

	$("#addApplicationModal").modal("hide");
	subModal = applicationName_MDL;
	$("#addFarmModal").modal("show");
});    

//Add field button
$(document).on("click", "#addFieldbtn", function() {
	if(editingApplication) {
		backToEditing = true;
	}

	$("#addApplicationModal").modal("hide");
	subModal = applicationName_MDL;
	$("#addFieldModal").modal("show");
});    


//Add applicator button
$(document).on("click", "#addApplicatorbtn", function() {
	if(editingApplication) {
		backToEditing = true;
	}

	$("#addApplicationModal").modal("hide");
	subModal = applicationName_MDL;
	$("#addApplicatorModal").modal("show");
});

//Add tankmix button
$(document).on("click", "#addTankMixbtn", function() {
	if(editingApplication) {
		backToEditing = true;
	}

	$("#addApplicationModal").modal("hide");
	subModal = applicationName_MDL;
	$("#addTankMixModal").modal("show");
});    




//Close application modal button
$(document).on("click", "#closeAPP_Modal", function() {
	$("#addApplicationModal").modal("hide");
	resetAppModal();
});

$(document).on("click", "#closeAPPWithX_Modal", function() {
	$("#addApplicationModal").modal("hide");
	resetAppModal();
});

function resetAppModal() {
	//clear input values
	document.getElementById('app_FarmName_Sel').value = "-";
	document.getElementById('app_FieldName_Sel').value = "-";
	document.getElementById('app_Applicator_Sel').value = "-";
	document.getElementById('app_Date_Input').value = "";
	document.getElementById('app_Time_Input').value = "";
	document.getElementById('app_TankMix_Sel').value = "-";
	document.getElementById('app_AppType_Sel').value = "-";
	document.getElementById('app_EquipName_Input').value = "";


	//clear alerts
	document.getElementById("app_FarmNameSel_Alert").innerHTML = "";
	document.getElementById("app_FieldNameSel_Alert").innerHTML = "";
	document.getElementById("app_ApplicatorSel_Alert").innerHTML = "";
	document.getElementById("app_Date_Alert").innerHTML = "";
	document.getElementById("app_Date_Schedule_Alert").innerHTML = "";
	document.getElementById("app_Time_Alert").innerHTML = "";
	document.getElementById("app_TankMixSel_Alert").innerHTML = "";
	document.getElementById("app_AppTypeSel_Alert").innerHTML = "";
	document.getElementById("app_EquipName_Alert").innerHTML = "";
	document.getElementById("ApplicationSave_Alert").innerHTML = "";
}



$("#app_Date_Input").change(function() {
	var yearMonthDay = $(this).val().split("-");
	var inputDate = new Date(yearMonthDay[0], yearMonthDay[1] - 1, yearMonthDay[2]); //Javascript months are 0-11 indexed so minus 1

	var today = new Date();
	today.setHours(0, 0, 0, 0);


	if(inputDate > today) {
		$("#app_Time_Input").val("17:00"); //Default assume 5:00 PM if future date is entered, disabling time input
		document.getElementById("app_Date_Schedule_Alert").innerHTML = "This is a scheduled application";
	}
	else{
		document.getElementById("app_Date_Schedule_Alert").innerHTML = "";
		$("#app_Time_Input").removeAttr('disabled');
		console.log($("#app_Time_Input").val());
	}
});







$('#Map_Div').on('click', '.edit-application', function() {
	id = $(this).attr('id');
	id_number = id.split('_')[1];

	editingApplicationID = id_number;
	editingApplication = true;

	$('#addApplicationModal').modal('show');
});


//Delete application button
$(document).on("click","#deleteApp_btn", function() {

	if(confirm("Delete this application?")) {
		if(editingApplication) {
			url = "/deleteApplication";
	
			var data = new FormData();
			data.append("appID", editingApplicationID);
	
			responseText = xmlhttp_post(url, data);
	
			if(responseText.toUpperCase().match('TRUE')) {
				resetAppModal();
	
				document.getElementById("ApplicationSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Application deleted successfully";
	
				updateLeftMenuAndMap();
	
			}
			else if(responseText.toUpperCase().match('FALSE')) {
				document.getElementById("ApplicationSave_Alert").style.color = 'rgb(241,8,8)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Failed to delete application";
			}
		}
		else {
			document.getElementById("ApplicationSave_Alert").style.color = 'rgb(241,8,8)';
			document.getElementById("ApplicationSave_Alert").innerHTML = "Something went wrong, editing flag was not set";
		}
	}

});




//Save application modal Button
$(document).on("click","#saveAPP_Modal", function() {
	farmName = document.getElementById('app_FarmName_Sel').value;
	fieldName = document.getElementById('app_FieldName_Sel').value;
	applicator = document.getElementById('app_Applicator_Sel').value;
	date = document.getElementById('app_Date_Input').value;

	endTimeElement = document.getElementById('app_Time_Input');
	endTime = endTimeElement.value;

	tankMixName = document.getElementById('app_TankMix_Sel').value;
	appType = document.getElementById('app_AppType_Sel').value;
	equipName = document.getElementById('app_EquipName_Input').value;

	console.log(appType);
	console.log(equipName);
	
	//check for valid values
	if(farmName == "-") {
		document.getElementById("app_FarmNameSel_Alert").innerHTML = "* Farm Name Required";
		contFunct = false;
	} else {
		document.getElementById("app_FarmNameSel_Alert").innerHTML = "";
		contFunct = true;
	}	
	
	if(fieldName == "-") {
		document.getElementById("app_FieldNameSel_Alert").innerHTML = "* Field Name Required";
		contFunct = false;
	} else {
		document.getElementById("app_FieldNameSel_Alert").innerHTML = "";
		contFunct = true;
	}
	
	if(applicator == "-") {
		document.getElementById("app_ApplicatorSel_Alert").innerHTML = "* Applicator Required";
		contFunct = false;
	} else {
		document.getElementById("app_ApplicatorSel_Alert").innerHTML = "";
		contFunct = true;
	}
	
	if(date == "") {
		document.getElementById("app_Date_Alert").innerHTML = "* Date Required";
		contFunct = false;
	} else {
		document.getElementById("app_Date_Alert").innerHTML = "";
		contFunct = true;
	}

	if(endTime == "") {
		document.getElementById("app_Time_Alert").innerHTML = "* Time Required";
		contFunct = false;
	} else {
		document.getElementById("app_Time_Alert").innerHTML = "";
		contFunct = true;
	}
	
	if(tankMixName == "-") {
		document.getElementById("app_TankMixSel_Alert").innerHTML = "* TankMix Required";
		contFunct = false;
	} else {
		document.getElementById("app_TankMixSel_Alert").innerHTML = "";
		contFunct = true;
	}
	
	if(appType == "-") {
		document.getElementById("app_AppTypeSel_Alert").innerHTML = "* Application Type Required";
		contFunct = false;
	} else {
		document.getElementById("app_AppTypeSel_Alert").innerHTML = "";
		contFunct = true;
	}
	
	if(equipName.trim() == "") {
		document.getElementById("app_EquipName_Alert").innerHTML = "* Equipment Required";
		contFunct = false;
	} else {
		document.getElementById("app_EquipName_Alert").innerHTML = "";
		contFunct = true;
	}
	//check for valid input data values and continue to database input function
	if (contFunct == true) {
		// send variable data to sql query and store new entry in the database


		if(editingApplication) {
			url = "/editApplication";

			var data = new FormData();
			data.append("appID", editingApplicationID);
			data.append("farmName", farmName);
			data.append("fieldName", fieldName);
			data.append("applicator", applicator);
			data.append("date", date);
			data.append("endTime", endTime);
			data.append("tankMixName", tankMixName);
			data.append("appType", appType);
			data.append("equipmentName", equipName);

			responseText = xmlhttp_post(url, data);
	
			if(responseText.toUpperCase().match('TRUE')) {
	
				document.getElementById("ApplicationSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Application edited successfully";
			
				updateLeftMenuAndMap();
	
			}
			else if(responseText.toUpperCase().match('FALSE')) {
				document.getElementById("ApplicationSave_Alert").style.color = 'rgb(241,8,8)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Failed to edit application";
			}

			
		}
		else {
			url = "/saveNewApplication";

			var data = new FormData();
			data.append("farmName", farmName);
			data.append("fieldName", fieldName);
			data.append("applicator", applicator);
			data.append("date", date);
			data.append("endTime", endTime);
			data.append("tankMixName", tankMixName);
			data.append("appType", appType);
			data.append("equipmentName", equipName);
	
			responseText = xmlhttp_post(url, data);
	
			if(responseText.toUpperCase().match('TRUE')) {
	
				document.getElementById("ApplicationSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Application added successfully";
			
				updateLeftMenuAndMap();
	
			}
			else if(responseText.toUpperCase().match('FALSE')) {
				document.getElementById("ApplicationSave_Alert").style.color = 'rgb(241,8,8)';
				document.getElementById("ApplicationSave_Alert").innerHTML = "Failed to add application";
			}

			// console.log(farmName);
			// console.log(fieldName);
			// console.log(applicator);
			// console.log(date);
			// console.log(endTime);
			// console.log(tankMixName);
			// console.log(appType);
			// console.log(equipName);
		}
	}
});


function updateLeftMenuAndMap() {
	var url = '/getAppJson'
	appFeatures = xmlhttp_get(url);

	refreshLeftMenu();

	//Center extent
	latCntr = 41.177;
	lonCntr = -96.47;
	zoomLvlCntr = 17;
	leafletMap_Setup(latCntr, lonCntr, zoomLvlCntr);
}



//-- Add Applicator Modal

$("#addApplicatorModal").on("hide.bs.modal", function() {
	$('#addApplicatorModalLoading').fadeIn();
	document.getElementById("applicator_ApplicatorSave_Alert").innerHTML = "";
});



$("#addApplicatorModal").on("shown.bs.modal", function() {
	//Populate organization dropdown selection
	applicatorOrgSel = document.getElementById('applicator_OrgName_Sel');
	var url = '/getAllOrgNames';
	allOrgNames = xmlhttp_get(url);

	popSelectionElem(applicatorOrgSel, allOrgNames);

	$('#addApplicatorModalLoading').fadeOut();
});



//close applicator modal button
$(document).on("click","#closeAPC_Modal", function() {
	$("#addApplicatorModal").modal("hide");

	if(backToEditing) {
		editingApplication = true;
	}

	if (subModal == applicationName_MDL) {
		$("#addApplicationModal").modal("show");
	}
	//clear input values
	// document.getElementById('apc_ApplicatorID_Input').value = "";
	document.getElementById('apc_FirstName_Input').value = "";
	document.getElementById('apc_LastName_Input').value = "";
	// document.getElementById('apc_LicenseType_Sel').value = "-";
	// document.getElementById('apc_LicenseCat_Sel').value = "-";
	// document.getElementById('apc_LicenseExp_Input').value = "";
	//clear alerts
	// document.getElementById("apc_ApplicatorID_Alert").innerHTML = "";
	document.getElementById("apc_FirstName_Alert").innerHTML = "";
	document.getElementById("apc_LastName_Alert").innerHTML = "";
	// document.getElementById("apc_LicenseTypeSel_Alert").innerHTML = "";
	// document.getElementById("apc_LicenseCatSel_Alert").innerHTML = "";
	// document.getElementById("apc_LicenseExp_Alert").innerHTML = "";
});



//Save applicator modal Button
$(document).on("click", "#saveAPC_Modal", function() {
		
	//Initialize variables
	firstName = document.getElementById('apc_FirstName_Input').value;
	lastName = document.getElementById('apc_LastName_Input').value;
	orgName = document.getElementById('applicator_OrgName_Sel').value;

	
	//check for valid values

	contFunct = true;
	if(firstName.trim() == "") {
		document.getElementById("apc_FirstName_Alert").innerHTML = "* First Name Required";
		contFunct = false;
	}

	if(lastName.trim() == "") {
		document.getElementById("apc_LastName_Alert").innerHTML = "* Last Name Required";
		contFunct = false;
	}


	if(orgName == "-") {
		document.getElementById("apc_OrgName_Alert").innerHTML = "* Organization Name Required";
		contFunct = false;
	}


	//check for valid input data values and continue to database input function
	if (contFunct == true) {
		//Send variable data to sql query and store new entry in the database
		document.getElementById("applicator_ApplicatorSave_Alert").innerHTML = "";
		
		var url = '/saveNewApplicator'

		var data = new FormData();
		data.append("firstName", firstName);
		data.append("lastName", lastName);
		data.append("orgName", orgName);

		responseText = xmlhttp_post(url, data);

		if(responseText.toUpperCase().match('TRUE')) {

			document.getElementById("applicator_ApplicatorSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
			document.getElementById("applicator_ApplicatorSave_Alert").innerHTML = "Applicator added successfully";

			document.getElementById('apc_FirstName_Input').value = "";
			document.getElementById('apc_LastName_Input').value = "";
		}
		else if(responseText.toUpperCase().match('FALSE')) {
			document.getElementById("applicator_ApplicatorSave_Alert").style.color = 'rgb(241,8,8)';

			if(responseText.toUpperCase().match('DUPLICATE')) {
				document.getElementById("applicator_ApplicatorSave_Alert").innerHTML = "Applicator already exists in this organization";
			}
			else {
				document.getElementById("applicator_ApplicatorSave_Alert").innerHTML = "Failed to add applicator";
			}
		}
	}
});



//-- Add TankMix Modal
newTankMixProducts = {};

$("#addTankMixModal").on("hide.bs.modal",function() {

	document.getElementById('tm_TankMixName_Input').value = "";
	document.getElementById('tm_Carrier_Sel').value = "";
	document.getElementById('tm_CarrierRate_Input').value = "";
	document.getElementById('tm_CarrierUnits_Sel').value = "";

	document.getElementById('tm_productMix_List').innerHTML = "";
	document.getElementById("tankMixSave_Alert").innerHTML = "";


	$('#addTankMixModalLoading').fadeIn();
});


$("#addTankMixModal").on("shown.bs.modal",function() {
	//Populate dropdowns and load modal

	carrierSel = document.getElementById('tm_Carrier_Sel');
	var url = '/getAllCarrierNames';
	allCarrierNames = xmlhttp_get(url);

	popSelectionElem(carrierSel, allCarrierNames);

	$('#addTankMixModalLoading').fadeOut();
});






//Add products button
$(document).on("click","#addMixProductBtn", function() {
	// $("#addTankMixModal").modal("hide");
	// subModal_2=tankmixName_MDL;
	$("#addProductToTankMixModal").modal("show");
});

//Close tankmix modal button
$(document).on("click","#closeTM_Modal",function() {
	$("#addTankMixModal").modal("hide");

	if(backToEditing) {
		editingApplication = true;
	}

	if (subModal == applicationName_MDL) {
		$("#addApplicationModal").modal("show");
	}

	//Clear input values
	document.getElementById('tm_TankMixName_Input').value = "";
	document.getElementById('tm_Carrier_Sel').value = "-";
	document.getElementById('tm_CarrierRate_Input').value = "";
	document.getElementById('tm_CarrierUnits_Sel').value = "-";

	//Clear alerts
	document.getElementById("tm_TankMixName_Alert").innerHTML = "";
	document.getElementById("tm_CarrierSel_Alert").innerHTML = "";
	document.getElementById("tm_CarrierRate_Alert").innerHTML = "";
	document.getElementById("tm_CarrierUnitsSel_Alert").innerHTML = "";
	document.getElementById("tm_ProductMixList_Alert").innerHTML = "";


});

//Save tankmix modal Button
$(document).on("click", "#saveTM_Modal", function() {
	//Declare variables
	var tankMixName
	var carrierName
	var carrierRate
	var carrierUnits

	//Initialize variables	
	tankMixName = document.getElementById('tm_TankMixName_Input').value;
	carrierName = document.getElementById('tm_Carrier_Sel').value;
	carrierRate = document.getElementById('tm_CarrierRate_Input').value;
	carrierUnits = document.getElementById('tm_CarrierUnits_Sel').value;
	
	//Check for valid values
	if(tankMixName == "") {
		document.getElementById("tm_TankMixName_Alert").innerHTML = "* TankMix Name Required";
		contFunct = false;
	} else {
		document.getElementById("tm_TankMixName_Alert").innerHTML = "";
		contFunct = true;
	}	

	if(carrierName == "-") {
		document.getElementById("tm_CarrierSel_Alert").innerHTML = "* Carrier Required";
		contFunct = false;
	} else {
		document.getElementById("tm_CarrierSel_Alert").innerHTML = "";
		contFunct = true;
	}

	if(carrierRate == "" || carrierRate == 0) {
		document.getElementById("tm_CarrierRate_Alert").innerHTML = "* Non-Zero Carrier Rate Required";
		contFunct = false;
	} else {
		document.getElementById("tm_CarrierRate_Alert").innerHTML = "";
		contFunct = true;
	}

	if(carrierUnits == "-") {
		document.getElementById("tm_CarrierUnitsSel_Alert").innerHTML = "* Carrier Units Required";
		contFunct = false;
	} else {
		document.getElementById("tm_CarrierUnitsSel_Alert").innerHTML = "";
		contFunct = true;
	}


	if(Object.keys(newTankMixProducts).length == 0) {
		document.getElementById("tm_ProductMixList_Alert").innerHTML = "* Product(s) Required";
		contFunct = false;
	} else {
		document.getElementById("tm_ProductMixList_Alert").innerHTML = "";
		contFunct = true;
	}


	//Check for valid input data values and continue to database input function
	if (contFunct == true) {

		//Send variable data to sql query and store new entry in the database
		document.getElementById("tankMixSave_Alert").innerHTML = "";
		
		var url = '/saveNewTankMix'

		var data = new FormData();
		data.append("tankMixName", tankMixName);
		data.append("carrierName", carrierName);
		data.append("carrierRate", carrierRate);
		data.append("carrierUnits", carrierUnits);
		data.append("productDetails", JSON.stringify(newTankMixProducts));

		console.log(newTankMixProducts);


		responseText = xmlhttp_post(url, data);

		if(responseText.toUpperCase().match('TRUE')) {

			newTankMixProducts = {};

			document.getElementById("tankMixSave_Alert").style.color = 'rgba(8, 75, 199, 0.808)';
			document.getElementById("tankMixSave_Alert").innerHTML = "Tank Mix added successfully";


			document.getElementById('tm_TankMixName_Input').value = "";
			document.getElementById('tm_Carrier_Sel').value = "-";
			document.getElementById('tm_CarrierRate_Input').value = "";
			document.getElementById('tm_CarrierUnits_Sel').value = "-";
			document.getElementById('tm_productMix_List').innerHTML = "";
		}
		else if(responseText.toUpperCase().match('FALSE')) {
			document.getElementById("tankMixSave_Alert").style.color = 'rgb(241,8,8)';

			if(responseText.toUpperCase().match('DUPLICATE')) {
				document.getElementById("tankMixSave_Alert").innerHTML = "Tank Mix name already exists";
			}
			else {
				document.getElementById("tankMixSave_Alert").innerHTML = "Failed to add tank mix";
			}
		}
	}
});




//-- Add Product To Tank Mix Modal

productsCreated = 0;
editingProduct = false;
editingProductNumber = -1;


$("#addProductToTankMixModal").on("hide.bs.modal", function() {
	//Clear Alerts
	document.getElementById("pm_ProductSel_Alert").innerHTML = "";
	document.getElementById("pm_ProductRate_Alert").innerHTML = "";
	document.getElementById("pm_ProductRateUnitsSel_Alert").innerHTML = "";

	//Clear inputs
	selectedProduct = "-";
	$('#prdContainer').find('.selectized').each(function(index, element) { 
		element.selectize && element.selectize.clear();
	})
	document.getElementById('pm_Product_Sel').value = "-";
	document.getElementById('addProductToTankMixProductRate_Input').value = "";
	document.getElementById('addProductToTankMixRateUnits_Sel').value = "-";

	$('#addProductToTankMixLoading').fadeIn();

	editingProduct = false;
});

$("#addProductToTankMixModal").on("shown.bs.modal", function() {
	
	productSel = document.getElementById('pm_Product_Sel');
	url = "/getAllProductNames";
	allProductNames = xmlhttp_get(url);

	popSelectionElem(productSel, allProductNames);

	var $select = $('#pm_Product_Sel').selectize();
	var selectize = $select[0].selectize;

	if(editingProduct) {
		oldDetails = newTankMixProducts[editingProductNumber];

		productName = oldDetails[0];
		rate = oldDetails[1];
		units = oldDetails[2];

		selectize.setValue(productName, false);
		document.getElementById("addProductToTankMixProductRate_Input").value = rate;
		document.getElementById("addProductToTankMixRateUnits_Sel").value = units;
	}


	$('#addProductToTankMixLoading').fadeOut();
});

//Close button
$(document).on("click", "#closePrd_Modal",function() {
	if(saved == false) {
		if(confirm("Close without saving your Product?")) {
			closePrdModal.call();
		} else {
			console.log("do nothing");
		}
	} else {
		closePrdModal.call();
	}
});

//Save Button
$(document).on("click", "#saveProduct_Modal", function() {

	productName = document.getElementById('pm_Product_Sel').value;
	rate = document.getElementById('addProductToTankMixProductRate_Input').value;
	units = document.getElementById('addProductToTankMixRateUnits_Sel').value;

	contFunct = true;
	if(productName.trim() == "" || productName == "-") {
		document.getElementById("pm_ProductSel_Alert").innerHTML = "* Product Name Required";
		contFunct = false;
	}

	if(rate == "" || rate == 0) {
		document.getElementById("pm_ProductRate_Alert").innerHTML = "* Non-Zero Rate Required";
		contFunct = false;
	}

	if(units == "-") {
		document.getElementById("pm_ProductRateUnitsSel_Alert").innerHTML = "* Units Required";
		contFunct = false;
	}

	if(contFunct == true) {

		if(editingProduct) {
			editProductInTankMix(editingProductNumber, productName, rate, units);
		}
		else {
			productsCreated += 1;
			addProductToTankMix(productsCreated, productName, rate, units);
		}

		document.getElementById("tm_ProductMixList_Alert").innerHTML = "";
		$("#addProductToTankMixModal").modal("hide");
	}
});


//Close button
$(document).on("click", "#closeProduct_Modal", function() {
	if(confirm("Close without saving your Product?")) {
		$("#addProductToTankMixModal").modal("hide");
	}
});




function editProductInTankMix(editingProductNumber, productName, rate, units) {
	newTankMixProducts[editingProductNumber] = [productName, rate, units];

	id = "productDetails_" + editingProductNumber;
	document.getElementById(id).innerHTML = productName + ", " + rate + " " + units;

	console.log(newTankMixProducts);
};



function addProductToTankMix(productsCreated, productName, rate, units) {

	//Create list item container with div inside
	count = productsCreated

	id = "li_" + count;
	listItemContainer = document.createElement('li');
	listItemContainer.id = id;


	id = "product_" + count;
	innerDiv = document.createElement('div');
	innerDiv.id = id;
	innerDiv.style = "display: table-row";

	listItemContainer.appendChild(innerDiv);



	//Create Product Details div
	id = "productDetails_" + count;
	productDetailsDiv = document.createElement('div');
	productDetailsDiv.id = id;
	productDetailsDiv.style = "display: table-cell"
	productDetailsDiv.innerHTML = productName + ", " + rate + " " + units;

	innerDiv.appendChild(productDetailsDiv)



	//Create parent div for edit and delete button
	id = "edit_delete_div_" + count;
	editDeleteDiv = document.createElement('div');
	editDeleteDiv.id = id;
	editDeleteDiv.style = "display:flex;";
	innerDiv.appendChild(editDeleteDiv);


	//Create Edit button group
	id = "editProductBtn_" + count;
	editButton = document.createElement('button');
	editButton.id = id;
	editButton.className = "btn btn-primary edit-product";
	editButton.type = "button";
	editButton.style = "margin-bottom: 5px; display:flex;";

	editButton.innerHTML = '<i class="fa fa-edit" style="color: rgb(62, 65, 61);margin-left: 0px;padding-right: 5px;padding-top: 5px;"></i>Edit'

	editDeleteDiv.appendChild(editButton);


	//Create Delete button group
	id = "deleteProductBtn_" + count;
	deleteButton = document.createElement('button');
	deleteButton.id = id;
	deleteButton.className = "btn btn-primary delete-product";
	deleteButton.type = "button";
	deleteButton.style = "margin-bottom: 5px; display:flex;";

	deleteButton.innerHTML = '<i class="fa fa-minus" style="color: red; margin-left: 0px;padding-right: 5px;padding-top: 5px;"></i>Delete'

	editDeleteDiv.appendChild(deleteButton);

	
	//Append to list
	document.getElementById('tm_productMix_List').appendChild(listItemContainer);

	//Add product to temporary new tank mix dictionary
	newTankMixProducts[productsCreated] = [productName, rate, units];
};


$('#tm_productMix_List').on('click', '.edit-product', function() {

	console.log("edit clicked");

	id = $(this).attr('id');
	id_number = id.split('_')[1];

	editingProductNumber = id_number;
	editingProduct = true;


	$("#addProductToTankMixModal").modal("show");
});


$('#tm_productMix_List').on('click', '.delete-product', function() {

	console.log("delete clicked");

	id = $(this).attr('id');
	id_number = id.split('_')[1];
	listItemID = "#li_" + id_number;

	$(listItemID).remove();
	delete newTankMixProducts[id_number];
});



//-- Add Product Mix Modal
// $("#addProductMixModal").on("shown.bs.modal", function() {
// 	productArr = new Array();

// 	//Remove product container
//     if(document.getElementById('prdContainer_0')!=null) {
//         oldCont = document.getElementById('prdContainer_0');
//         oldCont.remove();
//     }

// 	//Call add product function and pass array
// 	productArr = addMixPrdBtn.call();

// 	//console.log(productArr.length);
// });   

// //Add additional product button
// $(document).on("click", "#addMixPrdbtn", function() {
// 	//Call add product container button function
// 	productArr = addMixPrdBtn.call();
// });  

// //Remove product buttons

// //Close button
// $(document).on("click", "#closePM_Modal", function() {
// 	if(saved == false) {
// 		if(confirm("Close without saving your Product Mix?")) {
// 			closePrdMix.call();
// 		}else{
// 			console.log("do nothing");
// 		}
// 	} else {
// 		closePrdMix.call();
// 	}
// });

// //Save Button
// $(document).on("click","#savePM_Modal",function() {
// 	savePrdMix().call();
// });













//-- Add Product Modal
// $("#addProductModal").on("shown.bs.modal", function() {

// });

// //Close button
// $(document).on("click", "#closePrd_Modal",function() {
// 	if(saved == false) {
// 		if(confirm("Close without saving your Product?")) {
// 			closePrdModal.call();
// 		}else{
// 			console.log("do nothing");
// 		}
// 	} else {
// 		closePrdModal.call();
// 	}
// });

// //Save Button
// $(document).on("click", "#savePrd_Modal", function() {
// 	savePrdModal().call();
// });


//Large Code Sets Dedicated to the 'Product Mix' Modal
//save chemical mixture from product mix modal
function savePrdMix() {
	//declare variables
    var i;
	var productElem;
    var rateElem;
    var unitElem;
    var productName;
    var productRate;
    var productUnits;
	var productAlert;
	var rateAlert;
	var unitAlert;
    
	//loop through product array to check/set alerts and write user inputs to a product mix string   
    for (i = 1; i <= productArr.length; i++) {
        productElem = "pm_Product_Sel_".concat(i);
        rateElem =  "pm_ProductRate_Input_".concat(i);
        unitElem = "pm_ProductRateUnits_Sel_".concat(i);

        //check for valid values
		productName = document.getElementById(productElem).value;
		productRate = document.getElementById(rateElem).value;
		productUnits = document.getElementById(unitElem).value;
        productAlert = "pm_ProductSel_Alert_".concat(i);
		rateAlert = "pm_ProductRate_Alert_".concat(i);
		unitAlert = "pm_ProductRateUnitsSel_Alert_".concat(i);
		//assume user has everything filled in and then check
		contFunct = true;
		if(productName == "-") {
			document.getElementById(productAlert).innerHTML = "* Product Required";
            contFunct = false;
        } else {
			document.getElementById(productAlert).innerHTML = "";
        }	
        if(productRate == "") {
            document.getElementById(rateAlert).innerHTML = "* Product Rate Required";
            contFunct = false;
        } else {
            document.getElementById(rateAlert).innerHTML = "";
        }
        if(productUnits == "-") {
            document.getElementById(unitAlert).innerHTML = "* Product Units Required";
            contFunct = false;
        } else {
            document.getElementById(unitAlert).innerHTML = "";
        }
        //check for valid input data values and continue to database input function
        if (contFunct == true) {
            // set variable data and send to sql query and store new entry in the database
			if(productMix == undefined) {
				productMix = productName + ", " + productRate + ", " + productUnits;
			} else {
				productMix.concat(" ; " + productName + ", " + productRate + ", " + productUnits);
			}
			saved = true;
			console.log(productName);
            console.log(productRate);
            console.log(productUnits);
        }
    }
};

//Close product mix modal
function closePrdMix() {
	//Declare variables
	var i;

	//Hide modal and show parent modal	
	$("#addProductMixModal").modal("hide");
	if (subModal_2==tankmixName_MDL) {
		$("#addTankMixModal").modal("show");
	}

	//Loop through product array
	for (i=1; i<=productArr.length; i++) {
		//Clear all product containers
		prdCont = document.getElementById('prdContainer_'.concat(i));
        prdCont.remove();
	}
};




//Add product selection container to product mix modal
function addMixPrdBtn() {
	//declare variables
	var product
	var productRate
	var productUnits
    var cnt = 0;
	var prdDiv
    var id
    var newPrd_cont
    var newCont
    var productDiv
    var rateDiv
    var unitDiv
    var prdH
    var rmvBtn
    var rmvBtnIcon
    var prdSel
    var addPrdBtn
	var addPrdBtnIcon
	var alertLbl
    var prdRate
    var rateH
    var prdUnits
    var unitH
    var unitSel
    
    cnt = productArr.length + 1;
    console.log(productArr.length);
	//html product container code
    prdDiv = document.getElementById( 'prdDiv' );

	//create container
    id = "prdContainer_" + cnt;
    newPrd_cont = document.createElement( 'div' );
    newPrd_cont.className = "container";
    newPrd_cont.id = id;
    newPrd_cont.style = "border-color: rgb(160,159,159);border-bottom-style: solid;";

	//create product divider
    productDiv = document.createElement( 'div' );
    productDiv.id = 'productDiv_' + cnt;
    //heading
    prdH = document.createElement( 'H1' );
    prdH.style = "font-size: 16px;color: rgb(7,7,7);margin-bottom: 0px;";
    var text = document.createTextNode("Product ");
    productDiv.appendChild(prdH);
    //button
    rmvBtn = document.createElement( 'button' );
    rmvBtn.className="btn btn-primary";
    rmvBtn.name="removePrd";
    rmvBtn.type="button";
    rmvBtn.style="margin-left: -20px;padding-left: 0px;padding-bottom: 0px;padding-right: 5px;padding-top: 0px;";
    rmvBtn.addEventListener('click', function() { removePrd.call();});
    //button icon
    rmvBtnIcon = document.createElement( 'icon' );
    rmvBtnIcon.id='removePrd_Icon'
    rmvBtnIcon.accessKey=cnt;
    rmvBtnIcon.className="fa fa-minus";
    rmvBtnIcon.style="color: rgb(202,0,0);";
    rmvBtnIcon.style.boxSizing = "::before";
    rmvBtn.appendChild(rmvBtnIcon);
    prdH.appendChild(rmvBtn);
    prdH.appendChild(text);
    //select
    id = "pm_Product_Sel_" + cnt;
    prdSel = document.createElement( 'select' );
    prdSel.id = id;
	//prdSel.option.value="-";
    productDiv.appendChild(prdSel);  
	//button (add product button)
	addPrdBtn = document.createElement( 'button');
	addPrdBtn.className="btn-custom btn-light";  
	addPrdBtn.name="addPrd";
	addPrdBtn.type="button" 
	addPrdBtn.style="font-size: 100%;padding-right: 6px;padding-left: 20px;min-width: auto;max-width: none;padding-bottom: 0px;padding-top: 0px;font-style: italic;";
	addPrdBtn.addEventListener('click', function() { $("#addProductMixModal").modal("hide"); $("#addProductModal").modal("show");});
	//button icon (add product icon)
	addPrdBtn.innerHTML='<i class="fa fa-plus" style="color: rgb(3,169,59);text-align: center;font-size: 100%;padding-right: 5px;"></i>Add';	
	productDiv.appendChild(addPrdBtn);

    //alert label
    alertLbl = document.createElement( 'label' ); 
	alertLbl.id="pm_ProductSel_Alert_" + cnt;
    alertLbl.style="color: rgb(241,8,8);font-style: italic;padding-left: 10px;";
    productDiv.appendChild(alertLbl);

    //append product select to product container
    newPrd_cont.appendChild(productDiv);

	//create product rate divider
    rateDiv = document.createElement( 'div' );
    rateDiv.id = "productRateDiv_" + cnt;
    rateDiv.style = "padding-top: 10px;";

    //heading
    rateH = document.createElement( 'H1');
    rateH.style = "font-size: 16px;color: rgb(7,7,7);margin-bottom: 0px;";
    rateH.innerHTML = "Product Rate";
    rateDiv.appendChild(rateH);

    //text input
    prdRate = document.createElement( 'input' );
    prdRate.type = "text";
    prdRate.id = "pm_ProductRate_Input_" + cnt;
    prdRate.style="padding-top: 0px;";
    rateDiv.appendChild(prdRate);

    //alert lbl
    alertLbl = document.createElement( 'label' );
    alertLbl.id = "pm_ProductRate_Alert_" + cnt; 
	alertLbl.style = "color: rgb(241,8,8);font-style: italic;padding-left: 10px;";
    rateDiv.appendChild(alertLbl)

    //append rate divider to product container
    newPrd_cont.appendChild(rateDiv);

	//create unit measure divider
    unitDiv = document.createElement( 'div' );
    unitDiv.id = "productUnitsDiv_" + cnt;
    unitDiv.style = "padding-top: 10px;";

	//heading
    unitH = document.createElement( 'H1' );
    unitH.style="font-size: 16px;color: rgb(7,7,7);margin-bottom: 0px;";
    unitH.innerHTML = "Product Units";
    unitDiv.appendChild(unitH);

	//select
    unitSel = document.createElement( 'select' );
    unitSel.id="pm_ProductRateUnits_Sel_" + cnt;
	let unitOpArr = ["-","oz / ac","lb / ac","floz / ac","pt / ac","qt / ac","gal / ac"];

	//call populate function
	popSelectionElem(unitSel,unitOpArr);
    unitDiv.appendChild(unitSel);

	//alert label
    alertLbl = document.createElement( 'label' );
    alertLbl.id = "pm_ProductRateUnitsSel_Alert_" + cnt;
    alertLbl.style="color: rgb(241,8,8);font-style: italic;padding-left: 10px;";
    unitDiv.appendChild(alertLbl);

	//append unit divide to product container
    newPrd_cont.appendChild(unitDiv);

	//append product containe to product divider
    prdDiv.appendChild(newPrd_cont);
	productArr.push(newPrd_cont);
	return productArr;
};

//remove product selection container from product mix modal (called from javascript html 'addEventListener' element)
function removePrd(e) {
    var prdCont;
	//instance refers to prd number in modal 'integer value'
    e = e || window.event;
    e = e.target || e.srcElement;
    if (e.id === 'removePrd_Icon') {
        instance = e.accessKey;
        var containerName = "prdContainer_";
        console.log(containerName.concat(instance));
    //remove product container
        if(productArr.length >= 2) {
            prdCont = document.getElementById(containerName.concat(instance));
            prdCont.remove();
            var i = instance - 1;
            productArr.splice(i,1);
            for(i=0; i< productArr.length ; i++) {
                var obj = productArr[i];
                console.log(i);
                console.log(obj.id);
            }
        }
    }
};

//close product modal
function closePrdModal() {
	//declare variables
	var i;

	//hide modal and show parent modal	
	$("#addProductModal").modal("hide");
	if (subModal_2==tankmixName_MDL) { 
		$("#addProductMixModal").modal("show");
	}

	//loop through product array
	for (i = 1; i <= productArr.length; i++) {
	//clear all product containers
		prdCont = document.getElementById('prdContainer_'.concat(i));
        prdCont.remove();
	}
};

//function validDirectory(fileDirectory) {
//	
//};

//function saveFile(fileName,fileDirectory) {
//	
//};

//function validFile(fileName,fileDirectory) {
//	
//};
