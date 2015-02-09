# Social Media Analysis Tool

## Development Process:

#### Backend:
- Flask, headless REST api. 

#### Frontend:
- D3, ember.js

## Roles and Responsibilites:
- dj: front end, documentation
- spleensauce: front end, test automation
- pietdaniel: back end, deploys
- ali: front end, back end, CI
- isaac: \<place claim here\>

## Requirements:
- TODO

## Features:
- Queries
- Graphs
- etc

## Process:
- Send email to BFW about server requirements, ensure ssh access for deploys
- Set up twitter api key, safely!!
- Start developing
- ???
- profit

## Current Status

### Backend

- oauth 1.1 has been implemented
- this is not client side application only auth which will most likely hit rate limits
- this is per user authorization which requires server side query for security reasons
 - access_token/secret should not be sent to client side
 - client side storage of application keys is not secure
- a hack (crossdomain decorator) is used currently for testing because i dont want to set up a local nginx instance
 - this should be removed when we grab a domain/server and run with nginx
 - probably could have a better pattern here

### Frontend
- really simple boilerplate with ember/bootstrap
- if a user login the key is used server side to run a query in the the tweets route
- a lot to do here but next is setting up a sane authentication/authorization scheme client side
