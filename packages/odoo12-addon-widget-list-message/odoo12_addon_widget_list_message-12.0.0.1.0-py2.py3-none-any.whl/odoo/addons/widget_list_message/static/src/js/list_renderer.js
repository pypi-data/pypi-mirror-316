odoo.define('widget_list_message.ListRenderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.group_field = '';
            this.group_fields = [];
            if (typeof this.state.getContext().group_field != 'undefined'){
                this.group_field = this.state.getContext().group_field;
            }
            if (typeof this.state.getContext().group_fields != 'undefined'){
                this.group_fields = this.state.getContext().group_fields;
            }
        },
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            if (this.group_fields.length == 0){
                return $td;
            }
            if (node.attrs.name == this.group_field){
                var $div = $('<div>');
                for(var fields of this.group_fields) {
                    var $p = $('<p>');
                    for(var field of fields) {
                        if (record.data[field]._isAMomentObject){
                            $p.append(record.data[field].format('DD-MM-YYYY  h:mm:ss a'));
                        }else{
                            $p.append(record.data[field]);
                        }
                        $p.append('&nbsp;&nbsp;&nbsp;');
                    }
                    $div.append($p);
                }
                if ($($td).find('div').length > 0){
                    $($td).find('div').html($div);
                }else{
                    $td.html($div);
                }
            }
            return $td;
        },
    });
    return ListRenderer;
});
