<?php
 include 'Config.php';
 //$cfg = new Config("/home/tyler/Desktop/dev/Ping-Monitor/pingMonitor.cfg");
 $cfg = new Config("/var/www/pingMonitor.cfg");

 $user = $cfg->getOption("DB_USER");
 $pass = $cfg->getOption("DB_PASS");
 $host = $cfg->getOption("DB_HOST");
 $name = $cfg->getOption("DB_NAME");

 $link=mysqli_connect($host,$user,$pass);
 if(!$link){
	die("Error when opening connection:\n\t" . mysqli_error());
 }

 $success = mysqli_select_db($link,$name);
 if(!$success){
	die('Error when opening database:\n\t' . mysqli_error());
 }

 // TODO: Add ability to filter data via parameters
 function readData($ip_filter="",$date_start_filter="",$date_end_filter=""){
	global $link;
	$sql_query='SELECT * FROM dataTable';

	// Filter stuff
	// ...

	if($ip_filter != "" || $date_start_filter != "" || $date_end_filter != ""){
		$sql_query = $sql_query . ' WHERE ';
	}

	if($ip_filter != ""){
		$sql_query = $sql_query . ' IP="' . $ip_filter . '"';
		if($date_start_filter != "" || $date_end_filter != ""){
			$sql_query = $sql_query . ' AND';
		}
	}

	if($date_start_filter != ""){
		$sql_query = $sql_query . ' datetime>="' . $date_start_filter . '"';
		if($date_end_filter != ""){
			$sql_query = $sql_query . ' AND';
		}
	}

	if($date_end_filter != ""){
		$sql_query = $sql_query . ' datetime<="' . $date_end_filter . '"';
	}

	$rows=array();
	$result =mysqli_query($link,$sql_query);
	if(!$result){
		echo('An error occurred when querying the database:<p>');
		print_r(mysqli_error_list($link));
		echo('<p>Command: ' . $sql_query);
		die('');
	}
	for($idx=0;$idx<mysqli_num_rows($result);$idx++){
		array_push($rows,mysqli_fetch_array($result,MYSQL_NUM));
	}
	return $rows;
 }

 if(isset($_GET['ip'])){
	$ip=$_GET['ip'];
 }else{
	$ip="";
 }

 if(isset($_GET['sdate'])){
	$sdate=$_GET['sdate'];
 }else{
	$sdate="";
 }

 if(isset($_GET['edate'])){
	$edate=$_GET['edate'];
 }else{
	$edate="";
 }

 // If no ip is specified, don't display anything
 if($ip!=""){
	 $result=readData($ip,$sdate,$edate);
	 for($edx=0;$edx<sizeof($result);$edx++){
		 echo "<p>";
		 for($idx=0;$idx<sizeof($result[$edx]);$idx++){
			echo $result[$edx][$idx] . "  ";
		 }
	 }
 }

?>
