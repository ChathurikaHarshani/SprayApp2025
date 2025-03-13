var screenWdth;
var newWdth;
var screenHght;
var newHght;
var mainColumn;
var map;
var mapDiv;
var btnGrp_Div;
var latCntr;
var lonCntr;
var zoomLvlCntr;
var boundFarm;
var boundField;
var boundCropYear;
var boundObject;
var lastVertex;
var appFeatures;
var mapFeatures;
var map;
var mapBounds;
var featBound;
var hasEditAccess;

//Object Event Functions
$(document).on("click", "#centerExtent_Btn", function () {
	leafletMap_FlyTo(mapBounds);
});

$('#top_arrow_button').click(function () {
	$(this).find('i').toggleClass('fa-caret-up fa-caret-down')
});


// window.onorientationchange = function() {
// 	//window.alert("the orientation of the device has changed" + window.orientation);
// 	//setOrientation();
// 	//bodyFormatting();
// 	//titleRowFormatting();
// 	//mapRowFormatting();

// 	//debug
// 	console.log("");
// 	console.log("Orientation Change:");
// 	console.log("DegOrient: " + window.orientation);
// 	console.log("screenWdth: " + screenWdth);
// 	console.log("screenHght: " + screenHght);
// 	console.log("html width: " + document.getElementById('userMain_HTML').clientWidth);
// 	console.log("html height: " + document.getElementById('userMain_HTML').clientHeight);
// 	console.log("titleRow width: " + document.getElementById('Title_Row').clientWidth);
// 	console.log("titleRow height: " + document.getElementById('Title_Row').clientHeight);
// 	console.log("mainRow width: " + document.getElementById('Main_Row').clientWidth);
// 	console.log("mainRow height: " + document.getElementById('Main_Row').clientHeight);
// 	console.log("mapDiv width: " + document.getElementById('Map_Div').clientWidth);
// 	console.log("mapDiv height: " + document.getElementById('Map_Div').clientHeight);
// };


$(document).on("click", "#Measure", function () {
	measureFeet();
});

//System Helper Functions
function getCookie(name) {
	var cookieArr = document.cookie.split(";");
	console.log("cookie:");
	console.log(document.cookie);
	console.log(cookieArr);
	for (var i = 0; i < cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split("=");
		if (name == cookiePair[0].trim()) {
			return decodeURIComponent(cookiePair[1]);
		}
	}
}

function disableContextMenu() {
	mapDiv = document.getElementById("Map_Div");
	mapDiv.setAttribute("oncontextmenu", "return false");
};

function enableContextMenu() {
	mapDiv = document.getElementById("Map_Div");
	mapDiv.setAttribute("oncontextmenu", "return true");
};


//Page Load Functions
function userMain_Load() {
	// var username = getCookie('username'); 
	//var jsonFile = getCookie('json');
	//var jsonFile = '<%Session["jsonFile"] %>';
	//var url = 'https://spray-safely.com/getAppJson?json='+jsonFile;

	var url = '/getAppJson';
	appFeatures = xmlhttp_get(url);


	var url = '/checkEditAccess';
	hasEditAccess = xmlhttp_get(url);
	console.log(hasEditAccess);


	refreshLeftMenu();

	//Center extent
	latCntr = 41.177;
	lonCntr = -96.47;
	zoomLvlCntr = 17;
	leafletMap_Setup(latCntr, lonCntr, zoomLvlCntr);
};

function featurePoly(feature, layer) {
	//set formatting for feature polygon and return it to the instantiating call
	featID = feature['id'];
	featProp = feature['properties'];
	featGeom = feature['geometry'];
	//drawActiveREI(featGeom['coordinates']);
	//console.log(featGeom);
	//format popup window for feature
	var popup = featurePopup(featID, featProp);


	//attach feature popup to layer
	layer.bindPopup(popup, { minwidth: 120, closeOnClick: false });
	layer.layerID = featID
	layerBounds = layer.getBounds();
	feature = { 'id': featID, 'bounds': layerBounds }
	mapFeatures.push(feature);

	// Send layer to bottom after popup is removed in case polygons overlap
	layer.getPopup().on('remove', function () {
		layer.bringToBack();
	})
};

function featureStyle(feature) {
	appTimeType = feature['properties']['AppTimeType'];

	featColor = 'gray';
	if (appTimeType == "Past") {
		featColor = '#99ff00';
	}
	else if (appTimeType == "Current") {
		featColor = '#620000';
	}
	else if (appTimeType == "Future") {
		featColor = '#ba5e2a';
	}

	return {
		fillColor: featColor,
		weight: 3,
		opacity: 1,
		color: 'white',
		fillOpacity: 0.7
	};
};

//How do I get current application im looking at?
function featurePopup(featID, featProp) {
	appFeatLength = appFeatures['features'].length;
	console.log(appFeatLength);
	for (i = 0; i < appFeatLength; i++) {
		feat = appFeatures['features'][i];
		// console.log(feat);
		id = feat['id'];

		if (id == featID) {
			featREI = feat['properties']['REIExp'];
			popup = '<h3><a href="nameofapplicationpage">' + 'Application #' + '' + featID + '</a>';

			if (hasEditAccess) {
				popup += '<div style="display:inline; padding-left:5px">' +
					'<button id="editApplicationBtn_' + featID + '" type="button" style="margin-left:auto" class="btn btn-primary edit-application btn-sm">' +
					'<i class="fa fa-edit" style="margin-left: 0px;padding-right: 5px;padding-top: 5px;"> </i>Edit </button>' +
					'</div>'
			}

			popup += '</h3><br> <b>REI Expiration: ' + featREI + '</b>';

			return popup
		}

	}




	//Population of Application Properties Modal


	console.log(featREI)
	/*
			'<br> <b>FarmName:</b> '+featFarmName+
			'<br> <b>FieldName:</b> '+featFieldName+
			'<br> <b>AppType:</b> '+featAppType+
			'<br> <b>StartTime:</b> '+featStartTime+
			'<br> <b>EndTime:</b> '+featEndTime+
			'<br> <b>Rei Expires:</b> '+featREIExp+
			'<br> <b>Weather:</b> '+featWeather+
			'<br><b>TankMix:</b> '+
			'<a href="#" onClick="openPopupModal(event,'+featID+')"><i><b>PRODUCT LIST</b></i></a>';
	*/

	//console.log(popup);

	return popup
};

function jsonTest(feature) {
	console.log(feature['properties']);
};

