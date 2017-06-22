# BCFM-Reservation
This is a Python/Django Web App that was designed for the Bell Co. Flea Market. It is a database that contains info about their spaces and buildings and lets customers reserve spaces and add thier contact info to wait lists for building contracts. The application also has admin login permissions that lets employees of the BCFM manage reservations, wait lists, and the permissions of other users. The admin site also has some reporting tools built with D3.js to show occupancy rate as well as reporting on reservation types. The application is hosted with Nginx and Gunicorn and has sercurity settings added through Let's Encrypt with SSL certificates. In the next version of this app I would like to make it more responsive for smaller screens, I would like to expand to include a full POS/Checkout feature, and expand to login through social channels and auto-create social posts for users after creating reservations.

### Technologies
This application was built with Python, Django, Gunicorn, Nginx, D3.js, and Let's Encrypt.

## Setup Project
This project is with Nginx and Gunicorn.
You can view the site at [bcfmreserve.com](http://www.bcfmreserve.com/)
