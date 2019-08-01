if (!window.dash_clientside) {
    window.dash_clientside = {};
}

if (!window.GRAPH_ID) {
    window.GRAPH_ID = "btc-signal";
}
const SAVE_FILE_NAME = "bpi";

function figDataToStr(fig, colDelimiter = ",", rowDelimiter = "\n") {
    if (typeof fig.data == "undefined") {
        console.warn(
            "figDataToStr: fig.data is undefined. exiting with empty string."
        );
        return "ERROR,Unable to extract data from figure";
    }

    const data = fig.data;

    // create array-of-columns from data
    let aggregated = data
        .map(elem => {
            return [elem.x, elem.y];
        })
        .reduce((a, c) => {
            return a.concat(c);
        });

    // reshape into array-of-rows
    aggregated = aggregated[0].map(function(col, i) {
        return aggregated
            .map(function(row) {
                return row[i];
            })
            .join(","); // and convert to a csv representation
    });

    // generate table header from trace names
    let lblArray = data
        .map(elem => {
            return ["timestamp"].concat(elem.name).join(colDelimiter);
        })
        .join(colDelimiter);
    aggregated.unshift(lblArray); // add table header to top of aggregated

    // convert array-of-rows to CSV string
    return aggregated.join(rowDelimiter);
}

window.dash_clientside.download = {
    csvDownload: function(
        trigger,
        fig,
        colDelimiter = ",",
        rowDelimiter = "\n"
    ) {
        if (typeof trigger == "undefined" || typeof fig.data == "undefined") {
            return false;
        }

        // extract sensor data from figure
        const dataTable = figDataToStr(fig);

        // generate file timestamp
        const d = new Date();
        const footer = "Downloaded".concat(colDelimiter, d.toISOString());

        // generate file and send through file-saver
        const file = new Blob([dataTable.concat("\n\n", footer)], {
            type: "text/csv;charset=utf-8"
        });

        console.log("downloading figure data to csv.");
        saveAs(file, SAVE_FILE_NAME + ".csv");
    },
    jsonDownload: function(trigger, fig) {
        if (typeof trigger == "undefined" || typeof fig.data == "undefined") {
            return false;
        }

        // generate formatted json blob
        const dataTable = JSON.stringify(fig.data, null, 4);

        // generate file and send through file-saver
        const file = new Blob([dataTable], {
            type: "application/json;charset=utf-8"
        });

        console.log("downloading figure data to json.");
        saveAs(file, SAVE_FILE_NAME + ".json");
    },
    loadHistorical: function(trigger, extend) {
        if (typeof trigger == "undefined") {
            return false;
        }

        let data;
        fetch("/assets/close.json")
            .then(response => response.json())
            .then(json => (data = json.bpi))
            .then(() => {
                if (typeof extend == "undefined") {
                    console.log("prepending historical data");
                    Plotly.addTraces(window.GRAPH_ID, {
                        x: Object.keys(data),
                        y: Object.values(data)
                    });
                    Plotly.restyle(
                        window.GRAPH_ID,
                        {
                            name: "BPI",
                            type: "scattergl",
                            mode: "lines+markers"
                        },
                        0
                    );
                    return true;
                }

                Plotly.prependTraces(
                    window.GRAPH_ID,
                    {x: [Object.keys(data)], y: [Object.values(data)]},
                    [0]
                );
                return true;
            });
    }
};
