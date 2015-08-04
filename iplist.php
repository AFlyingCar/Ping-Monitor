<?php
  include 'Config.php';
  $cfg = new Config("/home/tyler/Desktop/dev/Ping-Monitor/pingMonitor.cfg");
  $user = $cfg->getOption("DB_USER");
  $pass = $cfg->getOption("DB_PASS");
  $host = $cfg->getOption("DB_HOST");
  $name = $cfg->getOption("DB_NAME");

  $link = mysqli_connect($host,$user,$pass);
  if(!$link){
	  die('Error when opening database:\n\t' . mysqli_error());
  }

  $success = mysqli_select_db($link,$name);
  if(!$success){
	  die('Error when opening database:\n\t' . mysqli_error());
  }

  function readIP($cFilter = -1){
	  global $link;
	  $sql_query = "SELECT * FROM IP_LIST";
	  if($cFilter >= 0){
		$sql_query = $sql_query . " WHERE CompanyID=" . $cFilter;
	  }
	  $rows = array();
	  $result = mysqli_query($link,$sql_query);
	  if(!$result){
		die('Error when querying database:<p>' . mysqli_error());
	  }
	  for($idx = 0; $idx < mysqli_num_rows($result); $idx++){
		array_push($rows,mysqli_fetch_array($result,MYSQL_NUM));
	  }
	  return $rows;
  }

  if(isset($_GET['id'])){
	$cID = $_GET['id'];
  }else{
	$cID = -1;
  }

  $result = readIP($cID);
  for($edx = 0; $edx < sizeof($result); $edx++){
	echo "<p>";
	echo "<A href=\"reader.php?ip=" . $result[$edx][2] . "\">" . $result[$edx][2] . "</A>";
  }
?>
