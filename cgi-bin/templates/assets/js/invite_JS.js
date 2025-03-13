$("#sendInvite").on("click", function() {
    var url = '/invite';
	allOrgNames = xmlhttp_get(url);
    
	farmOrgSel = document.getElementById('farm_FarmOrg_Sel');
	popSelectionElem(farmOrgSel, allOrgNames);

	$('#addFarmModalLoading').fadeOut();
});