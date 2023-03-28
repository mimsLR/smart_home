# Home IoT

## Link to GitLab repository:
Source: [Click here for GitLab repository](https://gitlab.cs.uab.edu/CS499F2022/Team4/Home-IoT)

## Installation steps:
1. Clone the repository.
```
git clone https://gitlab.cs.uab.edu/CS499F2022/Team4/Home-IoT.git
```
2. Install 'virtualenv'.
```
pip3 install virtualenv
```
3. Navigate to app.
```
cd Home-IoT
```
4. Create and activate a virtual environment.  
Windows:
```
virtualenv venv
venv\Scripts\activate
```
Mac/Linux:
```
virtualenv venv
source ./venv/bin/activate
```
5. Install requirements (make sure this is inside the active virtual environment).
```
pip3 install -r requirements.txt
```
6. Run application (must use this command instead of 'flask run').
```
python3 app.py
```

Note: When done, use CTRL + C to quit the Flask development server and type `deactivate` to deactivate the virtual environment.

## Add packages to project
To add packages to the project, ensure that you are inside of an active virtual environment. Then, use `pip3 install` and add the package name to requirements.txt (i.e., `pip3 install flask` then add `flask` to a new line on requirements.txt).

## CS499 Team 4 Members
* [Caleb Harrison](https://gitlab.cs.uab.edu/calebh1)
* [Yasmin Ingah](https://gitlab.cs.uab.edu/yingah)
* [Logan Mims](https://gitlab.cs.uab.edu/lmims52)
* [Chase Blakey](https://gitlab.cs.uab.edu/cblakey1)
* [Connor Gallagher](https://gitlab.cs.uab.edu/connorg)
* [Tanner Lyons]()
