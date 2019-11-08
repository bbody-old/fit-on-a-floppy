// helpers.js
function addHelpers(hb) {
    hb.registerHelper('showSize', function(bytes, kilobytes, kibibytes){
        var result = "";
        var sizeKilobytes = parseFloat(kilobytes).toFixed(2);
        var sizeKibibytes = parseFloat(kibibytes).toFixed(2);
        var sizeBytes = parseFloat(bytes);

        result += sizeKilobytes + "kB / ";
        result += sizeKibibytes + "KiB";
        result = "<abbr title=\"" + sizeBytes + " bytes" + "\">" + result + "</abbr>";

        return result;
    });

    hb.registerHelper('trim', function(str) {
        if (str.length > 20) {
            return str.substring(0, 17) + "...";
        }
        return str;
    });

    hb.registerHelper('rowspan', function(list) {
        return parseInt(list.length) + 2;
    });

    hb.registerHelper('times', function(iterations, content) {
        var buff = [];
        for (var i = 0; i < iterations; i++) {
            buff.push(content);
        }
        return buff.join(' ');
    });

    return hb;
}

module.exports = addHelpers;
