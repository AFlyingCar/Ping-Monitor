<form action="iplist.php" method="post">
	StartDate: <input type="text" name="sdate"/><p/>
	EndDate: <input type="text" name="edate"/><p/>
	<input type="submit" name="submit" />
</form>
<?php
  /*
  * iplist.php
  * Lists all ip addresses. The addresses listed can be filtered by company name.
  */

  // Get all info on how to access the database
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

  // Reads all IP addresses. If $cFilter is <= 0, then now filter is applied and all ips are listed.
  function readIP($cFilter = -1){
	  global $link;
	  $sql_query = "SELECT * FROM IP_LIST";

	  // Apply the filter if it is specified
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

  // Check for filters
  if(isset($_GET['id'])){
	$cID = $_GET['id'];
  }else{
	$cID = -1;
  }

  if(isset($_POST['sdate'])){
	$sdate = $_POST['sdate'];
  }else{
	$sdate = '';
  }

  if(isset($_POST['edate'])){
	$edate = $_POST['edate'];
  }else{
  	$edate='';
  }

  $href = '<A href="reader.php?ip=';

  // Apply filters
  $result = readIP($cID);
  for($edx = 0; $edx < sizeof($result); $edx++){
	echo "<p>";
	// Format output to link properly and apply the correct filters
	echo $href . $result[$edx][2];
	if($sdate != ''){
		echo "&sdate=" . $sdate;
	}
	if($edate != ''){
		echo "&edate=" . $edate;
	}
	echo "\">" . $result[$edx][2];
	echo "</A>";
  }
?>

