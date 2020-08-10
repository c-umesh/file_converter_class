# File Converter

This program converts CSV file into JSON file and XML file which has parent child hierarchy.
Depth of level in hierarchy is dependent on number of columns .
Input to file are : 
    inputfile name (csv file)
    delimiter( csv file delimiter)
    skip_header_rows (top n rows which are not be considered for JSON file)
    skip_columns_rows(skips columns from left in file which are not to be considered for JSON file)
    output file name (Name of Json file which needs to be created)
Output file : JSON file will created with output file name

# Prerequisites
The project requires Python 3.6 or above to run.
Apart from the  modules which need to be imported for the project to run is mentioned in requirements.txt file.
To import the prerequisites use below command from Linux machine

```bash
pip3 install -r requirements.txt
```



# Instructions to run the program

To run the project please use following command to generate json file . Please ensure following is followed
 from fileconverter import FileConvertToJson
	
	 #execute program with context using context manager
  with FileConvertToJson("data_few_records.csv",",",1,1) as fp:
      fp.write("data_few_records1.json")
	
  #execute program regularly
	 json1 =  FileConvertToJson("data_few_records.csv",",",1,1)
	 json1.convert()
	 json1.write("data_few_records2.json")

 To run the project please use following command to generate XML file . Please ensure following is followed
  from fileconverter import FileConverterToXML
 	 #execute program with context using context manager
  with FileConverterToXML("data_few_records.csv",",",1,1) as fc_xml:
      fc_xml.write("with_data_few_records1.xml")
	
  #execute program regularly
	 xml1 =  FileConverterToXML("data_few_records.csv",",",1,1)
	 xml1.convert()
  xml1.write("data_few_records3_xml.xml")

