# spotify
link: http://spotify-env.eba-yiivtcr7.us-east-1.elasticbeanstalk.com/

## How did I connect this to Elastic Beanstalk AWS
### vscode -> github
1. get `pip`
2. create `.gitignore` file copied from online example
3. create virtual environment `$ python3 -m venv .venv` and activate `$ source .venv/bin/activate`
4. create `requirements.txt` by installing whatever packages (spotipy, flask) and then `$ pip freeze > requirements.txt`
5. commit files locally to `.git`
```
$ git add .
$ git commit -m 'my message'
```
6. create new repository and create the connection in terminal
```
$ git remote add origin https://github.com/username/repo.git
$ git branch -M main
$ git push -u origin main
```
7. log in using username and password should be a personal access token that can be generated in github account settings -> developer settings
8. now everything should be on github repository

### set up AWS and connect to git
1. create aws account
2. go to Elastic Beanstalk
3. create application 
4. create environment with python3 since this is flask application and choose sample application for now because you'll push your code after
5. now go to codepipeline, create pipeline with matching name to your application, source provide should be github (version 2), sign into github and allow just the repository that we just made, choose the main branch, skip any other steps and go all the way to the end.

### double check everything
if there are errors
1. double check packages, download in the `.venv` and update `requirements.txt`
2. double check spotify developer dashboard and update the redirect uri from local host to the elastic beanstalk url
 
