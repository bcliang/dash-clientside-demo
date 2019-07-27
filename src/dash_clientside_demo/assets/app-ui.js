if (!window.dash_clientside) {
    window.dash_clientside = {};
}
if (!window.GRAPH_ID) {
    window.GRAPH_ID = "btc-signal";
}

window.dash_clientside.ui = {
    relayout: function(extendData, updateXRange, updateFigTitle, fig) {
        if (
            typeof extendData == "undefined" ||
            typeof fig === null ||
            typeof fig.data == "undefined" ||
            fig.data.length == 0
        ) {
            return false;
        }

        let newData = extendData;
        if (newData.length > 1 && Array.isArray(newData[0])) {
            newData = newData[0];
        }
        const x1 = newData[0].x.slice(-1).toString();
        let d = new Date(
            Date.parse(x1) - updateXRange * 86400000 - 420 * 60000
        );
        const x0 =
            updateXRange === 0
                ? fig.data[0].x.slice(0, 1).toString()
                : d
                      .toISOString()
                      .slice(0, 19)
                      .replace("T", " ");

        let updatedTitle = [];
        switch (updateFigTitle) {
            case 2:
                updatedTitle.unshift(
                    "price=" + newData[0].y.slice(-1).toString()
                );
            case 1:
                updatedTitle.unshift("time=" + x1 + "Z");
            default:
                updatedTitle.unshift(fig.layout.title);
        }
        updatedTitle = updatedTitle.join(", ");

        // update only values within nested objects
        const update = {
            "xaxis.range[0]": x0, // xmin
            "xaxis.range[1]": x1, // xmax
            "title.text": updatedTitle
        };

        //console.log("relayout: ", update);
        Plotly.relayout(window.GRAPH_ID, update);

        return true;
    },
    value: function(input) {
        return input;
    },
    disable: function(trigger) {
        if (typeof trigger == "undefined") {
            return false;
        }

        return true;
    }
};
