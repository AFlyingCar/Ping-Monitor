<?php
  /*
  * CompanyList.php
  * Lists all of the companies in the database, and links to a list of all IP addresses associated with that company.
  */

  // Get all info on how to access the database
  include 'Config.php';
  // $cfg = new Config("/home/tyler/Desktop/dev/Ping-Monitor/pingMonitor.cfg");
  $cfg = new Config("/var/www/pingMonitor.cfg");
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

  // Exactly what the name implies
  function readCompanyList(){
	global $link;
	$sql_query = "SELECT * FROM CompanyList";
	$rows = array();
	$result = mysqli_query($link,$sql_query);
	if(!$result){
		die('Error when querying database:<p>' . mysqli_error());
	}

   	// Because mysqli_blah functions are really stupid in how they return data,
  	// We need to place all of it manually into an indexed array (index:value, not key:value!)
	for($idx = 0; $idx < mysqli_num_rows($result); $idx++){
		array_push($rows,mysqli_fetch_array($result,MYSQL_NUM));
	}
	return $rows;
  }

  // Now that that is all done, read the comapnies...
  $result = readCompanyList();

  // And print them out
  for($edx = 0; $edx < sizeof($result);$edx++){
	  echo "<p>";
	  $cName = $result[$edx][1];
	  // Format the output so that it links to iplist.php with the appropriate CompanyID
	  echo "<A href=\"iplist.php?id=" . $result[$edx][0] . "\">" . $cName . "</A>";
  }
?>

