<!DOCTYPE html>
<!-- saved from url=(0061)https://p.w3layouts.com/demos/easy_admin_panel/web/index.html -->
<html style="overflow: hidden;"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Panel de control de minicadena IoT</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<meta name="keywords" content="Easy Admin Panel Responsive web template, Bootstrap Web Templates, Flat Web Templates, Android Compatible web template, 
Smartphone Compatible web template, free webdesigns for Nokia, Samsung, LG, SonyEricsson, Motorola web design">
<script async="" src="./panelsimplificado_files/analytics.js"></script><script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
 <!-- Bootstrap Core CSS -->
<link href="./panelsimplificado_files/bootstrap.min.css" rel="stylesheet" type="text/css">
<!-- Custom CSS -->
<link href="./panelsimplificado_files/style.css" rel="stylesheet" type="text/css">
<!-- Graph CSS -->
<link href="./panelsimplificado_files/font-awesome.css" rel="stylesheet"> 
<!-- jQuery -->
<!-- lined-icons -->
<link rel="stylesheet" href="./panelsimplificado_files/icon-font.min.css" type="text/css">
<!-- //lined-icons -->
<!-- chart -->
<script src="./panelsimplificado_files/Chart.js"></script>
<!-- //chart -->
<!--animate-->
<link href="./panelsimplificado_files/animate.css" rel="stylesheet" type="text/css" media="all">
<script src="./panelsimplificado_files/wow.min.js"></script>
<script src="./panelsimplificado_files/mis_scripts.js"></script>
	<script>
		 new WOW().init();
	</script>
	
<!--//end-animate-->
<!----webfonts--->
<link href="./panelsimplificado_files/css" rel="stylesheet" type="text/css">
<!---//webfonts---> 
 <!-- Meters graphs -->
<script src="./panelsimplificado_files/jquery-1.10.2.min.js"></script>
<!-- Placed js at the end of the document so the pages load faster -->

<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.js"></script>
<!-- <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>
<script src="http://ajax.aspnetcdn.com/ajax/knockout/knockout-2.2.1.js"></script>

</head> 
   
 <body class="sticky-header left-side-collapsed" onload="initMap()">

<script async="" type="text/javascript" src="https://cdn.fancybar.net/ac/fancybar.js?zoneid=1502&amp;serve=C6ADVKE&amp;placement=w3layouts" id="_fancybar_js"></script>


    <section>
    <!-- left side start-->
		
		<!-- left side end-->
    
		<!-- main content start-->
		<div class="main-content">
			<!-- header-starts -->
			
		<!-- //header-ends -->
			<div id="page-wrapper">
				<div class="graphs">
<!---728x90--->

					<div class="col_3">
						
						<div class="col-md-3 widget widget1">
							<div class="r3_counter_box">
								<i class="fa fa-eye"></i>
								<div class="stats">
								  <div id="volumen_Div">
									<h5>{{volume}}</h5>
								  </div>
								  <div class="grow grow3">
									<p>Volumen</p>
								  </div>
								</div>
							</div>
						 </div>
						<div class="col-md-3 widget widget1">
							<div class="r3_counter_box">
								<i class="fa fa-users"></i>
								<div class="stats">
								  <div id="estado_Div">
								  	<h5>{{state}}</h5>
								  </div>
								  <div class="grow grow1">
									<p>Estado</p>
								  </div>
								</div>
							</div>
						</div>
						 <div class="col-md-3 widget">
							<div class="r3_counter_box">
								<i class="fa fa-usd"></i>
								<div class="stats">
								  <div id="canal_Div">
									  <h5>{{channel}}</h5>
								  </div>
								  <div class="grow grow2">
									<p>Canal</p>
								  </div>
								</div>
							</div>
						</div>
						<div class="clearfix"> </div>
					</div>
<!---728x90--->

			<!-- switches -->
		
		<!-- //switches -->
<!---728x90--->

		<div class="col_1">
			<div class="col-md-4 span_8">
				<div class="activity_box">
					<h3>VOLUMEN</h3>
					<div class="scrollbar" id="style-2">

						<div class="activity-row activity-row1">
							<div class="single-bottom">
								<ul>
									<li>
									<form action="/volumen" method="post">
										<input type="submit" name="vol" value="up" required="">
										<label for="brand"><span></span> Subir volumen.</label>
									</form>
									</li>
									<li>
									<form action="/volumen" method="post">
										<input type="submit" name="vol" value="down" required="">
										<label for="brand"><span></span> Bajar volumen.</label>
									</form>
									</li>
								
								</ul>
							</div>
						</div>


					</div>
					
				</div>
			</div>
			<div class="col-md-4 span_8">
				<div class="activity_box activity_box1">
					<h3>ESTADO</h3>
					<div class="scrollbar" id="style-2">
						<div class="activity-row activity-row1">
							<div class="single-bottom">
								<ul>
									<li>
									<form action="/estado" method="post">
										<input type="submit" name="est" required="">
										<label for="brand">Encender/Apagar.</label>
									</form>
									</li>
								</ul>
							</div>
						</div>
						
					</div>
				</div>
			</div>
			<div class="col-md-4 span_8">
				<div class="activity_box activity_box2">
					<h3>CANAL</h3>
					<div class="scrollbar" id="style-2">
						<div class="activity-row activity-row1">
							<div class="single-bottom">
								<ul>
									<li>
									<form action="/canal" method="post">
										<input type="submit" name="can" value="up" required="">
										<label for="brand"><span></span> Subir canal.</label>
									</form>
									</li>
									<li>
									<form action="/canal" method="post">
										<input type="submit" name="can" value="down" required="">
										<label for="brand"><span></span> Bajar canal.</label>
									</form>
									</li>
								
								</ul>
							</div>
						</div>
					</div>
				</div>
				<div class="clearfix"> </div>
			</div>
			<div class="clearfix"> </div>
			
		</div>
				</div>
			<!--body wrapper start-->
			</div>
			 <!--body wrapper end-->
		</div>
        <!--footer section start-->
			
        <!--footer section end-->

      <!-- main content end-->
   </section>

<script src="./panelsimplificado_files/jquery.nicescroll.js"></script>

<script src="./panelsimplificado_files/scripts.js"></script>

<div id="ascrail2000" class="nicescroll-rails" style="width: 5px; z-index: 1000; cursor: default; position: fixed; top: 0px; height: 100%; right: 0px; opacity: 0; background: rgb(66, 79, 99);">
	<div style="position: relative; top: 69px; float: right; width: 5px; height: 856px; border: 0px; border-radius: 10px; background-color: rgb(39, 204, 228); background-clip: padding-box;">
		
	</div>
</div>
<div id="ascrail2000-hr" class="nicescroll-rails" style="height: 5px; z-index: 1000; position: fixed; left: 0px; width: 100%; bottom: 0px; cursor: default; display: none; opacity: 0; background: rgb(66, 79, 99);">
	<div style="position: relative; top: 0px; height: 5px; width: 1297px; border: 0px; border-radius: 10px; background-color: rgb(39, 204, 228); background-clip: padding-box;">
		
	</div>
</div>

</body>

</html>
