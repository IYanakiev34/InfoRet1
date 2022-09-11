# Front-end of the Info ret assingment 1

## Things done

- [x] Header for the application with navigation
- [x] Form for the user to submit authors name and sorting type
- [x] Table to display results from the query
- [x] Error handling but with alerts
- [x] Dockerfile to build the applications and copy it to nginx server
- [x] Nginx to serve the app
- [x] Enumerate the returned list
- [x] Error handling with clr validators, better lock and feel and safer

## Things to do

- [ ] Paginate the table to it's easier for the users
- [ ] In order to get all result on the backend check for pagination property if so get next
      until no more then send the the array of json objects back to the front end where we extract the properties
- [ ] Add the histogram for every paper by year : relatively easy uuse the graph functionality
- [ ] Add histogram for number of papers per publication: ASK TEACHER FOR THE PUBLICATIONS NAMES
- [ ] Add histogram for the three fields source name,publication year nad publisher for the papers citing the selected papers
      ASK TEACH FOR THIS!!! Best guess is that whe have to get selected papers and then get cited and do the stuff prob easier way
- [ ] Add input for user to select papers

### How to get all publications if author has more than 100 papers

1. Add start and num to the queries

   - Start = 0, or previous num + 1
   - Num = 100,200,etc

2. Programming logic: get results, if results length == 100 get more until length < 100
3. After result gotten display in paginated table by 20
