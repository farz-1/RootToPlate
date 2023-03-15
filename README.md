# SH31 main

Web app for Young Enterprise Scotland to help calculate their carbon footprint and help control their rocket composter.

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
python manage.py makemigrations composter
python manage.py makemigrations
python manage.py migrate
exit
heroku run python roottoplate/manage.py makemigrations composter -a roottoplate
heroku run python roottoplate/manage.py migrate -a roottoplate
heroku run python roottoplate/manage.py population_script.py -a roottoplate
```

##Useful commands
conda info --envs 

## Add your files

- [x] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [x] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh31/sh31-main.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [x] [Set up project integrations](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh31/sh31-main/-/settings/integrations)

## Collaborate with your team

- [x] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [x] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [x] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [x] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [x] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Using the built-in continuous integration in GitLab.

- [x] [Django tests run through Gitlab CI/CD Pipelines to test aspects of the website to see if it is functional]
- [x] [Static analysis tests run using flake8 on the pipeline as well to prevent things like syntax errors, typos, bad formatting, incorrect styling ]
- [x] [Deployment takes place to Heroku using the pipeline every time a commit on any branch has passed the previous two tests]
## Name
RootToPlate

## Description
[TO DO]Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On analyzing the CI/CD page , badges convey the status of two stages testing and deployment. A green tick means it has succeeded , a red cross means one or both of the stages have failed and a grey slash means that the testing and (or) deployment was cancelled. 

## Visuals
Included below is a screenshot of the homepage of the deployed website. The whole page is accessible through https://roottoplate.herokuapp.com/composter/


## Installation
All the dependencies required to be installed are provided in the requirements.txt file in the root of the folder. Instructions on how to run these have been provided above.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
For deployment and heroku related issues , Farzwan can be contacted at 2553017M@student.gla.ac.uk and for issues relating to minor changes such as fields or adding features Abi can be contacted at 2560822H@student.gla.ac.uk

## Roadmap
The current implementation of the website is to be our final one but changes and modifications can be implemented along with new features if the customer requires so.

## Contributing
Since the ownership has been transferred to the the customer , any contributions would have to be contracted through them to us. The acceptance of this contract is highly dependant on the availability of our developers. 

## Authors and acknowledgment
[TO DO] Show your appreciation to those who have contributed to the project.

## License
[TO DO] For open source projects, say how it is licensed.

## Project status
As the project currently exists , it has sufficiently fulfilled all our the customers initial needs and requirements. The customer is free to build further on this project and contract us or look elsewhere as the code is made available to them.