function openPopupModal(evt, id) {
	//set appFeatLength
	appFeatLength = appFeatures['features'].length;
	//locate product information by comparing id to feature id
	for (i = 0; i < appFeatLength; i++) {
		feat = appFeatures['features'][i];
		featID = feat['id'];
		if (featID == id) {
			featTankMix = feat['properties']['TankMix'];
		}
	}
	//set tankmix array length
	tankMixLength = featTankMix.length;
	//print properites to console
	//console.log(properties);
	carrier = {}
	prodArr = []
	for (i = 0; i < tankMixLength; i++) {
		prod = featTankMix[i];
		if (prod.hasOwnProperty('Carrier')) {
			carrier = prod
			//console.log("Carrier:"+String(prod['Carrier']));
		} else {
			prodArr[i] = prod
			//console.log("Product:"+String(prod['Product']));
		}

	}
	//sort products array alphabetically
	prodArr.sort((a, b) => (a.Product > b.Product) ? 1 : -1);
	//add carrier to popup formated products list
	carrierList = '<p><i><b>Name:</b> ' + carrier['Carrier'] + '</i>' +
		'<br><i><b>Rate:</b> ' + carrier['Rate'] + '</i>' +
		'<br><i><b>Units:</b> ' + carrier['Units'] + '</i></p>';


	//set length of products array
	prodLength = prodArr.length;
	//loop through products array and format products list for popup
	prodList = ''
	for (i = 0; i < prodLength; i++) {
		prodInfo = prodArr[i]
		prodStr = '<p><i><b>Name:</b> ' + prodInfo['Product'] + '</i>' +
			'<br><i><b>Rate:</b> ' + prodInfo['Rate'] + '</i>' +
			'<br><i><b>Units:</b> ' + prodInfo['Units'] + '</i></p>';
		prodList = prodList + prodStr;
	}
	console.log('link is working');
	console.log(evt.target);
	document.getElementById("pList_CarrierContent").innerHTML = carrierList;
	document.getElementById("pList_PrdContent").innerHTML = prodList;
	$("#pListModal").modal("show");
	location.href = "#pListCarrierHeading";
};



class HomeButton extends L.Control {
	onAdd() {
		var button = L.DomUtil.create('div');
		button.id = "centerExtent_Btn"
		button.className = "leaflet-bar leaflet-control hide-when-drawing";
		button.title = "Home";

		var crosshairs_icon = L.DomUtil.create('a');
		crosshairs_icon.className = "fa fa-crosshairs";
		crosshairs_icon.style = "font-size:30px;line-height:30px;width:30px;text-align:center;";
		crosshairs_icon.href = "#";

		button.append(crosshairs_icon);

		return button;
	}
};

class ToolsButton extends L.Control {
	onAdd() {
		var button = L.DomUtil.create('div');
		button.className = "leaflet-bar leaflet-control hide-when-drawing";
		button.title = "Tools";

		var wrench_icon = L.DomUtil.create('a');
		wrench_icon.className = "fa fa-wrench";
		wrench_icon.style = "font-size:30px;line-height:30px;width:30px;text-align:center;";
		wrench_icon.href = "#";
		wrench_icon.setAttribute("data-toggle", "dropdown");


		var menu = L.DomUtil.create('div');
		menu.className = "dropdown-menu";

		var identify = L.DomUtil.create('a');
		identify.className = "dropdown-item";
		identify.id = "Identify";
		identify.style = "width:100%";
		identify.append("Identify");

		var selection = L.DomUtil.create('a');
		selection.className = "dropdown-item";
		selection.id = "Selection";
		selection.style = "width:100%";
		selection.append("Selection");

		var measure = L.DomUtil.create('a');
		measure.className = "dropdown-item";
		measure.id = "Measure";
		measure.style = "width:100%";
		measure.append("Measure");

		menu.append(identify);
		menu.append(selection);
		menu.append(measure);

		button.append(wrench_icon);
		button.append(menu);

		return button;
	}
};

class LegendButton extends L.Control {
	onAdd() {
		var legendButton = L.DomUtil.create('div');
		legendButton.className = "leaflet-bar leaflet-control hide-when-drawing";
		legendButton.title = "Legend";

		var legend_icon = L.DomUtil.create('a');
		legend_icon.className = "fa fa-question";
		legend_icon.style = "font-size: 30px; line-height: 30px; width: 30px; text-align: center; color: #000000";
		legend_icon.href = "#";
		legend_icon.setAttribute("data-toggle", "dropdown");

		var menu = L.DomUtil.create('div');
		menu.className = "dropdown-menu";

		var expiredColor = L.DomUtil.create('div');
		expiredColor.className = "div";
		expiredColor.id = "expiredColor";
		expiredColor.style = "width: 40px; height: 25px; background: #99ff00; border-style: solid; justify-content: center; border-width: thin; border-color: black; border-radius: 4px; margin-right: 20px";

		var expiredText = L.DomUtil.create('div');
		expiredText.id = "expiredText";
		expiredText.innerHTML = "Expired";
		expiredText.style = "width:100%; text-align: justify;";
		
		var expiredFlexContainer = L.DomUtil.create('div');
		expiredFlexContainer.className = "flex-container";
		expiredFlexContainer.style = "width: 100%; display: flex; justify-content: center;";
		expiredFlexContainer.appendChild(expiredColor);
		expiredFlexContainer.appendChild(expiredText);
		
		var expiredDivContainer = L.DomUtil.create('div');
		expiredDivContainer.className = "dropdown-item";
		expiredDivContainer.style = "width: 100%; justify-content: center";
		expiredDivContainer.id = "expiredDivContainer";
		expiredDivContainer.append(expiredFlexContainer);
	
		var activeColor = L.DomUtil.create('div');
		activeColor.className = "div";
		activeColor.id = "activeColor";
		activeColor.style = "width: 40px; height: 25px; background: #620000; border-style: solid; justify-content: center; border-width: thin; border-color: black; border-radius: 4px; margin-right: 20px";

		var activeText = L.DomUtil.create('div');
		activeText.id = "activeText";
		activeText.innerHTML = "Active";
		activeText.style = "width: 100%; text-align: justify;";
		
		var activeFlexContainer = L.DomUtil.create('div');
		activeFlexContainer.className = "flex-container";
		activeFlexContainer.style = "width: 100%; display: flex; justify-content: center;";
		activeFlexContainer.appendChild(activeColor);
		activeFlexContainer.appendChild(activeText);
		
		var activeDivContainer = L.DomUtil.create('div');
		activeDivContainer.className = "dropdown-item";
		activeDivContainer.style = "width: 100%; justify-content: center";
		activeDivContainer.id = "activeDivContainer";
		activeDivContainer.append(activeFlexContainer);

		var scheduledColor = L.DomUtil.create('div');
		scheduledColor.className = "div";
		scheduledColor.id = "scheduledColor";
		scheduledColor.style = "width: 40px; height: 25px; background: #ba5e2a; border-style: solid; justify-content: center; border-width: thin; border-color: black; border-radius: 4px; margin-right: 20px";

		var scheduledText = L.DomUtil.create('div');
		scheduledText.id = "scheduledText";
		scheduledText.innerHTML = "Scheduled";
		scheduledText.style = "width:100%; text-align: justify;";
		
		var scheduledFlexContainer = L.DomUtil.create('div');
		scheduledFlexContainer.className = "flex-container";
		scheduledFlexContainer.style = "width: 100%; display: flex; justify-content: center;";
		scheduledFlexContainer.appendChild(scheduledColor);
		scheduledFlexContainer.appendChild(scheduledText);
		
		var scheduledDivContainer = L.DomUtil.create('div');
		scheduledDivContainer.className = "dropdown-item";
		scheduledDivContainer.style = "width: 100%; justify-content: center";
		scheduledDivContainer.id = "scheduledDivContainer";
		scheduledDivContainer.append(scheduledFlexContainer);

		menu.append(expiredDivContainer);
		menu.append(activeDivContainer);
		menu.append(scheduledDivContainer);

		legendButton.append(legend_icon);
		legendButton.append(menu);

		return legendButton;
	}
}

