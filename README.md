
# Zip Away

This Django web application provides location matching by various preferences across the 33,000 zip codes in the United States. Uses an algorithm to find the least squared differences for an input zip code in a target state then provides a list of zip code matches. Results are visualized through an interactive map

<img width="1216" alt="Screen Shot 2021-03-26 at 10 09 52 AM" src="https://user-images.githubusercontent.com/41166358/112666222-f0d18b80-8e29-11eb-9bee-dc622139fb40.png">


### Intructions for running the application

1.	Clone repository
3.	Open a terminal and navigate to ckinnen-cschippits-shashab/
4.	Run:
   ```chmod 775 install.sh run_scraping.sh``` 
4.	To run the data cleaning scripts and launch the application, type:
	```./install.sh``` 
5.	Open a web browser and navigate to http://127.0.0.1:8000/.
6.	In the zip code field, type in a starting zip code.
7.	Use the drop-down menu to choose a target state.
8.	Check any combination of boxes corresponding to preferences. At least one box must be checked.
9.	Click “Submit”
10.	Wait patiently while the results populate.
11.	Read the results and have fun interacting with the map!
12.	(optional) To run a sample of the web scraping process, type:
	```./run_scraping.sh``` 
