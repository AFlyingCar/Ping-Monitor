<?php
 include 'Config.php';
 $cfg = new Config("/home/tyler/Desktop/dev/Ping-Monitor/pingMonitor.cfg");

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
 function readData(){
	global $link;
	$sql_query='SELECT * FROM dataTable';

	// Filter stuff
	// ...

	$rows=array();
	$result =mysqli_query($link,$sql_query);
	for($idx=0;$idx<mysqli_num_rows($result);$idx++){
		array_push($rows,mysqli_fetch_array($result,MYSQL_NUM));
	}
	//return mysqli_fetch_array($result,MYSQL_NUM);
	return $rows;
 }


 // Testing area
 $result=readData();
 for($edx=0;$edx<sizeof($result);$edx++){
	 echo "<p>";
	 for($idx=0;$idx<sizeof($result[$edx]);$idx++){
		echo $result[$edx][$idx] . "  ";
	 }
 }

?>
