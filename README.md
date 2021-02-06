# Auto-Survey it's a framework which allows to create custom surveys.

## Features:
* Filters: active, expired surveys
* Searchbar
* Adding, editing, removing surveys and answers (currently only from the Admin Menu)
* Automatically generated results (a graph and a table) for expired surveys.
* Feedback messages

## Customization:
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
* From the command line, type ```python manage.py runserver```. Then launch any internet browser and go the site which will show up in the command line (by default it should be: ```127.0.0.1:8000/```).

## Technology:
* ```Python``` 3.8
* ```Django``` 3.1.2
* ```numpy``` 1.19.3
* ```matplotlib``` 3.3.3

## Screenshots:
![AS1](https://user-images.githubusercontent.com/71539614/99896800-49362800-2c94-11eb-9e04-1fbe8adec5c4.png)  
<br>  
![AS2](https://user-images.githubusercontent.com/71539614/99896801-49cebe80-2c94-11eb-8fcf-b2a8241dfe91.png)   
<br>   
![AS3](https://user-images.githubusercontent.com/71539614/99896798-4804fb00-2c94-11eb-867b-1ba7121ca7b9.png)   
<br>   
![AS4](https://user-images.githubusercontent.com/71539614/99896799-489d9180-2c94-11eb-9d25-284d0b2876e1.png)   
<br>  
