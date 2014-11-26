
//Handles the typeahead capability
var vcs = new Bloodhound({
			datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
			queryTokenizer: Bloodhound.tokenizers.whitespace,
			limit: 20,
			prefetch: {
				// url points to a json file that contains an array of vc names
				url: '/static/vc_list.json',
				// the json file contains an array of strings, but the Bloodhound suggestion engine expects JavaScript objects so this converts all of those strings
				filter: function(list) {
				return $.map(list, function(vc) { return { name: vc }; });
				}
			}
		});
	 
		// kicks off the loading/processing of `local` and `prefetch`
		vcs.initialize();
	 
		// passing in `null` for the `options` arguments will result in the default
		// options being used
		$('.typeahead').typeahead(null, {
			name: 'vcs',
			displayKey: 'name',
			// `ttAdapter` wraps the suggestion engine in an adapter that
			// is compatible with the typeahead jQuery plugin
			source: vcs.ttAdapter()
		});

		//event handler for home button.  when home button is clicked, send request to the /vc-list
		$('#home').click(function(evt) {
			evt.preventDefault();
			$("#search-form").show();
			$(".typeahead").val('');
			$("#results-list").hide();
			$("#company-details").hide();
        });

		//event handler for log-out button.  when log-out button is clicked, send request to the /log-out url
		$('#log-out').click(function(evt) {
			$.post(
				"/log-out",
				function(result) {
					// this request clears the user's session
					console.log(result);
					window.location = result;
				}
			);
		});
		//event handler for the common investments button
		$('#common-investments-button').click(function(evt){
			evt.preventDefault();
			var str = $("#search-form").serialize();
			console.log(str);
				$.get(
				"/ajax/common-investments", str,
				function(result){
					console.log(result);
					$("#results-list").show();
					$("#search-form").hide();
					$("#results-list").html(result);
					//event handler for the selecting a company in the list
					$('.company').click(function(evt){
						console.log("clicked on company");
						var company = $(this).data("company"); //company is related to the data-company
						// when i click on a company route to /ajax/company-data
						$.get(
							"/ajax/company-data",
							{company : company},
							function(result){
								$("#company-details").html(result);
								$("#company-details").show();
								console.log(result);
							}
						);
						// this is for when the iqt detail table ready for query
						// $.get(
						// "/ajax/iqt-company-detail",
						// {company : company},
						// function(result){
						//		$("#iqt-company-results").html(result);
						//		console.log(result);
						// }
						// );
						// result will be html of company info w/ jinja
						// insert result into 
						
					});
				}
			);
		});