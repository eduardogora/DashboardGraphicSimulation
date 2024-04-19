import React, {useState} from 'react';
import { PieChartOutlined, BarChartOutlined, LineChartOutlined } from '@ant-design/icons';
import { Layout, Menu, theme, Button } from 'antd';
import ReactApexChart from 'react-apexcharts';
  
const { Header, Content, Footer, Sider } = Layout;

const items = [BarChartOutlined, PieChartOutlined, BarChartOutlined, BarChartOutlined, LineChartOutlined].map(
  (icon, index) => ({
    key: String(index + 1),
    icon: React.createElement(icon),
    label: `Graph ${index + 1}`,
  }),
);

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [graph, setGraph] = useState(0);
  const [show, setShow] = useState(0);

  var data = {
    graph1: {
      weekly: {
        series: [
        {
          name: 'Aproved Good',
          data: [18, 20, 15, 18, 20, 15, 18, 20,]
        },
        {
          name: 'Rejected Product',
          data: [2, 0, 5, 2, 0, 5, 2, 0,]
        }
        ],
        options: {
          chart: {
            type: 'bar',
            height: 350,
            stacked: true,
            stackType: '100%'
          },
          responsive: [{
            breakpoint: 480,
            options: {
              legend: {
                position: 'bottom',
                offsetX: -10,
                offsetY: 0
              }
            }
          }],
          xaxis: {
            categories: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8',],
          },
          fill: {
            opacity: 1
          },
          legend: {
            position: 'right',
            offsetX: 0,
            offsetY: 50
          },
          title: {
            text: 'Weekly Information Aproved vs Rejected product',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      },
      monthly: {
        series: [
        {
          name: 'Aproved Good',
          data: [10, 0,]
        },
        {
          name: 'Rejected Product',
          data: [10, 20,]
        }
        ],
        options: {
          chart: {
            type: 'bar',
            height: 350,
            stacked: true,
            stackType: '100%'
          },
          responsive: [{
            breakpoint: 480,
            options: {
              legend: {
                position: 'bottom',
                offsetX: -10,
                offsetY: 0
              }
            }
          }],
          xaxis: {
            categories: ['Month 1', 'Month 2',],
          },
          fill: {
            opacity: 1
          },
          legend: {
            position: 'right',
            offsetX: 0,
            offsetY: 50
          },
          title: {
            text: 'Monthly Information of Aproved vs Rejected product',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      }
    },
    graph2: {
      monthly1: {
        series: [44, 55, 13, 43, 22, 15],
        options: {
          chart: {
            width: 380,
            type: 'pie',
          },
          labels: ['Machine 1', 'Machine 2', 'Machine 3', 'Machine 4', 'Machine 5', 'Machine 6'],
          title: {
            text: 'Month 1',
            align: 'center',
            style: {
              fontSize: '20px'
            }
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              },
            }
          }]
        },
      },
      monthly2: {
        series: [44, 55, 13, 43, 22, 15],
        options: {
          chart: {
            width: 380,
            type: 'pie',
          },
          labels: ['Machine 1', 'Machine 2', 'Machine 3', 'Machine 4', 'Machine 5', 'Machine 6'],
          title: {
            text: 'Month 2',
            align: 'center',
            style: {
              fontSize: '20px'
            }
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              },
              title:{
                text: "Mes"
              }
            }
          }]
        },
      },
    },
    graph3: {
      weekly: {
        series: [{
          name: 'Station 1',
          data: [44, 55, 57, 56, 61, 58, 63, 60,]
        }, {
          name: 'Station 2',
          data: [76, 85, 101, 98, 87, 105, 91, 114,]
        }, {
          name: 'Station 3',
          data: [35, 41, 36, 26, 45, 48, 52, 53]
        }, {
          name: 'Station 4',
          data: [35, 41, 36, 26, 45, 48, 52, 53]
        }, {
          name: 'Station 5',
          data: [35, 41, 36, 26, 45, 48, 52, 53]
        }, {
          name: 'Station 6',
          data: [35, 41, 36, 26, 45, 48, 52, 53]
        },],
        options: {
          chart: {
            type: 'bar',
            height: 350
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
          },
          yaxis: {
            title: {
              text: 'Minutes'
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return val + " minutes"
              }
            }
          },
          title: {
            text: 'weekly Information of station occupancy',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      },
      monthly: {
        series: [{
          name: 'Station 1',
          data: [10, 20,]
        }, {
          name: 'Station 2',
          data: [10, 20,]
        }, {
          name: 'Station 3',
          data: [10, 20,]
        }, {
          name: 'Station 4',
          data: [10, 20,]
        }, {
          name: 'Station 5',
          data: [10, 20,]
        }, {
          name: 'Station 6',
          data: [10, 20,]
        },],
        options: {
          chart: {
            type: 'bar',
            height: 350
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Month 1', 'Month 2',],
          },
          yaxis: {
            title: {
              text: 'Minutes'
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return val + " minutes"
              }
            }
          },
          title: {
            text: 'Monthly Information  of station occupancy',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      },
    },
    graph4: {
      weekly: {
        series: [{
          name: 'Station 1',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        }, {
          name: 'Station 2',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        }, {
          name: 'Station 3',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        }, {
          name: 'Station 4',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        }, {
          name: 'Station 5',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        }, {
          name: 'Station 6',
          data: [80, 70, 60, 50, 50, 60, 70, 80,]
        },],
        options: {
          chart: {
            type: 'bar',
            height: 350
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
          },
          yaxis: {
            title: {
              text: '$ (thousands)'
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return val + " minutes"
              }
            }
          },
          title: {
            text: 'weekly Information of Station Downtime',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      },
      monthly: {
        series: [{
          name: 'Station 1',
          data: [12, 20,]
        }, {
          name: 'Station 2',
          data: [12, 20,]
        }, {
          name: 'Station 3',
          data: [12, 20,]
        }, {
          name: 'Station 4',
          data: [12, 20,]
        }, {
          name: 'Station 5',
          data: [12, 20,]
        }, {
          name: 'Station 6',
          data: [12, 20,]
        },],
        options: {
          chart: {
            type: 'bar',
            height: 350
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Month 1', 'Month 2',],
          },
          yaxis: {
            title: {
              text: '$ (thousands)'
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return + val + "  minutes"
              }
            }
          },
          title: {
            text: 'Monthly Information of Station Downtime',
            floating: true,
            offsetY: 0,
            align: 'center',
            style: {
              color: '#444'
            }
          },
        }
      },
    },
    graph5: {
      daily: {
        series: [{
          name: "Desktops",
          data: [10, 22, 13, 41, 22, 23, 21, 52, 13, 41, 42, 43, 61, 92, 13, 21, 22, 73, 41, 62, 93, 51, 22, 13, 31, 32, 33, 31, 
                 51, 52, 43, 21, 32, 53, 61, 52, 23, 41, 22, 23, 11, 12, 13, 21, 32, 43, 51, 62, 33, 31, 32, 13, 21, 32, 43, 11, ]
        }],
        options: {
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          title: {
            text: 'Product Production by Day',
            align: 'left'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            categories: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', 
                         '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '55', '53', '54', '55', '56',],
            title:{
              text: "Day"
            },
          },
          yaxis: {
            title: {
              text: 'Number of products'
            }
          },
        },
      },
      weekly: {
        series: [{
          name: "Products",
          data: [10, 22, 13, 41, 22, 23, 21, 52,]
        }],
        options: {
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          title: {
            text: 'Product Production by Week',
            align: 'left'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            categories: ['01', '02', '03', '04', '05', '06', '07', '08',],
            title:{
              text: "Week"
            },
          },
          yaxis: {
            title: {
              text: 'Number of products'
            }
          },
        },
      },
      monthly: {
        series: [{
          name: "Products",
          data: [10, 22,]
        }],
        options: {
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          title: {
            text: 'Product Production by Month',
            align: 'left'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            categories: ['01', '02',],
            title:{
              text: "Month"
            },
          },
          yaxis: {
            title: {
              text: 'Number of products'
            }
          },
        },
      },
    },
    
  }
  

  function changeGraph(e){
    console.log(e);
    setGraph(e.key);
  } 

  function changeShowState(e){
    console.log(e);
    setShow(e);
  }

  return (
    <Layout style={{minHeight: "100vh"}}>
      <Sider
        breakpoint="lg"
        collapsedWidth="0"
        onBreakpoint={(broken) => {
          console.log(broken);
        }}
        onCollapse={(collapsed, type) => {
          console.log(collapsed, type);
        }}
      >
        <div className="demo-logo-vertical" />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} items={items} onClick={(e) => changeGraph(e)}/>
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer, display: 'flex', alignItems: 'center', justifyContent: 'center'  }}>
          <h1 style={{ padding: 0, textAlign: "center" }}>Company dashboard</h1>
        </Header>
        <Content style={{ margin: '24px 16px 0' }}>
          <div
            style={{
              padding: 24,
              minHeight: 360,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
              height: "95%"
            }}
          >
            {graph === '1' ? 
            <div>
              {
                show === 2 
                ? <ReactApexChart options={data.graph1.weekly.options} series={data.graph1.weekly.series} type="bar" height={350} />
                : <ReactApexChart options={data.graph1.monthly.options} series={data.graph1.monthly.series} type="bar" height={350} />
              }
              
            </div> 
            : null}
            {graph === '2' 
            ? <div style={{  display: "flex", alignItems: "center", justifyContent: "center"}}>
                <ReactApexChart options={data.graph2.monthly1.options} series={data.graph2.monthly1.series} type="pie" width={380} />
                <ReactApexChart options={data.graph2.monthly2.options} series={data.graph2.monthly2.series} type="pie" width={380} />
              </div>  
            : null}
            {graph === '3' ?
            <div>
              {show === 2 
                ? <ReactApexChart options={data.graph3.weekly.options} series={data.graph3.weekly.series} type="bar" height={350} /> 
                : <ReactApexChart options={data.graph3.monthly.options} series={data.graph3.monthly.series} type="bar" height={350} /> 
              }
            </div>
            : null}
            {graph === '4' ?
            <div>
              {show === 2 
                ? <ReactApexChart options={data.graph4.weekly.options} series={data.graph4.weekly.series} type="bar" height={350} /> 
                : <ReactApexChart options={data.graph4.monthly.options} series={data.graph4.monthly.series} type="bar" height={350} /> 
              }
            </div>
            : null}
            {graph === '5' ? 
            <div>
              {show === 1 ? <ReactApexChart options={data.graph5.daily.options} series={data.graph5.daily.series} type="line" height={350} /> : null}
              {show === 2 ? <ReactApexChart options={data.graph5.weekly.options} series={data.graph5.weekly.series} type="line" height={350} /> : null}
              {show === 3 ? <ReactApexChart options={data.graph5.monthly.options} series={data.graph5.monthly.series} type="line" height={350} /> : null}
            </div>
            : null}
          </div>
        </Content>
        <Footer style={{ textAlign: 'center', background: colorBgContainer }}>
          {graph === "5" ? (
            <Button style={{margin: 10}} onClick={() => changeShowState(1)}>
              Daily
            </Button>
          ) : null}
          
          { (graph === "1" || graph === "3" || graph === "4" || graph === "5") ? (
            <Button style={{margin: 10}} onClick={() => changeShowState(2)}>
              Weekly
            </Button>
          ): null}
          
          { (graph === "1" || graph === "2" || graph === "3" || graph === "4" || graph === "5") ? (
            <Button style={{margin: 10}} onClick={() => changeShowState(3)}>
              Monthly
            </Button>
          ) : null}
          
        </Footer>
      </Layout>
    </Layout>
  );
};

export default App;