//Leaflet Functions
var map;
function leafletMap_Setup(lat, lon, zoomlvl) {
	mapFeatures = [];
	// build map 

	if (map) {
		map.off();
		map.remove();
	}

	map = L.map('Map_Div', {
		drawControl: false,
		zoomControl: false
	});

	//L.esri.TiledMapLayer

	mapLink = '<a href="http://www.esri.com/">Esri</a>';
	wholink = 'i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
	L.tileLayer(
		'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
		attribution: '&copy; ' + mapLink + ', ' + wholink,
		maxNativeZoom: 19,
		maxZoom: 22
	}).addTo(map);

	//L.esri.basemapLayer('ImageryClarity').addTo(mapDiv);
	L.esri.basemapLayer('TerrainLabels').addTo(map);

	zoom = L.control.zoom({ position: 'topright' }).addTo(map);
	L.DomUtil.addClass(zoom.getContainer(), 'hide-when-drawing');
	map.addControl(new HomeButton({ position: 'topright' }));
	map.addControl(new ToolsButton({ position: 'topright' }));
	map.addControl(new LegendButton({ position: 'bottomright' }));

	featCount = Object.keys(appFeatures['features']).length;

	if (featCount > 0) {
		//appFeatures['features'].forEach(featurePoly);
		var poly = new L.geoJson(appFeatures['features'], { onEachFeature: featurePoly, style: featureStyle }).addTo(map);
		//console.log(appFeatures['features']);

		// console.log(poly.getBounds());
		mapBounds = poly.getBounds();
		// console.log(mapBounds.length)

		map.fitBounds(mapBounds);



	} else {
		map.setView([lat, lon], zoomlvl);
	}

};


class DrawConfirmButton extends L.Control {
	onAdd() {
		var control = L.DomUtil.create('div');
		control.id = "drawConfirm_Control"
		control.className = "leaflet-bar leaflet-control";
		control.title = "Draw_Control";


		var confirm_button = L.DomUtil.create('button');
		confirm_button.id = "drawConfirm_Btn";
		confirm_button.className = "btn btn-primary";
		confirm_button.innerHTML = "Cancel";
		confirm_button.style = "color: #fff; background-color: #d9534f;";


		control.append(confirm_button);
		return control;
	}
};




function drawBoundary() {
	drawnItems = new L.featureGroup();
	map.addLayer(drawnItems);

	var drawConfirm = new DrawConfirmButton({ position: 'topright' })
	map.addControl(drawConfirm);


	var drawControlFull = new L.Control.Draw({
		draw: {
			polyline: false,
			marker: false,
			circlemarker: false
		},
		edit: {
			featureGroup: drawnItems,
			edit: false,
			remove: false
		},
		position: 'topright'


	});
	map.addControl(drawControlFull);


	var drawControlEditOnly = new L.Control.Draw({
		draw: false,
		edit: {
			featureGroup: drawnItems
		},
		position: 'topright'
	});



	$(".hide-when-drawing").css('display', 'none');


	map.on("draw:drawvertex", function (e) {
		evnt = window.event;

		if (evnt.which == 3) {
			dlp_btn = document.querySelector('[title="Delete last point drawn"]');
			dlp_btn.click();
		}
	});


	map.on('draw:drawstart', function () {
		//Disable right click context menu (ability to right click) during drawing
		disableContextMenu();
	});


	map.on('draw:drawstop', function () {
		//Enable right click context menu
		enableContextMenu();

		//save feature to geojson and add as individual layer


		//send new geojson to database connection for storage

	});


	var geometry = null;
	map.on('draw:created', function (e) {
		layer = e.layer;
		drawnItems.addLayer(layer);
		geometry = layer.toGeoJSON()['geometry'];

		// Change confirm button
		$("#drawConfirm_Btn").text("Finish");
		$("#drawConfirm_Btn").css("background-color", "#0275d8");


		// Change available controls
		map.removeControl(drawControlFull);
		map.addControl(drawControlEditOnly);
	});


	map.on('draw:deleted', function (e) {
		// Only do something if it was actually deleted (0 drawn shapes remaining)
		if (drawnItems.getLayers().length == 0) {

			geometry = null;

			// Change confirm button
			$("#drawConfirm_Btn").text("Cancel");
			$("#drawConfirm_Btn").css("background-color", "#d9534f");

			// Change available controls
			map.removeControl(drawControlEditOnly);
			map.addControl(drawControlFull);
		}
	});



	$(document).on("click", "#drawConfirm_Btn", function () {
		$(".hide-when-drawing").css('display', '');

		map.removeControl(drawControlFull);
		map.removeControl(drawControlEditOnly);
		map.removeControl(drawConfirm);

		// Disable event handlers - caused issues with duplicate events without this
		map.off('draw:created');
		map.off('draw:deleted');

		drawnItems.clearLayers();
		map.removeLayer(drawnItems);


		// Call function to go back to modal if anything was drawn
		if (geometry !== null) {
			finishedDrawing(geometry);
		}
	});

};

function leafletMap_FlyTo(elemBounds) {
	map.fitBounds(elemBounds);
	//map.setView([lat,lon],zoomlvl);
};



function measureFeet() {
	var lineItem = new L.featureGroup();
	var totalDistance;
	var segmentDistance;
	var previousVertice;
	var currentVertice;

	var measureLine = new L.Draw.Polyline(map, {
		showLength: true,
		metric: false,
		feet: true,
		allowIntersection: true,
	});

	measureLine.enable();

	drawControls(
		addFinish = false,
		addUndoBtn = true,
		addCancelBtn = true
	);

	map.on("draw:drawstart", function () {
		disableContextMenu();
	});

	map.on("draw:drawvertex", function (e) {
		console.log(e.target);
	});

	map.on("draw:drawstop", function () {
		enableContextMenu();
		btnGrp_Div.remove();
	});

	$('#undo_btn').on("click", function () {
		measureLine.deleteLastVertex();
	});

	$('#cancel_btn').on("click", function () {
		measureLine.disable();
	});

};

