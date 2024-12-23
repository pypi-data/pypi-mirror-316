var moduleBase = ptr('{base_address}');
var targetAddress = moduleBase.add(ptr('{rec_post}'))

Interceptor.attach(targetAddress, {
    onEnter: function(args) {
        this.arg0 = args[0];
        this.arg2 = args[2];

        var size = this.arg2.toInt32();

        var data = Memory.readByteArray(this.arg0, size);
        send(hexdump(data, { offset: 0, length: size, header: false, ansi: false }));
    }
});