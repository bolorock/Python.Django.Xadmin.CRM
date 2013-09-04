(function($) {
	$("#div_id_taxes").find(".controls").append("<a id=\"cmdTax\" title=\"计税\" class=\"btn btn-primary btn-small\"><i class=\"icon-play-circle\"></i></a>")
	$("#cmdTax").click(function(){
		comput();
	});
	
	
	function comput(id){
		var price=$("#id_price").val();
		if (price=="") return;
		
		var costPrice= $("#id_costprice").val();
		if (price=="") return;
		
		var taxId=id || $("#id_computingTax").val();
		if (taxId==""){
			$("#id_taxes").val("");
			return;
		}

		$.ajax({
			url : "/crm/get_computingTax/?id="+ taxId,
			type : "Get",
			success : function(data) {
				var exp=data.replace(/A/g,price).replace(/B/g,costPrice);
				var tax=eval(exp);
				$("#id_taxes").val(Math.round(tax*100)/100); //两位小数点
			},
			error:function(err){
				alert("error");
			}
		});
	}
	
	$("#id_computingTax").change(function(){
		comput($(this).val());
	});
	
	$(document).on("change",".adminselectwidget",function(){
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