function drawControls(addFinishBtn, addUndoBtn, addCancelBtn) {
	var mainColumn = document.getElementById('Main_Clm');

	//create elements
	btnGrp_Div = document.createElement('Div');
	btnGrp_Div.id = "drawBtnGrp_Div";
	btnGrp_Div.className = "btn-group flex-shrink-1 align-items-center";
	btnGrp_Div.setAttribute("role", "group");
	btnGrp_Div.style = "height: 30px;background: rgba(201,197,197,0.09);border-radius: 5px;margin-top: 2px;text-align: center;border: 1px solid rgba(33,37,41,0.36);width: 174px ;";
	btnGrp_Div.style.zIndex = 150;

	var finishBtn = document.createElement('button');
	finishBtn.id = "finish_btn";
	finishBtn.className = "btn btn-primary";
	finishBtn.setAttribute("type", "button");
	finishBtn.style = "margin-right: 2px;margin-left: 2px;font-size: 10px;height: 25px;padding-top: 3px;padding-bottom: 3px;margin-top: 0px;background: rgba(187,186,186,0.56);border-radius: 5px;";
	finishBtn.innerHTML = "Finish"
	finishBtn.style.zIndex = 50;

	var undoBtn = document.createElement('button');
	undoBtn.id = "undo_btn";
	undoBtn.className = "btn btn-primary";
	undoBtn.setAttribute("type", "button");
	undoBtn.style = "margin-right: 2px;margin-left: 2px;font-size: 10px;height: 25px;padding-top: 3px;padding-bottom: 3px;margin-top: 0px;background: rgba(187,186,186,0.56);border-radius: 5px;";
	undoBtn.innerHTML = "Undo"
	undoBtn.style.zIndex = 50;

	var cancelBtn = document.createElement('button');
	cancelBtn.id = "cancel_btn";
	cancelBtn.className = "btn btn-primary";
	cancelBtn.setAttribute("type", "button");
	cancelBtn.style = "margin-right: 2px;margin-left: 2px;font-size: 10px;height: 25px;padding-top: 3px;padding-bottom: 3px;margin-top: 0px;background: rgba(187,186,186,0.56);border-radius: 5px;";
	cancelBtn.innerHTML = "Cancel"
	cancelBtn.style.zIndex = 50;

	//add buttons to button group divider
	if (addFinishBtn == true) {
		btnGrp_Div.append(finishBtn);
	}
	if (addUndoBtn == true) {
		btnGrp_Div.append(undoBtn);
	}
	if (addCancelBtn == true) {
		btnGrp_Div.append(cancelBtn);
	}


	//add button group to map divider
	mainColumn.append(btnGrp_Div);

	//format button group location
	var drwBtnGrp = document.getElementById("drawBtnGrp_Div")
	drwBtnGrp.style.marginLeft = String((screenWdth / 2) - 87) + "px";

	// var ctrExtntBtn = document.getElementById("centerExtent_Btn");
	// console.log("height: " + ctrExtntBtn.clientHeight);
	// console.log("marginTop: " + ctrExtntBtn.offsetTop);
	// console.log("total: " + (ctrExtntBtn.clientHeight+ctrExtntBtn.offsetTop));
	// var toolbarCollapse = document.getElementById('Main_Toolbar_Collapse');
	// var totalMove = toolbarCollapse.clientHeight + ctrExtntBtn.offsetTop;
	// drwBtnGrp.style.marginTop = String(-(totalMove + 2))+"px";
	//String(-(ctrExtntBtn.clientHeight+ctrExtntBtn.offsetTop))+"px";
};

//called from farm management tree
function panToApplication(featID) {
	mapFeatLen = mapFeatures.length;
	for (i = 0; i < mapFeatLen; i++) {
		mapFeat = mapFeatures[i];
		mapFeatID = mapFeat['id'];
		if (mapFeatID == featID) {
			featBounds = mapFeat['bounds'];
			leafletMap_FlyTo(featBounds);
			//map.fitBounds(featBounds);
		}
	}
}


//Mobile device functions
function setOrientation() {
	if (window.orientation == 0 || window.orientation == 180) {
		screenWdth = document.getElementById('userMain_HTML').clientWidth;
		screenHght = document.getElementById('userMain_HTML').clientHeight;
	} else if (window.orientation == 90 || window.orientation == -90) {
		screenWdth = document.getElementById('userMain_HTML').clientHeight;
		screenHght = document.getElementById('userMain_HTML').clientWidth;
	};
};




function isDescendant(selector, object) {
	if (String(object[0].id).includes(selector)) {
		return true;
	}
	return false;
};

