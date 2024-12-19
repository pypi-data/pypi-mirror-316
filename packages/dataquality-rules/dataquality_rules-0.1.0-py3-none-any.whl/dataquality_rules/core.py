from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from jinja2 import Template


class DQR:

    def __init__(self, dataframe):
        self.conf = SparkConf().setAppName("DataQualityRule_Enabler")
        self.spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        self.df = dataframe
        self.totalCount = dataframe.count()*1.0
        self.totalNumCols = len(dataframe.columns)
        self.datasetInfo = {'Total Records' : self.totalCount,'Total Columns' : self.totalNumCols}

    def check_schema(self, expected_schema):
        actual_schema = self.df.schema
        return actual_schema == expected_schema

    def check_nulls(self, columns) -> dict:
        null_counts = dict()
        # columns = self.df.columns
        for cols in columns:
            count = self.df.filter(F.col(cols).isNull()).count()
            null_counts[cols] = (count/self.totalCount)*100.0
        return null_counts

    def check_duplicates(self, listOfCols: list) -> dict:
        duplicate_count = dict()
        for cols in listOfCols:
            count = self.df.groupBy(*cols).count().filter("count > 1").count()
            key = str(cols)
            duplicate_count[key] = (count/self.totalCount)*100.0
        return duplicate_count

    def check_uniqueness(self, columns) -> dict:
        unique_count = dict()
        for column in columns:
            count = self.df.select(column).distinct().count()
            unique_count[column] = 100.0 if count==1 else (count/self.totalCount)*100.0
        return unique_count

    def check_range(self, subset: dict) -> dict:
        range_count = dict()
        for column,values in subset.items():
            min_value ,max_value= values[0],values[1]
            if min_value and max_value:
                count = self.df.filter(
                    (F.col(column) < min_value) | (F.col(column) > max_value)
                ).count()
                range_count[column] = ([min_value,max_value],(count/self.totalCount)*100.0)
                return range_count
            else:
                raise ValueError('Range Not Defined')

    def check_values_in_list(self, subset: dict) -> dict:
        list_count = dict()
        for column,values in subset.items():
            count = self.df.filter(F.col(column).isin(values)).count()
            list_count[column] = [(count/self.totalCount)*100.0,values]
        return list_count

    def generate_html_report(self, report_name: str = 'Report',
                             recordCount: int = 0,
                             null_counts: dict = None,
                             unique_count: dict = None,
                             dup_count: dict = None,
                             list_count: dict = None,
                             range_count: dict = None
                             ):

        html_template = """
        <html>
            <head>
                <title>Data Quality Report</title>
                <style>
                    h1 {
                      text-align: center;
                    }
                    body {
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); 
                        margin-bottom: 20px;
                    }
                    table, th, td {
                        border: 1px solid black;
                    }
                    th, td {
                        padding: 10px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    .two-column th, .two-column td {
                        width: 50%;
                    }
                    .three-column th, .three-column td {
                        width: 33.33%;
                    }
        
                </style>
            </head>
            <body>
                <h1>Data Quality Report</h1>
                
                <h3> Dataset Overview </h3>
                <table class="two-column">
                        <tr>
                            <th>Metric</th>
                            <th>Stats</th>
                        </tr>
                        {% for column, null_count in datasetInfo.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ null_count }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                
                
                {% if null_counts %}
                <br>
                    <table class="two-column">
                        <tr>
                            <th>Column Name</th>
                            <th>Null Percentage</th>
                        </tr>
                        {% for column, null_count in null_counts.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ null_count }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                {% endif %}
                
                <br><br>
                
                {% if unique_count %}
                    <table class="two-column">
                        <tr>
                            <th>Column Name</th>
                            <th>Uniqueness Percentage</th>
                        </tr>
                        {% for column, unique_status in unique_count.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ unique_status }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                {% endif %}
                
                <br><br>
                
                {% if dup_count %}
                    <table class="two-column">
                        <tr>
                            <th>Column Name</th>
                            <th>Duplicate Percentage</th>
                        </tr>
                        {% for column, dup_status in dup_count.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ dup_status }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                {% endif %}
                
                <br><br>
                
                {% if list_count %}
                    <table class="three-column">
                        <tr>
                            <th>Column Name</th>
                            <th>ListSet</th>
                            <th>Within List Percentage</th>
                        </tr>
                        {% for column, count in list_count.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ count[1] }}</td>
                            <td>{{ count[0] }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                {% endif %}
                
                <br><br>
                
                {% if range_count %}
                    <table class="three-column">
                        <tr>
                            <th>Column Name</th>
                            <th>Value Range</th>
                            <th>Out Of Range Percentage</th>
                        </tr>
                        {% for column, count in range_count.items() %}
                        <tr>
                            <td>{{ column }}</td>
                            <td>{{ count[0] }}</td>
                            <td>{{ count[1] }}%</td>
                        </tr>
                        {% endfor %}
                    </table>
                {% endif %}
                
            </body>
        </html>
        """

        template = Template(html_template)
        rendered_html = template.render(null_counts=null_counts, recordCount=recordCount,
                                        unique_count=unique_count, dup_count=dup_count,
                                        list_count=list_count, range_count=range_count,
                                        datasetInfo=self.datasetInfo)
        location = f'reports/{report_name}.html'

        with open(location, 'w') as file:
            file.write(rendered_html)
        print(f"HTML report saved as {report_name}")

