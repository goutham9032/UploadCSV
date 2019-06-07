$DOM = $(document)
$DOM.ready(function(){

   function reset_file_ip(){
		$('#ip_csv_file').val('');
		$('#upload_csv .fa-spinner').addClass('no_display');
		$('#upload_csv .glyphicon-upload').html('Upload File');
   }

   function upload_csv(){
        $('#upload_csv .glyphicon-upload').html('Uploading')
        $('#upload_csv .fa-spinner').removeClass('no_display')
        event.preventDefault();
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
			if(this.readyState === 4  && this.status == 200 && this.responseText.includes('true')){
                reset_file_ip()
                alertify.success('File uploaded successfully');
                window.location.href = '/'
			}
            else if(this.responseText.includes('false')){
                if(!$(".alertify-notifier .ajs-error").is(':visible')){
                   reset_file_ip()
                   alertify.error('File uploading failed');
                }
            } 
        }
		request.open('POST', '/upload_csv/', true);
        var formData = new FormData(document.getElementById('file_upload_form'));
        request.send(formData);
   }

   function file_upload(){
       $('#upload_csv').prop('disabled',false);
   }

   function get_search_results_data_string(data){
        var results = `<table class="table table-striped">
                          <thead>
					        <tr>
							  <th scope="col">Name</th>
							  <th scope="col">Sku</th>
							  <th scope="col">Description</th>
						    </tr>
					      </thead>
                          <tbody>`
        for (var i = 0; i < data.length; i++) {
            var string = `<tr>
						    <td>` + data[i].name + `</td>
						    <td>` + data[i].sku + `</td>
						    <td>` + data[i].description + `</td>
                         </tr>`
            results = results + string
        }
        return results + '</tbody></table>'
   }

   function search_results(){
		var query = $('#search').val()
		var filters = $("input[name='filter']:checked").map(function() {return this.value;}).get().join(',')
        if (query.length < 2){
           $('.tab_spinner').hide() 
           $('#results_div').empty()
           $('#user-data-table').show()
           return 
        }
       
        $('#user-data-table').hide()
        $('.tab_spinner').show()
        $('#results_div').hide()
		ajax = $.ajax({
				type: "GET",
				url : '/search/?q=' + query + '&filters=' + filters,
		});
		ajax.done(function(data){
             var show_res = `<p class="show_results_count">Showing search results for "`+ query +`"</p>`
             var results = show_res + '<div class="table_results">' + 
                           get_search_results_data_string(data.results) + '</div>'
             $('.tab_spinner').hide() 
             if(data.results.length == 0){
                results =  `<p class="no_results">No results found</p>`
             }
             $('#results_div').empty().append(results).show()
             if($('input[name="highlight"]').is(':checked')){
               $('.table_results').highlight(query);
             }
		}).fail(function(data){
             alert(data)
		});
   }

   function hightlight_text(){
       var query = $('#search').val()
       if($('input[name="highlight"]').is(':checked')){
           $('.table_results').highlight(query);
       }
       else{
          $(".table_results").unhighlight();
       }
   }

   function delete_data(){
	   $.confirm({
			title: 'Delete',
			content: 'Are you sure you want to delete?',
			buttons: {
			  confirm: function() {
					$.ajax({
					  type: 'GET',
					  url: '/delete_records',
					  success: function(data) {
                         if (data.success){
                            alertify.success('Successfully deleted records');
                            window.location.href = '/'
                         }
                         else{
                            alertify.errot('Records deletion failed');
                         }   
					  },
					});
			  },
			  cancel: function() {},
			},
	   });

   }

   function bindEvents() {
        $DOM.on('click', '#upload_csv', upload_csv)
            .on('click', '#delete_data', delete_data)
            .on('change', '#ip_csv_file', file_upload)
            .on('change', 'input[name="filter"]', search_results)
            .on('change', 'input[name="highlight"]', hightlight_text)
            .on("keyup", "#search", _.debounce(search_results, 500))
   }

   
   alertify.set('notifier', 'position', 'top-right');
   bindEvents();
});
