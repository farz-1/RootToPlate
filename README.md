# SH31 main

Web app for Young Enterprise Scotland to help calculate their carbon footprint and help log data related to their rocket composter.

## Name
RootToPlate

## Description
#### Background
Young Enterprise Scotland (YE Scotland) is a charity based in Rouken Glen park. YE Scotland is aiming to become carbon neutral, and one way they are working toward this is by creating their own compost from food and other waste in order to be used for growing vegetables in their garden. This is part of their 'Root to Plate' project where they seek to track the journey of their food from the ground to their plates. The project was split into two parts and the part assigned to this group involved creating a tracker for compost, displaying graphs on the home page, and creating a ticketing system where restaurants can notify the team that they have some food waste that needs collected.

#### Features
Composter:
- Temperature input form where the user can log temperatures of the composter to ensure it is working properly.
- Output form the composter can be logged. 
- Inputs to the composter can be logged and the user can request advice. This calculates a recommended input if the proposed inputs result in an unsatisfactory carbon-nitrogen ratio for composting. It also informs the user if the most recently recorded temperature input was unsatisfactory and recommends inputs to alleviate this.
- Users can see information about recent logs.
- Once the composter has received an input, it will count down until it needs 'fed' again.

Restaurant request form:
- Restaurants can request food waste collection, specifying a deadline for collection.
- Staff can see these requests alongside restaurant contact details and mark the requests as collected.

Home page:
- Displays data in the form of graphs to show YE Scotland's progress toward carbon neutrality. These are generated based on calculations based on the data stored in the database, and changes dynamically as more data is entered through the various input forms on the web app.

Admin dashboard:
- Staff can add new input types, add users, change user passwords and add meter readings (used for graph calculations on the home page).
- Superusers can access the Django admin interface where they can see individual database entries in detail, as well as being able to create more super users.

The web app also contains various other smaller features such as links to YE Scotland social media and contact details.

The web app is mobile compatible. 
 

## Visuals
Included below is a screenshot of the homepage of the deployed website. The whole site is accessible through https://roottoplate.herokuapp.com/composter/

## Installation
All the dependencies required to be installed are provided in the requirements.txt file in the root of the folder. Instructions on how to run these have been provided below.

## Testing and Deployment

The project was tested and depoloyed using the built-in continuous integration in GitLab.

- Django tests run through Gitlab CI/CD Pipelines to test aspects of the website to see if it is functional. These can be run locally by the command:
```
python manage.py test
```
- Static analysis tests run using flake8 on the pipeline as well to prevent things like syntax errors, typos, bad formatting, incorrect styling. These can be run locally by the command:
```
flake8 [filename (optional)]
```
- Deployment takes place to Heroku using the pipeline every time a commit on any branch has passed the previous two tests.

If you would like to replicate this in a CI/CD pipeline tool of your own, the pipeline code can be found in the .gitlab-ci.yml file which can be found in the base project directory.

## Instructions to run locally
```
pip install virtualenv
virtualenv {env_name}
conda activate {env_name} 
git pull 
pip install -r requirements.txt
python manage.py makemigrations composter
python manage.py makemigrations
python manage.py migrate
python population_script.py (if you wish to populate the database)
python manage.py runserver

If you're missing pip just install it with: 
conda install pip

Replace {env_name} with a name of your choice to create and activate the virtual environment.
```

## Instructions to delete current database and re-run on Heroku
```
heroku login
heroku pg:reset DATABASE -a roottoplate
roottoplate
heroku run bash -a roottoplate
cd roottoplate
python manage.py makemigrations composter
python manage.py makemigrations
python manage.py migrate
exit
heroku run python roottoplate/manage.py makemigrations composter -a roottoplate
heroku run python roottoplate/manage.py migrate -a roottoplate
heroku run python roottoplate/manage.py population_script.py -a roottoplate
```

##Useful commands
```
conda info --envs
``` 

## Badges
On analyzing the CI/CD page , badges convey the status of two stages testing and deployment. A green tick means it has succeeded , a red cross means one or both of the stages have failed and a grey slash means that the testing and (or) deployment was cancelled.


## Support
For deployment and heroku related issues , Farzwan can be contacted at 2553017M@student.gla.ac.uk and for issues relating to minor changes such as fields or adding features Abi can be contacted at 2560822H@student.gla.ac.uk

## Roadmap
The current implementation of the website is to be our final one but changes and modifications can be implemented along with new features if the customer requires so.

## Contributing
Since the ownership has been transferred to the the customer, any contributions would have to be contracted through them to us. The acceptance of this contract is highly dependant on the availability of our developers. 

## Authors and acknowledgment
Authors:
Abi Hossell
Andrew Wyllie
Daniel Tudose
Farzwan Mohamed
Sandy Millar
Siqi Wu

Special thanks to the team at YE Scotland, specifically Lynn Kelly, Lucy McOuat and Lucia Nimmo. 

Special thanks to our coach Rishabh Mathur.

## License
The project is licensed under the Eclipse Public License 2.0. This license is a commercially friendly open source license that allows YE Scotland to edit, modify, distribute and create derivatives of this software. The intellectual property of this project belongs to YE Scotland. 

## Project status
As the project currently exists, it has sufficiently fulfilled all our the customers initial needs and requirements. The customer is free to build further on this project and contract us or look elsewhere as the code is made available to them.
