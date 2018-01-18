CDLI Data Parsing Tool

    Parse module:
        The file Parse.py contains code intended to be used as a module
        for other python3 scripts.  It converts data on tablets in the
        CDLI's .atf format to the following JSON structure:

            {   idToken1 : String, idToken2 : String, idToken3 : String,
                sides : [
                    {   side : Left/Right/Obverse/Reverse,
                        content : [
                            {   subregion : none/seal/column/...,
                                regionNum : n (optional),
                                lines : [Line 1 (String), Line 2 (String), ...]
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