//Farm Structure Functions
function refreshLeftMenu() {

	var add_application_div = document.getElementById('add_application_div');
	add_application_div.innerHTML = "";
	if (hasEditAccess) {
		var add_application_button = document.createElement('div');
		add_application_button.innerHTML = `
										<button class="btn-custom text-left" id="addApplication" type="button"
											style="width: 100%; padding-left:20px; padding-right:20px">
											<i style="padding-left: 20px; padding-right: 20px">
												<i class="fas fa-spray-can"></i>
												Add Application
											</i>
										</button>
										`;
		add_application_div.appendChild(add_application_button);
	}


	// console.log("refreshLeftMenu");
	// console.log(appFeatures);

	var main_accordion_body = document.getElementById('farms_accordion');
	main_accordion_body.innerHTML = ''; //Clear previous content if any

	var farmName;
	var farmObj;
	var farmCollapse;
	var fieldName;
	var fieldObj; 			//field collapse object
	var fieldAppAccordion;
	var appObj;				//application collapse object
	var appCollapse;
	var appDSObj;
	var i;
	var j;
	var x;


	//Populate FarmManager Tree from JSON appFeatures Variable

	//Set feature count for loop
	featCnt = appFeatures['features'].length;

	//Initiate array variables
	mgmtTreeArr = [];

	//Loop through features and populate farms array
	for (i = 0; i < featCnt; i++) {
		//Set feature properties to variables
		feat = appFeatures['features'][i];
		featID = feat['id'];
		featProp = feat['properties'];
		farmName = featProp['FarmName'];
		fieldName = featProp['FieldName'];
		tankMixName = featProp['TankMixName'];

		tankMixProducts = featProp['Products'];
		tankMixCarrier = featProp['Carrier'];

		appDict = { 'AppID': featID, 'TankMixName': tankMixName, 'CarrierInfo': tankMixCarrier, 'ProductsInfo': tankMixProducts };

		if (mgmtTreeArr.length > 0) {
			treeLen = mgmtTreeArr.length;
			//Loop through management tree array
			for (l = 0; l < treeLen; l++) {
				farmDictInst = mgmtTreeArr[l];
				farmInstName = farmDictInst['FarmName'];

				//Check if tree array item matches current feature farm
				if (farmInstName == farmName) {
					fieldInstArr = farmDictInst['Fields'];
					fieldLen = fieldInstArr.length;

					//Loop through field instance array and check for field
					for (n = 0; n < fieldLen; n++) {
						fieldInst = fieldInstArr[n];
						fieldInstName = fieldInst['FieldName'];

						if (fieldInstName == fieldName) {
							appArr = fieldInst['Apps'];
							appArr.push(appDict);
						} else if (n == fieldLen - 1) { //Field does not exist yet for this farm
							appArr = [appDict];
							fieldDict = { 'FieldName': fieldName, 'Apps': appArr };
							fieldInstArr.push(fieldDict);
						}

					}
				} else if (l == treeLen - 1) { //Farm does not exist yet
					appArr = [appDict];
					fieldDict = { 'FieldName': fieldName, 'Apps': appArr };
					fieldArr = [fieldDict];
					farmDict = { 'FarmName': farmName, 'Fields': fieldArr };
					mgmtTreeArr.push(farmDict);
				}
			}
		} else { //First farm to be pushed onto mgmtTreeArr
			appArr = [appDict];
			fieldDict = { 'FieldName': fieldName, 'Apps': appArr };
			fieldArr = [fieldDict];
			farmDict = { 'FarmName': farmName, 'Fields': fieldArr };
			mgmtTreeArr.push(farmDict);
		}
	}

	console.log(mgmtTreeArr);

	elemCnt = mgmtTreeArr.length;
	main_accordion_body.innerHTML = '';

	//Loop through management tree array and populate
	for (i = 0; i < elemCnt; i++) {

		farmDictInst = mgmtTreeArr[i];
		farmName = farmDictInst['FarmName'];
		farmObj = addFarm(i, farmName);

		farmCollapse = farmObj.lastChild;
		farmFieldAccordion = farmCollapse.lastChild;

		instFields = farmDictInst['Fields'];
		instFieldsLen = instFields.length

		//Loop through farm fields
		for (j = 0; j < instFieldsLen; j++) {
			fieldInst = instFields[j];
			fieldName = fieldInst['FieldName'];
			fieldObj = addField(i, j, fieldName);

			fieldCollapse = fieldObj.lastChild;
			fieldAppAccordion = fieldCollapse.lastChild;

			//Add application element per field
			appContObj = addApplicationStructure(i, j)
			appContCollapse = appContObj.lastChild;
			appContAccordion = appContCollapse.lastChild;

			applications = fieldInst['Apps'];
			appsLen = applications.length;

			//Add application to application element	
			for (x = 0; x < appsLen; x++) {
				app = applications[x];
				appName = app['TankMixName'];
				appID = app['AppID'];

				appObj = addApplication(i, j, x, appID, appName);
				appCollapse = appObj.lastChild;

				//App carrier rate element
				carrierInfo = app['CarrierInfo'];

				carrierName = carrierInfo[0];
				carrierRate = carrierInfo[1];
				carrierUnits = carrierInfo[2];

				carrierInfoString = String(carrierName) + ": " + String(carrierRate) + " " + String(carrierUnits);

				appDSObj = addCarrierRate(i, j, appID, 0, carrierInfoString);

				//Append carrier rate element to application
				appCollapse.append(appDSObj);

				//Append application to application structure
				appContAccordion.append(appObj);
			}
			//Append application object to field structure
			fieldAppAccordion.append(appContObj);

			//Append field object to farm structure
			fieldCollapse.setAttribute("data-parent", String("#").concat(farmFieldAccordion.id));
			farmFieldAccordion.append(fieldObj); //TODO: append field objects as multiple cards under same accordion instead of multiple accordions
		}
		//Append farm object to farm structure column
		main_accordion_body.append(farmObj);
	}
};


function addFarm(frmNum, farmName) {
	// Creates farm structure and returns it to calling
	// event function. (should be appended to farm Column
	// container in farm manager structure row)

	var frmID;		//Farm unique identifier

	//Initialize variables
	frmID = String("f").concat(frmNum);

	//Initialize overall card wrapper
	var FS_farmCardWrapper = document.createElement('div');
	FS_farmCardWrapper.id = String("FS_farmCardWrapper_").concat(frmID)
	FS_farmCardWrapper.className = "card";


	//Initialize card
	var FS_farmCard = document.createElement('div');
	FS_farmCard.id = String("FS_farmCard_").concat(frmID)
	FS_farmCard.className = "card";

	//Initialize card header
	var FS_farmCardHeader = document.createElement('div');
	FS_farmCardHeader.id = String("FS_farmCardHeader_").concat(frmID)
	FS_farmCardHeader.className = "card-header left-nav-card-header";

	var FS_farmHeader = document.createElement('h1');
	FS_farmHeader.id = String("FS_farmHeader_").concat(frmID);

	var FS_farmHeaderButton = document.createElement('button');
	FS_farmHeaderButton.id = String("FS_farmHeaderButton_").concat(frmID);
	FS_farmHeaderButton.className = "btn left-nav-btn text-left collapsed";
	FS_farmHeaderButton.style = "width:100%;";


	var FS_farmHeader_Icon = document.createElement('i');
	FS_farmHeader_Icon.className = "fas fa-warehouse"
	FS_farmHeader_Icon.id = String("FS_farmLink_Icon" + "_").concat(frmID);
	FS_farmHeader_Icon.style = "padding-right: 5px;color: rgb(177,6,6);border-top-left-radius: -41px;border: 3px none rgb(4,4,4);text-shadow: 0px 0px rgb(10,10,10);font-size: 100%;";



	FS_farmHeaderButton.setAttribute("data-Toggle", "collapse");
	FS_farmHeaderButton.setAttribute("data-target", String("#FS_farmCollapse_").concat(frmID));

	FS_farmHeaderButton.append(FS_farmHeader_Icon);
	FS_farmHeaderButton.append(farmName);
	FS_farmHeader.append(FS_farmHeaderButton);
	FS_farmCardHeader.append(FS_farmHeader);



	//Initialize card content
	var FS_farmCollapse = document.createElement('div');
	FS_farmCollapse.id = String("FS_farmCollapse_").concat(frmID);
	FS_farmCollapse.className = "collapse";

	var FS_farmFieldAccordion = document.createElement('div');
	FS_farmFieldAccordion.className = "accordion";
	FS_farmFieldAccordion.id = String("FS_farmFieldAccordion" + "_").concat(frmID);

	FS_farmCollapse.append(FS_farmFieldAccordion);

	FS_farmCardWrapper.append(FS_farmCardHeader);
	FS_farmCardWrapper.append(FS_farmCollapse);

	return FS_farmCardWrapper;
};

