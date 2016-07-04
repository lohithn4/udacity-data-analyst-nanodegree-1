
/*
	This functions filters the data and returns
	a dataset with the survival rates for each 
	combination of variables
*/

function getMyData(data) {
	
	var array_class     = ['1', '2', '3'];
	var array_age_group = ['0-15', '16-30', '31-45', '46-60', '60+', 'NaN'];
	var array_sex       = ['male', 'female'];
	var result = [];
	

	for (var i = 0; i < array_class.length; i++) {

		var data_class = dimple.filterData(data, "passenger_class", [array_class[i]]);

		for (var j = 0; j < array_age_group.length; j++) {
			
			var data_age_group = dimple.filterData(data_class, "age_group", [array_age_group[j]]);

			for (var k = 0; k < array_sex.length; k++) {
				
				var data_all  = dimple.filterData(data_age_group, "sex", [array_sex[k]]);
				var data_surv = dimple.filterData(data_all, "survived", ["1"]);
				var data_rate = (data_surv.length / data_all.length)*100;

				result.push({'passenger_class' : parseInt(array_class[i]),
						     'age_group'       : array_age_group[j], 
					         'sex'             : array_sex[k], 
					         'count'           : data_all.length,
					         'count_survived'  : data_surv.length,
					         'survival_rate'   : data_rate});

			};

		};
	};

	return result;
}


