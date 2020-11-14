var express = require('express');
var router = express.Router();

var fs = require('fs');
var postgres = require('postgres');
var cstr = null;
fs.readFileSync('private/cstr.txt', 'utf8', (err, data) => {
  if (err) {
    throw (err);
  }
  cstr = data;
});


router.get('/mapData', async(req, res, next) => {
  // connect to pg
  let sql = postgres(cstr);
  
  const mapData = await sql`
    SELECT ST_AsGeoJSON(t.*) 
    FROM (
      SELECT * 
      FROM tl_2019_us_county T 
      WHERE T.statefp == '39'
    ) AS t(id, name, geom)
  `

  /*const mapData = await sql`
    SELECT ST_AsGeoJSON(t.*) 
    FROM (
      SELECT * 
      FROM tl_2019_us_county T 
      WHERE T.statefp != '02' AND T.statefp != '09' AND 
        T.statefp != '23' AND T.statefp != '33' AND 
        T.statefp != '44' AND T.statefp != '50' AND T.statefp != '11'
    ) AS t(id, name, geom)

    UNION

    SELECT ST_AsGeoJSON(t.*)
    FROM (
      SELECT * 
      FROM tl_2019_us_state T 
      WHERE T.statefp = '02' OR T.statefp = '09' OR 
        T.statefp = '23' OR T.statefp = '33' OR 
        T.statefp = '44' OR T.statefp = '50' OR T.statefp = '11'
      ) AS t(id, name, geom); 
  `*/

  res.json(mapData);  
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

module.exports = router;
