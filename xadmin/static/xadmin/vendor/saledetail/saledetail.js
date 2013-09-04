(function($) {
	$("#saledetail_set-group").on("change",".adminselectwidget",function(){
		var productId=$(this).val();
		if (productId=="") return;
		var strId=$(this).attr("id");
		var prex=strId.substring(0,strId.lastIndexOf('-')+1);
		$.ajax({
			url : "/crm/getProduct/?product_id="+ productId,
			type : "Get",
			success : function(data) {
				var json=eval('(' + data + ')'); 
				var fields=json.fields;
				$("#"+prex+"price").val(fields.price);
				$("#"+prex+"costprice").val(fields.costprice);
				$("#"+prex+"discountRate1").val(fields.discountRatel);
				$("#"+prex+"otherFee").val(fields.otherFee);
				$("#"+prex+"taxes").val(fields.taxes);
			},
			error:function(err){
				alert("error");
			}
		});
	});
})(jQuery);