function addField(frmNum, fldNum, fieldName) {
	// Creates field structure and returns it to calling
	// event function (should be appended to farm content
	// container in farm structure object)

	var frmfldID;	//Farm, Field unique identifier

	//Initialize variables	
	frmfldID = String("f").concat(frmNum) + String("f").concat(fldNum);



	//Initialize field card wrapper
	var FS_fieldCardWrapper = document.createElement('div');
	FS_fieldCardWrapper.id = String("FS_fieldCardWrapper_").concat(frmfldID)
	FS_fieldCardWrapper.className = "card";


	//Initialize card header
	var FS_fieldCardHeader = document.createElement('div');
	FS_fieldCardHeader.id = String("FS_fieldCardHeader_").concat(frmfldID)
	FS_fieldCardHeader.className = "card-header left-nav-card-header";

	var FS_fieldHeader = document.createElement('h1');
	FS_fieldHeader.id = String("FS_fieldHeader_").concat(frmfldID);

	var FS_fieldHeaderButton = document.createElement('button');
	FS_fieldHeaderButton.id = String("FS_fieldHeaderButton_").concat(frmfldID);
	FS_fieldHeaderButton.className = "btn left-nav-btn text-left collapsed";
	FS_fieldHeaderButton.style = "width:100%;";

	var FS_fieldHeader_Icon = document.createElement('i');
	FS_fieldHeader_Icon.className = "fas fa-tractor";
	FS_fieldHeader_Icon.id = String("FS_fieldLink_Icon" + "_").concat(frmfldID);
	FS_fieldHeader_Icon.style = "padding-right: 5px;color: rgb(233,199,20);border-top-left-radius: -41px;border: 3px none rgb(4,4,4);text-shadow: -1px -1px 3px rgb(0,0,0), 1px 1px 3px rgb(0,0,0);font-size: 100%;";


	FS_fieldHeaderButton.setAttribute("data-Toggle", "collapse");
	FS_fieldHeaderButton.setAttribute("data-target", String("#FS_fieldCollapse_").concat(frmfldID));

	FS_fieldHeaderButton.append(FS_fieldHeader_Icon);
	FS_fieldHeaderButton.append(fieldName);
	FS_fieldHeader.append(FS_fieldHeaderButton);
	FS_fieldCardHeader.append(FS_fieldHeader);



	//Initialize card content
	var FS_fieldCollapse = document.createElement('div');
	FS_fieldCollapse.id = String("FS_fieldCollapse_").concat(frmfldID);
	FS_fieldCollapse.className = "collapse";

	var FS_fieldAppAccordion = document.createElement('div');
	FS_fieldAppAccordion.className = "accordion";
	FS_fieldAppAccordion.id = String("FS_fieldAppAccordion" + "_").concat(frmfldID);

	FS_fieldCollapse.append(FS_fieldAppAccordion);

	FS_fieldCardWrapper.append(FS_fieldCardHeader);
	FS_fieldCardWrapper.append(FS_fieldCollapse);

	return FS_fieldCardWrapper;
};



function addApplicationStructure(frmNum, fldNum) {
	// Creates Application structure in farm field structure and return it to
	// calling event function (should be appended to field content container
	// in farm structure object)

	var frmfldApp;		//Farm, Field unique identifier

	//Initialize variables	
	frmfldApp = String("f").concat(frmNum) + String("f").concat(fldNum) + String("A").concat(0);



	//Initialize app card wrapper
	var FS_appStructCardWrapper = document.createElement('div');
	FS_appStructCardWrapper.id = String("FS_appStructCardWrapper_").concat(frmfldApp)
	FS_appStructCardWrapper.className = "card";


	//Initialize card header
	var FS_appStructCardHeader = document.createElement('div');
	FS_appStructCardHeader.id = String("FS_appStructCardHeader_").concat(frmfldApp)
	FS_appStructCardHeader.className = "card-header left-nav-card-header";

	var FS_appStructHeader = document.createElement('h1');
	FS_appStructHeader.id = String("FS_appStructHeader_").concat(frmfldApp);

	var FS_appStructHeaderButton = document.createElement('button');
	FS_appStructHeaderButton.id = String("FS_appStructHeaderButton_").concat(frmfldApp);
	FS_appStructHeaderButton.className = "btn left-nav-btn text-left collapsed";
	FS_appStructHeaderButton.style = "width:100%;";

	var FS_appStruct_Icon = document.createElement('i');
	FS_appStruct_Icon.className = "fas fa-layer-group";
	FS_appStruct_Icon.id = String("FS_appContLink_Icon" + "_").concat(frmfldApp);
	FS_appStruct_Icon.style = "padding-right: 5px;color: #888888;border-top-left-radius: -41px;border: 3px none rgb(4,4,4);text-shadow: -1px -1px 3px rgb(0,0,0), 1px 1px 3px rgb(0,0,0);font-size: 100%;";


	FS_appStructHeaderButton.setAttribute("data-Toggle", "collapse");
	FS_appStructHeaderButton.setAttribute("data-target", String("#FS_appStructCollapse_").concat(frmfldApp));

	FS_appStructHeaderButton.append(FS_appStruct_Icon);
	FS_appStructHeaderButton.append("Applications");
	FS_appStructHeader.append(FS_appStructHeaderButton);
	FS_appStructCardHeader.append(FS_appStructHeader);



	//Initialize card content
	var FS_appStructCollapse = document.createElement('div');
	FS_appStructCollapse.id = String("FS_appStructCollapse_").concat(frmfldApp);
	FS_appStructCollapse.className = "collapse";

	var FS_appStructAccordion = document.createElement('div');
	FS_appStructAccordion.className = "accordion";
	FS_appStructAccordion.id = String("FS_appStructAccordion" + "_").concat(frmfldApp);

	FS_appStructCollapse.append(FS_appStructAccordion);

	FS_appStructCardWrapper.append(FS_appStructCardHeader);
	FS_appStructCardWrapper.append(FS_appStructCollapse);

	return FS_appStructCardWrapper;
};


function addApplication(frmNum, fldNum, asNum, appID, appName) {
	// Creates application and returns it to calling event function

	var frmfldAID;	//Farm, Field, Application unique identifier

	//Initialize variables
	frmfldAID = String("f").concat(frmNum) + String("f").concat(fldNum) + String("A").concat(asNum);


	//Initialize app card wrapper
	var FS_appCardWrapper = document.createElement('div');
	FS_appCardWrapper.id = String("FS_appCardWrapper_").concat(frmfldAID)
	FS_appCardWrapper.className = "card";


	//Initialize card header
	var FS_appCardHeader = document.createElement('div');
	FS_appCardHeader.id = String("FS_appStructCardHeader_").concat(frmfldAID)
	FS_appCardHeader.className = "card-header left-nav-card-header";

	var FS_appHeader = document.createElement('h1');
	FS_appHeader.id = String("FS_appStructHeader_").concat(frmfldAID);

	var FS_appHeaderButton = document.createElement('button');
	FS_appHeaderButton.id = String("FS_appHeaderButton_").concat(frmfldAID);
	FS_appHeaderButton.className = "btn left-nav-btn text-left collapsed";
	FS_appHeaderButton.style = "width:100%;";


	var FS_appData_Icon = document.createElement('i');
	FS_appData_Icon.className = "la la-file-text-o";
	FS_appData_Icon.id = String("FS_appDataLink_Icon" + "_").concat(frmfldAID);
	FS_appData_Icon.style = "padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;"

	FS_appHeaderButton.setAttribute("data-Toggle", "collapse");
	FS_appHeaderButton.setAttribute("data-target", String("#FS_appCollapse_").concat(frmfldAID));

	FS_appHeaderButton.append(FS_appData_Icon);
	FS_appHeaderButton.append(appName);

	FS_appHeaderButton.setAttribute('onClick', 'panToApplication(' + appID + ')');

	FS_appHeader.append(FS_appHeaderButton);
	FS_appCardHeader.append(FS_appHeader);


	//Initialize card content
	var FS_appCollapse = document.createElement('div');
	FS_appCollapse.id = String("FS_appCollapse_").concat(frmfldAID);
	FS_appCollapse.className = "collapse";


	FS_appCardWrapper.append(FS_appCardHeader);
	FS_appCardWrapper.append(FS_appCollapse);


	return FS_appCardWrapper;
};




