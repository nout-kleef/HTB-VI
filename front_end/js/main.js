const DUMMY = true;
let SP_prices = [];
let ESX_prices = [];
let SP_trades = [];
let ESX_trades = [];
let ws;

window.onload = main();

function main() {
    console.info("page loaded");
    if (DUMMY) {
        SP_prices = dummy_SP_prices;
        ESX_prices = dummy_ESX_prices;
        SP_trades = dummy_SP_trades;
        ESX_trades = dummy_ESX_trades;
        updateGraph();
    } else {
        // TODO: live data
        startListening();
    }
}

function startListening() {
    // ws = new WebSocket('ws://');
    // ws.onopen = function () {
    //     console.log('Connected');
    // };
    // ws.onmessage = updateReceived;
}

// TYPE=PRICE|FEEDCODE=FOOBAR|BID_PRICE=10.0|BID_VOLUME=100|ASK_PRICE=11.0|ASK_VOLUME=20
// TYPE=TRADE|FEEDCODE=FOOBAR|BUY=TRUE|PRICE=22.0|VOLUME=100
function updateReceived(msg) {
    // check which list this update should go to
    comps = msg.split("|");
    if (comps[0] == "TYPE=PRICE") {
        let bid_price = Number(comps[2].split("=")[1]);
        let bid_volume = Number(comps[3].split("=")[1]);
        let ask_price = Number(comps[4].split("=")[1]);
        let ask_volume = Number(comps[5].split("=")[1]);
        let mid_market = (bid_price + ask_price) / 2;
        if (comps[1] == "FEEDCODE=SP-FUTURE") {
            SP_prices.push(mid_market);
        } else {
            ESX_prices.push(mid_market);
        }
    } else {
        let isBuy = compos[2] == "BUY=TRUE";
        let price = Number(comps[3].split("=")[1]);
        let volume = Number(comps[4].split("=")[1]);
        notify(isBuy ? "bought" : "sold", volume, comps[1].split("=")[1], price);
        if (comps[1] == "FEEDCODE=SP-FUTURE") {
            SP_trades.push(new Trade(0, isBuy, price, volume));
        } else {
            ESX_trades.push(new Trade(0, isBuy, price, volume));
        }
    }
    // redraw graph with new data
    updateGraph();
}

function notify(action, vol, instr, price) {
    let icon = "";
    if (action == "bought") {
        icon = "<span class='glyphicon glyphicon-arrow-up' style='color:lightgreen'></span> ";
    } else if (action == "sold") {
        icon = "<span class='glyphicon glyphicon-arrow-down' style='color:red'></span> ";
    }
    const msg = "<span>" + icon + "<b>" + action + "</b> " + vol + " shares of <b>" + instr + "</b> at <b>" + price + "</b></span><br>";
    const currHtml = document.getElementById("notifications").innerHTML;
    document.getElementById("notifications").innerHTML = msg + currHtml;
}

function updateGraph() {
    // TODO: convert lists to JSON
    let chart1 = Highcharts.chart('container1', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'SP over time'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'line',
            name: 'SP mid-market price',
            data: SP_prices
        }, {
            type: 'scatter',
            name: 'SP trades',
            data: SP_trades
        }
        ]
    });

    let chart2 = Highcharts.chart('container2', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'ESX over time'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'line',
            name: 'ESX mid-market price',
            data: ESX_prices
        }, {
            type: 'scatter',
            name: 'ESX trades',
            data: ESX_trades
        }
        ]
    });
}
