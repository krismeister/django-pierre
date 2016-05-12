function ImageChooser() {
    var dialog;
    var active_control = null;
    this.AdminControl = {
        dialog_options: {
                'title': "Image Selector",
                'width': 1200,
                'height': 600,
                'autoOpen': false,
                'draggable': false,
                'modal': true,                
                'position': ['center', 20],
                'resizeable': true
        },
        'init': function(opts) {        
            var self = this;
            var controls = jQuery("select").filter(function() {
                return (/imageproperty_set-\d+-image/).test(jQuery(this).attr("name"));
            });
            if (controls.length === 0) { return; }
            controls.each(function() {
                var html_id, image_id, preview, instruction, control;
                html_id = jQuery(this).attr("name") + "_control";
                image_id = self.get_image_id(this);
                if (image_id) {
                    preview = jQuery('<img src="/media_browser/preview/' + image_id + '/" width="150" height="150">');
                    jQuery(this).parent().parent().find(".original").append(preview);
                }
                instruction = (image_id) ? "Select a new image" : "Select an image";
                control = jQuery('<a href="#" id="' + html_id + '">'+ instruction + '</a>');
                control.click(self.select_image);
                jQuery(this).parent().append(control);
                jQuery(this).hide();
            });
            if (opts) {
                for (var property in opts) {
                    if (opts.hasOwnProperty(property)) {
                        this.dialog_options[property] = opts[property];
                    }
                }
            }            
            dialog = jQuery('<div id="dialog"><iframe src="/admin/media_browser/choose/" id="modalIframeId" width="100%" height="100%" marginWidth="0" marginHeight="0" frameBorder="0" scrolling="auto" title="Dialog Title">Your browser does not support iframes.</iframe></div>');
            jQuery(document.body).append(dialog);
            jQuery("#dialog").dialog(self.dialog_options);
        },
        'get_image_id': function(selector) {
            selector = jQuery(selector);
            id = selector.find("option[selected='true']").attr("value")
            return (id === "") ? false : id;
        },
        'select_image': function(evt) {
            evt.preventDefault();
            active_control = jQuery(this).parent().parent();
            dialog.dialog('open');
        },
        'update_image': function(image_id) {
            dialog.dialog('close');
            active_control.find(".original p").hide();
            var img = active_control.find(".original img");
            active_control.find(".image select option").each(function() {
                opt = jQuery(this);
                if (opt.attr("value") === image_id) { opt.attr("selected", "selected"); }
                else { opt.attr("selected", ""); }
                
            });
            if (img.length > 0) {
                img.attr("src", '/media_browser/preview/' + image_id + '/');
            }
            else {
                preview = jQuery('<img src="/media_browser/preview/' + image_id + '/" width="150" height="150">');
                active_control.find(".original").append(preview);                
            }
        }
    };
    this.List = {
        'init': function () {
            var self = this;
            jQuery(".image-detail").click(self.use_image);
        },
        'use_image': function(evt) {
            evt.preventDefault();
            link = jQuery(this);
            image_id = link.attr("id").replace("image_", "");
            window.parent.Chooser.AdminControl.update_image(image_id);
        }
    };
}
var Chooser;
jQuery(document).ready(function() {
    Chooser = new ImageChooser();
    Chooser.AdminControl.init();
});
