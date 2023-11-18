const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.post('/', (req, res) => {
  const location = req.body.location;
  const { temp, windspeed } = req.body;

  const rainwind = spawn('python', ['rainwind.py', location]);

  rainwind.stdout.on('data', function (data) {
    const output = JSON.parse(data.toString());
    const a = output.temp;
    const b = output.windspeed;
    const c = output.rmse_temp;
    const d = output.rmse_windspeed;

    const weather = spawn('python', ['weather.py', location, a, b, c, d]);

    weather.stdout.on('data', function (data) {
      const result1 = JSON.parse(data.toString());

      const weather2 = spawn('python', ['weather2svm.py', location, a, b, c, d]);

      weather2.stdout.on('data', function (data) {
        const result2 = JSON.parse(data.toString());
        const combinedResult = {
          result1: result1,
          result2: result2
        };
        res.json(combinedResult);
      });
    });
  });
});

app.listen(4000, () => console.log('Application listening on port 4000'));
