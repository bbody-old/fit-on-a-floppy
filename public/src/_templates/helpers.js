// helpers.js
function addHelpers(hb) {
    hb.registerHelper('showSize', function(str){
        var sizeKB = parseInt(str)/1024;
       return sizeKB.toFixed(2) + "kb";
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
