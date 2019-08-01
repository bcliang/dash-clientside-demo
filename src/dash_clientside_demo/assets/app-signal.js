if (!window.dash_clientside) {
    window.dash_clientside = {};
}

if (!window.GRAPH_ID) {
    window.GRAPH_ID = "btc-signal";
}
const MAX_HISTORY_ELTS = 15;
const ORDER_SGFILT = 8;
const COEFF_SGFILT = [-21, 14, 39, 54, 59, 54, 39, 14, -21];
const NORM_SGFILT = 231;

function filterFIR(data, coeff, norm) {
    return (
        data
            .map((v, index, array) => v * coeff[index])
            .reduce((a, b) => a + b, 0) / norm
    );
}
let mean = arr => arr.reduce((a, b) => a + b) / arr.length;

window.dash_clientside.signal = {
    history: [],
    filterSignal: function(relayoutData, extendData, filterType) {
        if (
            typeof relayoutData == "undefined" ||
            typeof relayoutData["title.text"] == "undefined" ||
            typeof extendData == "undefined" ||
            filterType === 0 ||
            extendData.length == 1 ||
            extendData[1].shift() > 0
        ) {
            return false;
        }

        const rawData = extendData[0].shift();
        if (typeof rawData == "undefined") {
            return false;
        }

        const filtTraceExists =
            document.getElementById(window.GRAPH_ID).data.length > 1;
        let filtData = [];

        // update browser store
        rawData.y.forEach(elem => {
            if (
                window.dash_clientside.signal.history.unshift(elem) >
                MAX_HISTORY_ELTS
            ) {
                window.dash_clientside.signal.history.pop();
            }

            switch (filterType) {
                case 2:
                    // process FIR filter as long as there are sufficient elements in the filter buffer
                    // otherwise, fall back on case 1 (signal mean)
                    if (
                        window.dash_clientside.signal.history.length >
                        ORDER_SGFILT
                    ) {
                        filtData.push(
                            filterFIR(
                                window.dash_clientside.signal.history.slice(
                                    0,
                                    ORDER_SGFILT + 1
                                ),
                                COEFF_SGFILT,
                                NORM_SGFILT
                            )
                        );
                        break;
                    }
                case 1:
                    // return the mean
                    filtData.push(mean(window.dash_clientside.signal.history));
                    break;
                default:
                    // return data with no signal processing (note: we shouldn't get to this state)
                    filtData.push(elem);
            }
        });

        if (filtTraceExists) {
            Plotly.extendTraces(
                window.GRAPH_ID,
                {
                    x: [rawData.x],
                    y: [filtData]
                },
                [1]
            );
        } else {
            Plotly.addTraces(window.GRAPH_ID, {
                x: rawData.x,
                y: filtData,
                name: "filter",
                type: "scattergl",
                mode: "lines+markers"
            });
        }

        return true;
    }
};
