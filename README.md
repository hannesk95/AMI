Applied Machine Intelligence Technical University Munich, Chair of Data Processing, SS20, Group 10

###########################
Group members:
###########################
- Auinger, Florian: 			florian.auinger@tum.de
- Butsch, Florian: 			florian.butsch@tum.de
- Gahr, Johannes: 			johannes.gahr@tum.de
- Gensheimer, Johannes: 		johannes.gensheimer@tum.de
- Hölzl, Florian: 				florian.hoelzl@tum.de
- Kiechle, Johannes: 			johannes.kiechle@tum.de
- Miller, Christoph: 			christoph.miller@tum.de
- Nowak, Constantin: 		constantin.nowak@tum.de

###########################
Preparing your environment
###########################

Install all required packages by running:
pip install -r requirements.txt

###########################
Running the web interface
###########################

go to folder GUI and run the web interface locally with Python 3:
python app.py

###########################
General about this repository:
###########################
- data/
	--> consists all the raw and processed data used in this project for the sectors mobility, energy and household, economy, corona, and greenhouse gas emissions.
- dataprocessing/
	--> consists all the processing scripts to turn the raw data in the data/ folder to the standardized csv files.
- database_create/
	--> reads all processed csv files from data/ and creates a database. Two scripts are placed in this folder. DataPreprocessingMilestone2.ipynb that reads all the data and creates a json and CreateFinalFeatureDatabase.ipynb only uses features that are used in the further path of the project.
- models/
	--> consists all investigated models, feature selection scripts, and further investigations. 
- deliverables/
	--> consists all submission documents for all four Milestones with the status at the submission date.
- GUI/
	--> consists all scripts of the web interface and the used models. Only feature_database.json is placed in the data/ folder and not in the GUI folder. 

###########################
Acknowledgement
###########################
If there are any questions or comments please contact one of the group members mentioned above. 

###########################
Resources for the web interface
###########################

* [Dash](https://dash.plot.ly/)
* Inspired by [Tableau template](https://www.tableau.com/solutions/workbook/improve-patient-satisfaction-improving-cycle-time).
