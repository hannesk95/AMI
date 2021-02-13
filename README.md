# Investigating the impact of COVID-19 on the climate change

---

### Preface

In the context of a university lecture called "Applied Machine Intelligence" at Technical University Munich (TUM), chair of data processing, we have been investigating the impact of COVID-19 on the climate change in the summer term 2020. In order to draw inference on collected data, various machine learning approaches were used. 

---

### Group members:

- Auinger, Florian: 			florian.auinger@tum.de
- Butsch, Florian: 			florian.butsch@tum.de
- Gahr, Johannes: 			johannes.gahr@tum.de
- Gensheimer, Johannes: 		johannes.gensheimer@tum.de
- Hölzl, Florian: 			florian.hoelzl@tum.de
- Kiechle, Johannes: 			johannes.kiechle@tum.de
- Miller, Christoph: 			christoph.miller@tum.de
- Nowak, Constantin: 			constantin.nowak@tum.de

---

### Prerequisits

Install all required packages: `pip install -r requirements.txt`

---

### Running the web application

Change directory to [GUI](GUI/) and run the web interface locally with Python 3: `python3 app.py`

---

### Repository structure

- [GUI](GUI/)
	- Incorporates all scripts of the web interface and the used models. Only feature_database.json is placed in the data/ folder and not in the GUI folder.
- [data](data/)
	- Incorporates all the raw and processed data used in this project for the sectors mobility, energy and household, economy, corona, and greenhouse gas emissions.
- [database_create](database_create/)
	- Reads all processed csv files from [data](data/) and creates a database. Two scripts are placed in this folder. DataPreprocessingMilestone2.ipynb that reads all the data and creates a json and CreateFinalFeatureDatabase.ipynb only uses features that are used in the further path of the project.
- [dataprocessing](dataprocessing/)
	- Incorporates all the processing scripts to turn the raw data in the [data](data/) folder to the standardized csv files
- [deliverables](deliverables/)
	- Incorporates all submission documents for all four Milestones with the status at the submission date.
- [models](models/)
	- Incorporates all investigated models, feature selection scripts, and further investigations. 

---

### Resources for the web interface

* [Dash](https://dash.plot.ly/)
* Inspired by [Tableau template](https://www.tableau.com/solutions/workbook/improve-patient-satisfaction-improving-cycle-time).

---

### Hint

After the project was completed, this repository was moved from the internal LDV GitLab to this Github repository. 