function addCarrierRate(frmNum, fldNum, appID, dsNum, rateName) {
	var frmfldADSID;	//Farm, Field, Application, dataset unique identifier

	//Initialize variables
	frmfldADSID = String("f").concat(frmNum) + String("f").concat(fldNum) + String("A").concat(appID) + String("DS").concat(dsNum);

	//Initialize card content
	var FS_appRate = document.createElement('div');
	FS_appRate.id = String("FS_appRate_").concat(frmfldADSID);
	FS_appRate.className = "card-body";

	var FS_app_Icon = document.createElement('i');
	FS_app_Icon.className = "fas fa-spray-can";
	FS_app_Icon.id = String(String("FS_app").concat(appID) + "_Link_Icon" + "_").concat(frmfldADSID);
	FS_app_Icon.style = "padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;";



	//initialize app card wrapper
	var FS_appCardWrapper = document.createElement('div');
	FS_appCardWrapper.id = String("FS_appCardWrapper_").concat(frmfldADSID);
	FS_appCardWrapper.className = "card";


	//initialize field divider
	// var FS_fieldDiv = document.createElement( 'div' );
	// FS_fieldDiv.className="accordion";
	// FS_fieldDiv.id=String("FS_field_div"+"_").concat(frmfldID);




	//initialize card header
	var FS_appCardHeader = document.createElement('div');
	FS_appCardHeader.id = String("FS_appStructCardHeader_").concat(frmfldADSID)
	FS_appCardHeader.className = "card-header left-nav-card-header";

	var FS_appHeader = document.createElement('h1');
	FS_appHeader.id = String("FS_appStructHeader_").concat(frmfldADSID);

	var FS_appHeaderButton = document.createElement('button');
	FS_appHeaderButton.id = String("FS_appHeaderButton_").concat(frmfldADSID);
	FS_appHeaderButton.className = "btn left-nav-btn text-left collapsed";
	FS_appHeaderButton.style = "width:100%;";


	var FS_appData_Icon = document.createElement('i');
	FS_appData_Icon.className = "la la-file-text-o";
	FS_appData_Icon.id = String("FS_appDataLink_Icon" + "_").concat(frmfldADSID);
	FS_appData_Icon.style = "padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;"

	FS_appHeaderButton.setAttribute("data-Toggle", "collapse");
	FS_appHeaderButton.setAttribute("data-target", String("#FS_appCollapse_").concat(frmfldADSID));

	FS_appHeaderButton.append(FS_appData_Icon);
	FS_appHeaderButton.append(appName);
	FS_appHeaderButton.setAttribute('onClick', 'panToApplication(' + appID + ')');
	FS_appHeader.append(FS_appHeaderButton);
	FS_appCardHeader.append(FS_appHeader);



	//initialize card content
	var FS_appCollapse = document.createElement('div');
	FS_appCollapse.id = String("FS_appCollapse_").concat(frmfldADSID);
	FS_appCollapse.className = "collapse";

	// var FS_fieldCardBody = document.createElement('div');
	// FS_fieldCardBody.className="card-body";

	// FS_fieldCollapse.append(FS_fieldCardBody);




	// var FS_appAccordion = document.createElement( 'div' );
	// FS_appAccordion.className="accordion";
	// FS_appAccordion.id=String("FS_appAccordion"+"_").concat(frmfldAID);

	// // FS_farmCollapse.append(FS_farmCardBody);
	// FS_appCollapse.append(FS_appAccordion);



	FS_appCardWrapper.append(FS_appCardHeader);
	FS_appCardWrapper.append(FS_appCollapse);


	// FS_fieldDiv.append(FS_fieldCardHeader);
	// FS_fieldDiv.append(FS_fieldCollapse);


	return FS_appCardWrapper;
};















// //initialize application data collapse
// 	var FS_appDataCollapse = document.createElement( 'div' );
// 	FS_appDataCollapse.id=String("FS_appDataCollapse"+"_").concat(frmfldAID);
// 	FS_appDataCollapse.style="padding-left: 16px;margin-top: -9px;padding-bottom: 5px;padding-top: 2px;";

// //initialize application data collapse button
// 	var FS_appDataButton = document.createElement( 'a' );
// 	FS_appDataButton.className="btn btn-light";
// 	FS_appDataButton.setAttribute("data-toggle","collapse");
// 	FS_appDataButton.setAttribute("aria-expanded","false");
// 	FS_appDataButton.setAttribute("aria-controls",String("FS_appDataContent"+"_").concat(frmfldAID));
// 	FS_appDataButton.href=String("#FS_appDataContent"+"_").concat(frmfldAID);
// 	FS_appDataButton.setAttribute("role","button");
// 	FS_appDataButton.id=String("FS_appDataCollapse_btn"+"_").concat(frmfldAID);
// 	FS_appDataButton.style="font-size: 15px;line-height: 13px;padding: 0px;width: 16px;height: 17px;margin-top: 5px;";

// //initialize application data collapse button icon	
// 	var FS_appDataButton_Icon = document.createElement( 'i' );
// 	FS_appDataButton_Icon.className="far fa-plus-square justify-content-center align-items-center align-content-center align-self-center";
// 	FS_appDataButton_Icon.id=String("appDataBtn_Icon"+"_").concat(frmfldAID); 
// 	FS_appDataButton_Icon.style="color: rgba(33,37,41,0.92);font-size: 12px;line-height: 16px;letter-spacing: 2px;padding: 0px;box-shadow: 0px 0px;width: 16px;height: 14px;text-align: center;";

// //initialize application data link
// 	var FS_appDataLink = document.createElement( 'a' );
// 	FS_appDataLink.id=String("FS_appDataLink"+"_").concat(frmfldAID);
// 	FS_appDataLink.style="text-align: right;color: rgb(3,3,3);font-size: 70%;";
// 	FS_appDataLink.setAttribute('onClick','panToApplication('+appID+')');

