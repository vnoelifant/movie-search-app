$('#selectionChoice').change(function(){    
    var selectedval = $(this).val();    
    if(selectedval == 'general'){
      $('#searchForm').attr('placeholder','Enter title to get general details!');
    }
    
    else if(selectedval == 'similar'){
     $('#searchForm').attr('placeholder','Enter title to find similar content!');
    }

    else if(selectedval == 'movie_credits'){
      $('#searchForm').attr('placeholder','Enter name to find credits!');
     }
    
     else {
    $('#searchForm').attr('placeholder','Enter title for recommendations!');
    }    
 });
