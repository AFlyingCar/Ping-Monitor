<?php
 // Have to re-write Config.py in php because php is stupid

 // Small function to determine if str1 startswith str2
 // Don't ask me what it does specifically, I found it online.
 function startsWith($str,$str2){
	return $str2 === "" || strrpos($str,$str2,-strlen($str)) !== FALSE;
 }

 // Class for parsing Config files.
 // It is used for a specific syntax I use in files ending with .cfg
 class Config{
	private $filename;
	private $raw_data;
	private $options;
	private $errors;

	function Config($name){
		$this->filename=$name;
		$this->raw_data=$this->readFile();
		$returns=$this->parseData();
		$this->options=$returns[0];
		$this->errors=$returns[1];
	}

	// Opens and reads the file, returning the contents
	function readFile(){
		$f = fopen($this->filename,'r');
		return fread($f,filesize($this->filename));
	}

	// Really long and complicated method for parsing the Config file
	function parseData(){
		// See Config.py for a description on the syntax of CFG files
		$returns=array();
		$parsed = explode("\n",$this->raw_data,-1);
		//var_dump($parsed);
		$error=0;

		for($i=0;$i<sizeof($parsed);$i++){
			$line=$parsed[$i];
			//echo "<p>>> " . $line; // Debugging call. Remove when class works

			// Check if the line is empty or a comment
			if(startsWith($line,'@') || $line==""){ continue; }

			try{
				// Leaving the old code here, as an adage to php's syntax making no sense
				// Why the heck would you do delimiter,string,limit?! It makes much, much more sense to do string,delimiter,limit
				$var_val = explode('=',$line,3);//explode($line,'=',3);
				//echo var_dump($var_val) . "<p>";
				$var_val[0]=trim($var_val[0]);
				$var_val[1]=trim($var_val[1]);

				// Check if value is a string
				if(startsWith($var_val[1],'"') || startsWith($var_val[1],"'")){
					$val = substr($var_val[1],1,-1);

					if(startsWith($val,"cwd\\") || startsWith($val,"cwd//")){
						$val=getcwd() . '/' . substr($val,5,strlen($val));
					}
					$returns[$var_val[0]] = $val;

				// Check if value is an int
				}elseif(is_int($var_val[1])){
					$returns[$var_val[0]] = intval($var_val[1]);

				//Check if value is a float (or double, doesn't matter)
				}elseif(is_float($var_val[1])){
					$returns[$var_val[0]] = floatval($var_val[1]);

				// Check if value is a list/array
				}elseif(startsWith($var_val[1],"(") || startsWith($var_val[1],"[")){
					$returns[$var_val[0]] = $this->stringToList($var_val[1]);

				// Check if value is a boolean
				}elseif(is_bool($var_val[1])){
					$returns[$var_val[0]] = boolval($var_val[1]);

				// Treat the value as a string if it isn't of a recognized type
				}else{
					$returns[$var_val[0]] = $var_val[1];
				}

			// If for whatever reason an exception is thrown: catch it, add 1 to the error counter, print the error, and move on as if nothing happened
			}catch(Execption $e){
				echo "An error has occurred while parsing " . $filename . "!";
				echo $e->getMessage();
				$error+=1;
			}
		}
		return [$returns,$error];
	}

	// Method for converting strings into arrays
	// Basically recreating the parsing method above
	function stringToList($str){
		$contents = substr($str,1,-1);
		$elems=explode($contents,',');

		for($i=0;$i<sizeof($elems);$i++){
			$val=$elems[$i];

			if(is_int($val)){
				$elems[$i] = intval($val);
			}elseif(is_float($val)){
				$elems[$i] = floatval($val);
			}elseif(is_bool($val)){
				$elems[$i] = boolval($val);
			}elseif(startsWith($val,"(") || startsWith($val,"[")){
				$elems[$i] = $this->stringToList($val);
			}elseif(startsWith($val,'"') || startsWith($val,"'")){
				$s = substr($val,1,-1);
				if(startsWith($s,"cwd\\") || startsWith($s,"cwd//")){
					$s = getcwd() . '/' . substr($s,5,strlen($val));
				}
				$elems[$i] = $s;
			}
		}
		return $elems;
	}

	// Returns the value associated with varName
	function getOption($varName){
		return $this->options[$varName];
	}

	// Returns the entire set of option:value pairs
	function getAllOptions(){
		return $this->options;
	}
 }
?>
