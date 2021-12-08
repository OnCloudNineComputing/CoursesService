# OH Application Courses Microservice

Team OnCloudNine

## Supported Paths
### /api/courses - [GET, POST, PUT, DELETE]
<ul>
<li>GET: returns all courses</li>
<li>POST: creates a course</li>
<ul>
<li>Send course data as JSON object</li>
<li>Fields</li>
<ul>
<li>Required: course_name, course_year, course_sem, dept, 
course_number, section, credits, course_days</li>
<li>Optional: start_time, end_time, location, enrollment</li>
</ul>
</ul>
</ul>
Example JSON:

```json
{
   "course_name": "Cloud Computing",
   "course_year": 2021,
   "course_sem": "Fall",
   "dept": "COMS",
   "course_number": "E6156",
   "section": "001",
   "credits": 3,
   "course_days": "F",
   "start_time": "1:10 PM",
   "end_time": "3:40 PM",
   "location": "501 Northwest Corner Building",
   "enrollment": 171
}

```

<ul>
<li>PUT: updates all courses that match the provided conditions</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of two blocks, titled "update_fields" and 
"where_fields"</li>
</ul>
</ul>

```json
{
"update_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
},
"where_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes all courses in database</li>
</ul>

### /api/courses/\<course_id\> - [GET, PUT, DELETE]
<ul>
<li>GET: returns the course that matches the provided course_id</li>
<ul>
<li>Course ID can be either the SQL auto-generated integer ID or a 
course_code in the format "year_sem_dept_number_section"</li>
</ul>
</ul>

```
Example course_code: 2021_Fall_COMS_E6156_001
```

<ul>
<li>PUT: updates course that matches the given ID, if it exists, with the 
information provided</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of fields to update</li>
</ul>
</ul>

```json
{
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes course that matches ID if it exists</li>
</ul>

### /api/ta - [GET, POST, PUT, DELETE]
<ul>
<li>GET: returns all TAs and associated course IDs</li>
<li>POST: creates a record for a TA and associated course ID</li>
<ul>
<li>Send TA data as JSON object</li>
<li>Fields</li>
<ul>
<li>Required: TA, uni, course_id</li>
</ul>
</ul>
</ul>
Example JSON:

```json
{
   "TA": "Srujan Esanakarra",
   "uni": "ve2170",
   "course_id": 1
}

```

<ul>
<li>PUT: updates all TA records that match the provided conditions</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of two blocks, titled "update_fields" and 
"where_fields"</li>
</ul>
</ul>

```json
{
"update_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
},
"where_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes all records of TAs and associations in database</li>
</ul>

### /api/ta/\<uni\> - [GET, PUT, DELETE]
<ul>
<li>GET: returns the records for the given TA matched by uni and associated 
course IDs</li>
<li>PUT: updates records for the given TA with the information provided</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of fields to update</li>
</ul>
</ul>

```json
{
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes records of the given TA and course associations that 
exist</li>
</ul>

### /api/professor - [GET, POST, PUT, DELETE]
<ul>
<li>GET: returns all professors and associated course IDs</li>
<li>POST: creates a record for a professor and associated course ID</li>
<ul>
<li>Send professor data as JSON object</li>
<li>Fields</li>
<ul>
<li>Required: professor, uni, course_id</li>
</ul>
</ul>
</ul>
Example JSON:

```json
{
   "TA": "Donald F Ferguson",
   "uni": "dff9",
   "course_id": 1
}

```

<ul>
<li>PUT: updates all professor records that match the provided conditions</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of two blocks, titled "update_fields" and 
"where_fields"</li>
</ul>
</ul>

```json
{
"update_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
},
"where_fields": {
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes all records of professors and associations in database</li>
</ul>

### /api/professor/\<uni\> - [GET, PUT, DELETE]
<ul>
<li>GET: returns the records for the given professor matched by uni and 
associated 
course IDs</li>
<li>PUT: updates records for the given professor with the information 
provided</li>
<ul>
<li>Send update data as JSON object</li>
<li>JSON object should consist of fields to update</li>
</ul>
</ul>

```json
{
"field1": "value",
"field2": "value",
"last_field": "value"
}
```

<ul>
<li>DELETE: deletes records of the given professor and course associations that 
exist</li>
</ul>

## Details
<ul>
<li>Users must authenticate using Google</li>
<li>Courses are checked against Vergil for accuracy</li>
<li>Course IDs must exist in the courses table before professors and TAs 
can be added</li>
</ul>