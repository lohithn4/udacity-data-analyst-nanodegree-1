/*
 * This function gets the current filter
 * options
 */

function getCurrentFilter() {
	return {'form_select': $('#formSelect').val(),
            'form_check' : $('#formCheck:checked').length}; // will return 1 if checked, 0 if not
}


function makeChart(filter, data) {

	var width  = 590;
	var height = 400;

	// Create title based on filter
	var title_text = getTitle(filter);

	d3.select('#chart1Container').append('h2').text(title_text);

	var svg = dimple.newSvg("#chart1Container", width, height);

	// Go throught data and get survival rate dataset
	var myData = getMyData(filter, data);

	var barChart = new dimple.chart(svg, myData);

	var x;
	var y = barChart.addMeasureAxis("y", "survival_rate");
	y.title = "Survival Rate";

	if(filter.form_select == 'passenger_class' && filter.form_check == 0) {
		x = barChart.addCategoryAxis("x", ["passenger_class"]);
		x.title = "Passenger Class";
		barChart.addSeries("passenger_class", dimple.plot.bar);
	}
	else if(filter.form_select == 'passenger_class' && filter.form_check == 1) {
		x = barChart.addCategoryAxis("x", ["passenger_class", "sex"]);
		x.title = "Passenger Class / Sex";
		barChart.addSeries("sex", dimple.plot.bar);
		barChart.addLegend(37, 10, 510, 20, "right");
	}
	else if(filter.form_select == 'age_group' && filter.form_check == 0) {
		x = barChart.addCategoryAxis("x", ["age_group"]);
		x.addOrderRule(["0-15", "16-30", "31-45", "46-60", "60+", "NaN"]);
		x.title = "Age Group";
		barChart.addSeries("age_group", dimple.plot.bar);
	}
	else {
		x = barChart.addCategoryAxis("x", ["age_group", "sex"]);
		x.addOrderRule(["0-15", "16-30", "31-45", "46-60", "60+", "NaN"]);
		x.title = "Age Group / Sex";
		barChart.addSeries("sex", dimple.plot.bar);
		barChart.addLegend(37, 10, 510, 20, "right");
	}

	barChart.draw();

}


function getTitle(filter) {
	var title = "Survival Rate by ";
	if(filter.form_select == 'passenger_class') {
		title = title.concat('Passenger Class');
	} else {
		title = title.concat('Age Group');
	}
	if(filter.form_check == 1) {
		title = title.concat(' & Sex');
	}
	return title;
}

function getMyData(filter, data) {
	var myData;
	if(filter.form_select == 'passenger_class' && filter.form_check == 0) {
		myData = getSurvivalRatesClass2(data);
	}
	else if(filter.form_select == 'passenger_class' && filter.form_check == 1) {
		myData = getSurvivalRatesClass(data);
	}
	else if(filter.form_select == 'age_group' && filter.form_check == 0) {
		myData = getSurvivalRatesAge(data);
	}
	else {
		myData = getSurvivalRatesAge2(data);
	}

	return myData;

}


/*
 * This function returns a dataset of
 * Survival Rates by Class & Sex
 */

function getSurvivalRatesClass(data) {
	var array_class = ['1', '2', '3'];
	var array_sex   = ['male', 'female'];
	var result = [];
	for (var i = 0; i < array_class.length; i++) {
		for (var j = 0; j < array_sex.length; j++) {
			var class_i_sex_j_all  = dimple.filterData(dimple.filterData(data, "sex", [array_sex[j]]), "passenger_class", [array_class[i]]);
			var class_i_sex_j_surv = dimple.filterData(class_i_sex_j_all, "survived", ["1"]);
			var class_i_sex_j_rate = class_i_sex_j_surv.length / class_i_sex_j_all.length;		
			result.push({'passenger_class': parseInt(array_class[i]),
				         'sex'            : array_sex[j], 
				         'survival_rate'  : class_i_sex_j_rate});
		};
	};
	return result;
}

/*
 * This function returns a dataset of
 * Survival Rates by Class & No Sex
 */

function getSurvivalRatesClass2(data) {
	var array_class = ['1', '2', '3'];
	var result = [];
	for (var i = 0; i < array_class.length; i++) {
		var class_i_all  = dimple.filterData(data, "passenger_class", [array_class[i]]);
		var class_i_surv = dimple.filterData(class_i_all, "survived", ["1"]);
		var class_i_rate = class_i_surv.length / class_i_all.length;		
		result.push({'passenger_class': parseInt(array_class[i]),
			         'survival_rate'  : class_i_rate});
	};
	return result;
}

/*
 * This function returns a dataset of
 * Survival Rates by Age Group
 */

function getSurvivalRatesAge(data) {
	var array_age_group = ['0-15', '16-30', '31-45', '46-60', '60+', 'NaN'];
	var result = [];
	for (var i = 0; i < array_age_group.length; i++) {
		var age_group_i_all  = dimple.filterData(data, "age_group", [array_age_group[i]]);
		var age_group_i_surv = dimple.filterData(age_group_i_all, "survived", ["1"]);
		var age_group_i_rate = age_group_i_surv.length / age_group_i_all.length;
		result.push({'age_group'     : array_age_group[i],
			         'survival_rate' : age_group_i_rate});
	};
	return result;
}


/*
 * This function returns a dataset of
 * Survival Rates by Age Group and Sex
 */
function getSurvivalRatesAge2(data) {
	var array_age_group = ['0-15', '16-30', '31-45', '46-60', '60+', 'NaN'];
	var array_sex   = ['male', 'female'];
	var result = [];
	for (var i = 0; i < array_age_group.length; i++) {
		for (var j = 0; j < array_sex.length; j++) {
			var age_i_sex_j_all  = dimple.filterData(dimple.filterData(data, "age_group", [array_age_group[i]]), "sex", [array_sex[j]]);
			var age_i_sex_j_surv = dimple.filterData(age_i_sex_j_all, "survived", ["1"]);
			var age_i_sex_j_rate = age_i_sex_j_surv.length / age_i_sex_j_all.length;
			result.push({'age_group'    : array_age_group[i], 
				         'sex'          : array_sex[j], 
				         'survival_rate': age_i_sex_j_rate});
		};
	};
	return result;
}