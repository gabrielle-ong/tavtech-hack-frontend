$( function ()
{
  $( document ).on( 'submit', '.image-form', function ( ev )
	{
		// Just for fun
		var values = {};
		$.each( $( this ).serializeArray(), function ( i, field )
		{
      		values[ field.name ] = field.value;
		} );
		console.log( values );
		
		// hide image preview, show loading state
		$(".upload").addClass('hide');
		$(".loading").removeClass('hide');

		ev.preventDefault(); 

		// model code here
		setTimeout(function() {
			cganTransform();
		}, 5000);
  });
});

function cganTransform() {
	console.log('cgan')
}