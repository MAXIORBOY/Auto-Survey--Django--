# Auto-Survey is my first Django project. It's a framework which allows to create custom surveys.

## Implementation:
```Survey``` customizable options:
* name  
* description
* photo representing the survey (link)
* orientation of that photo (horizontal / portrait)
* single vote (True / False)
* end date of voting
* type of vote:
  * single-choice
  * multi-choice (up to n choices)
  * answer comparasion (beetween n randomly picked choices)
  
```Answer``` customizable options:
* name
* description
* photo representing the survey (link)
* orientation of that photo (horizontal / portrait)
* to which survey it belongs
  
## Launch:
* From the command line, type ```python manage.py runserver```. Then launch any internet browser and go the site which will show up in the command line.

## Technology:
* ```Python``` 3.8
* ```Django``` 3.1.2
* ```numpy``` 1.19.3
* ```matplotlib``` 3.3.3

## Screenshots:
(...)
