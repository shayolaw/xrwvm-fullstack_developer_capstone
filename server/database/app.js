var express = require('express');
var mongoose = require('mongoose');
var fs = require('fs');
var cors = require('cors');
var app = express();
var port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

var reviews_data = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
var dealerships_data = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

mongoose.connect('mongodb://mongo_db:27017/', { dbName: 'dealershipsDB' });

var Reviews = require('./review');
var Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(function () {
    Reviews.insertMany(reviews_data.reviews);
  });
  Dealerships.deleteMany({}).then(function () {
    Dealerships.insertMany(dealerships_data.dealerships);
  });
} catch (error) {
  res.status(500).json({ error: 'Error fetching documents' });
}

app.get('/', function (req, res) {
  res.send('Welcome to the Mongoose API');
});

app.get('/fetchReviews', function (req, res) {
  Reviews.find(function (err, documents) {
    if (err) {
      res.status(500).json({ error: 'Error fetching documents' });
    } else {
      res.json(documents);
    }
  });
});

app.get('/fetchReviews/dealer/:id', function (req, res) {
  Reviews.find({ dealership: req.params.id }, function (err, documents) {
    if (err) {
      res.status(500).json({ error: 'Error fetching documents' });
    } else {
      res.json(documents);
    }
  });
});

app.get('/fetchDealers', function (req, res) {
  Dealerships.find(function (err, documents) {
    if (err) {
      res.status(500).json({ error: 'Error fetching documents' });
    } else {
      res.json(documents);
    }
  });
});

app.get('/fetchDealers/:state', function (req, res) {
  Dealerships.find({ state: req.params.state }, function (err, documents) {
    if (err) {
      res.status(500).json({ error: 'Error fetching document' });
    } else {
      res.send(documents);
    }
  });
});

app.get('/fetchDealer/:id', function (req, res) {
  Dealerships.find({ id: req.params.id }, function (err, documents) {
    if (err) {
      res.status(500).json({ error: 'Error fetching document' });
    } else {
      res.send(documents);
    }
  });
});

app.post('/insert_review', express.raw({ type: '*/*' }), function (req, res) {
  var data = JSON.parse(req.body);
  Reviews.find().sort({ id: -1 }).then(function (documents) {
    var new_id = documents[0].id + 1;

    var review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year
    });

    review.save(function (err, savedReview) {
      if (err) {
        console.log(err);
        res.status(500).json({ error: 'Error inserting review' });
      } else {
        res.json(savedReview);
      }
    });
  });
});

app.listen(port, function () {
  console.log('Server is running on http://localhost:' + port);
});
