CDLI Data Parsing Tool

    Initial Data:
        The .atf file these scripts are designed to work at can be downloaded at
        https://cdli.ucla.edu/tools/cdlifiles/cdliatf_unblocked.zip

    Parse module:
        The file Parse.py contains code intended to be used as a module
        for other python3 scripts.  It converts data on tablets in the
        CDLI's .atf format to the following JSON structure:

	{   idCDLI : String, idName : String,
	    objectType : String, startsOn : int, endsOn : int,
	    sides : [
		 {   side : None, Left/Right/Obverse/Reverse/...,
		     content : [
		         {   subregion : none/seal/column/...,
		             regionNum : n (optional),
		             lines : [ { text : String, 
					 (optional) comments :  [commentLine 1, ...]		 
					 (optional) attestations : [nameId 1, nameId 2, ... ]
					} , ....
				     ]
		         }, ...
		     ]
		 }, ...
	     ]
	}

    jsonExporter.py
        This is a python3 script which uses the Parse module convert the data
        from the .atf format into JSON files, which can then be easily read into
        other projects (via json module for python projects:
        https://docs.python.org/3.5/library/json.html  ).

        By default the script exports only the id and text of each tablet,
        in the following form:
            [ {id : TabletId(String} , text : TabletText(String)} ,  ...]
        The output will be stored in the file: CDLI_text.json

        By supplying an appropriate command line argument the script will also
        export the entire above tablet structure for each tablet, stored
        in the file: CDLI_full.txt

        Usage:
            python3 jsonExporter.py [CDLI data file] [Also export full structure: y/n]

    AddAttestations.py
	Adds results from SNER to json representation of data (i.e. adds attestations field), 
	and outputs a mapping of name Ids to the text of the names.


	!!! IMPORTANT NOTE:
	Because this process needs to utalize SNER's methods for normalizing text,
	it must import classes from SNER.  This requires that SNER be added to pythons 
	path variable, and this is currently hardcoded, so in order to use this script 
	you may need to modify it to reflect the location of SNER on the current system. 
	See Line 13.

	Usage:
  python3 AddAttestations.py [ATF File] [Key File] [Prediction File] [json Output] [Names output]

	- [ATF File] should be CDLI data file used for this run of SNER
	- [Key File] is one output of SNER, target_atf.KEY
	- [Prediction File] is another output of sner, atf_prediction.RT
	- [json Output] and [Names output] are locations to save results
