  <html>
  <head>
    <script type="text/javascript"
          src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>

    <script type="text/javascript">
      google.setOnLoadCallback(drawChart);

      function drawChart() {

        % for ret in results:
        var data_${ret.uuid} = google.visualization.arrayToDataTable([
          ['Timestamp', '${ret.unit}'],
          % for item in ret.data:
          ['${item[0]}', '${item[1]}'],
          % endfor
        ]);

        var options_${ret.uuid} = {
          title: '${ret.name}',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart_${ret.uuid} = new google.visualization.LineChart(document.getElementById('chart_${ret.uuid}'));

        chart_${ret.uuid}.draw(data_${ret.uuid}, options_${ret.uuid});
        % endfor
      }
    </script>
  </head>
  <body>
    % for ret in results:
    <div id="chart_${ret.uuid}" style="width: 1600px; height: 200px"></div>
    % endfor
  </body>
</html>