// //initialize application data link icon
// 	var FS_appDataLink_Icon = document.createElement( 'i' );
// 	FS_appDataLink_Icon.className="la la-file-text-o";
// 	FS_appDataLink_Icon.id=String("FS_appDataLink_Icon"+"_").concat(frmfldAID);
// 	FS_appDataLink_Icon.style="padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;"

// //initialize application data collapse content divider 
// 	var FS_appDataContent = document.createElement( 'div' );
// 	FS_appDataContent.className="collapse";
// 	FS_appDataContent.id=String("FS_appDataContent"+"_").concat(frmfldAID);
// 	FS_appDataContent.style="padding-bottom: 3px;";

// //initialize a divider to contain application rate (container for application carrier rate)
// 	var FS_appDataDiv = document.createElement( 'div' );
// 		FS_appDataDiv.className="d-flex flex-column flex-grow-1 flex-shrink-1 flex-fill justify-content-start align-items-start align-content-start align-self-start";
// 		FS_appDataDiv.id=String("FS_appData_Div"+"_").concat(frmfldAID);
// 		FS_appDataDiv.style="font-size: 100%;padding-left: 17px;width: 126px;padding-bottom: 2px;";
// //check application name length and set it to a limit of 14 characters
//     if(appName.length>14){
//         appName = appName.substring(0,11).concat('...');
//     }

// //Append Elements
// 	//icon to link
// 	FS_appDataLink.append(FS_appDataLink_Icon);
// 	//text to link
// 	FS_appDataLink.append(appName);
// 	//button icon to button
// 	FS_appDataButton.append(FS_appDataButton_Icon);
// 	//button to collapse
// 	FS_appDataCollapse.append(FS_appDataButton);
// 	//link to collapse
// 	FS_appDataCollapse.append(FS_appDataLink);
// 	//div to content
// 	FS_appDataContent.append(FS_appDataDiv);
// 	//content to collapse
// 	FS_appDataCollapse.append(FS_appDataContent);

// //return initialized application data structure object
// 	return FS_appDataCollapse;
// };

//function addApplication(frmNum,fldNum,cyNum,asNum,dsNum,applicationName,datasetLink){
//// Creates an application dataset object and returns it
//// to the calling event function (should be appended to 
//// the application div in the application content container
//// in the application structure)
//
//	var frmfldCYASDSID;		//farm, field, crop year, application, dataset Unique Identifier
//
////initialize variables
//	frmfldCYASDSID = String("f").concat(frmNum)+String("f").concat(fldNum)+String("CY").concat(cyNum)+String("AS").concat(asNum)+String("DS").concat(dsNum);
//
////initialize boundary dataset divider
//	var FS_appDSDiv = document.createElement( 'div' );
//	FS_appDSDiv.className="d-flex flex-column flex-grow-1 flex-shrink-1 flex-fill justify-content-start align-items-start align-content-start align-self-start";
//	FS_appDSDiv.id=String(String("FS_app").concat(asNum)+"_Div"+"_").concat(frmfldCYASDSID);
//	FS_appDSDiv.style="font-size: 100%;padding-left: 34px;width: 109px;padding-top: 1px;padding-bottom: 1px;";
//
////initialize boundary dataset link
//	var FS_appDSLink = document.createElement( 'a' );
//	FS_appDSLink.id=String(String("FS_app").concat(asNum)+"_Link"+"_").concat(frmfldCYASDSID);
//	FS_appDSLink.style="text-align: right;color: rgb(3,3,3);font-size: 60%;";
//
////initialize boundary dataset link icon
//	var FS_appDSLink_Icon = document.createElement( 'i' );
//	FS_appDSLink_Icon.className="fas fa-spray-can";
//	FS_appDSLink_Icon.id=String(String("FS_app").concat(asNum)+"_Link_Icon"+"_").concat(frmfldCYASDSID);
//	FS_appDSLink_Icon.style="padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;";
//	
////Append Elements
//	//icon to link
//	FS_appDSLink.append(FS_appDSLink_Icon);
//	//text to link
//	FS_appDSLink.append(applicationName);
//	//link to div
//	FS_appDSDiv.append(FS_appDSLink)

////return initialized boundary dataset object
//	return FS_appDSDiv;
//};

function addAppRate(frmNum, fldNum, appID, dsNum, rateName, datasetLink) { //TODO: datasetLink not needed?
	// Creates an application dataset object and returns it
	// to the calling event function (should be appended to 
	// the application div in the application content container
	// in the application structure)

	var frmfldADSID;		//farm, field, application, dataset Unique Identifier

	//initialize variables
	frmfldADSID = String("f").concat(frmNum) + String("f").concat(fldNum) + String("A").concat(appID) + String("DS").concat(dsNum);


	//initialize card content
	var FS_appRate = document.createElement('div');
	FS_appRate.id = String("FS_appRate_").concat(frmfldADSID);
	FS_appRate.className = "card-body";

	var FS_app_Icon = document.createElement('i');
	FS_app_Icon.className = "fas fa-spray-can";
	FS_app_Icon.id = String(String("FS_app").concat(appID) + "_Link_Icon" + "_").concat(frmfldADSID);
	FS_app_Icon.style = "padding-right: 5px;border-top-left-radius: -41px;border: 3px none rgb(1,1,1);font-size: 100%;";


	FS_appRate.append(FS_app_Icon);
	FS_appRate.append(rateName);




	return FS_appRate;


};











$(document).ready(function () {
    $("#saveApplicatorBtn").click(function (event) {
        event.preventDefault(); // Prevent default form submission

        var firstName = $("#firstName").val();
        var lastName = $("#lastName").val();
        var orgName = $("#orgName").val();

        if (!firstName || !lastName || !orgName) {
            alert("All fields are required.");
            return;
        }

        $.ajax({
            url: "/saveNewApplicator",
            type: "POST",
            data: {
                firstName: firstName,
                lastName: lastName,
                orgName: orgName
            },
            success: function (response) {
                alert(response.message);
                if (response.success) {
                    location.reload(); // Reload the page on success
                }
            },
            error: function (xhr) {
                console.error("Request failed: ", xhr.responseText);
                alert("Failed to add applicator. Check console for details.");
            }
        });
    });
});


$('#saveApplicatorButton').click(function() {
    var data = $("#applicatorForm").serialize();
    console.log("🔹 Sending Data:", data);  // Debugging log

    $.ajax({
        url: "/saveNewApplicator",
        type: "POST",
        data: data,
        success: function(response) {
            console.log("✅ Response:", response);
            alert(response.message);
        },
        error: function(xhr, status, error) {
            console.log("❌ Error:", xhr.responseText);
            alert("Error: " + xhr.responseText);
        }
    });
});

