function decodeUplink(input) {
    var data = {};
    var UP_ORDER = {1: ['ambient_temp', 1], 2: ['sky_temp', 1]};

    var warnings = [];

    var fields = input.bytes[0];

    var step;
    var i = 1;
    for (step = 1; step < 9; step++) {
        if (fields & (1 << (step-1))) {
            var v = UP_ORDER[step];
            var temp = 0;
            for (s = 1; s <= v[1]; s++) {
                temp = temp + (input.bytes[i] << (v[1] - s));
                i++;
            }

            if (v[0] == 'ambient_temp' || v[0] == 'sky_temp') {
                temp-=100;
            }

            data[v[0]] = temp;
        }
    }

    return {
        data: data,
        warnings: warnings
        };
  }