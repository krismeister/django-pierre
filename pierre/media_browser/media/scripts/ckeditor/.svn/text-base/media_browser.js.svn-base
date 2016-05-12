var ActiveMediaBrowser = null; //This global is where any currently active media browser is stored
var ActiveDialog = null; //This is were the DOM object holding any currently open media browser dialog is stored

function MediaBrowser() {
    this.Grid =  function() {
        return {
            'init': function() {
                // Insert image into CKEditor when image is clicked:
                var self = this;
                $(".use-image").click(function(evt) {
                    evt.preventDefault();
                    $.get($(this).attr("href"), {}, self.insert_image_callback);
                });
                // Add tool tips to images:
                $(".image-detail").each(function() {
                    var img = $(this);
                    img.qtip({
                        content: img.find("dl").html(),
                        show: 'mouseover',
                        hide: 'mouseout',
                    });
                });            
            },
            'insert_image_callback': function(data, status) {
                window.parent.ActiveMediaBrowser.Editor.add_image(data);
            }
        }
    }();
    this.Template = function() {
        return {
            'init': function(full_size_img_src) {
                 this.url = full_size_img_src;
                 callback = this.insert_templated_image_callback;
                var self = this;
                $("form#template").submit(function (evt) { self.submit.apply(self, [evt])});
            },
            'submit': function(evt) {
                var params;
                if (evt) evt.preventDefault();
                params = this.get_params();
                $.get(this.url, params, this.insert_templated_image_callback);
            },
            'insert_templated_image_callback': function(data, status) {
                window.parent.ActiveMediaBrowser.Editor.add_image(data);
            },
            'get_params': function() {                
                var params, action;
                var params = {
                    'display': $("#id_display").val(),
                    'show_caption': $("#id_show_caption").attr("checked") ? "yes" : "no",
                    'show_credit': $("#id_show_credit").attr("checked") ? "yes" : "no"
                }
                action = $("#id_action"); //action field may or may not exist
                if (action.length > 0) params['action'] = action.val();
                return params;
                
            }
        }
    };
    this.Resize = function() {
        var initial_image_preview, full_size_image, active_image, use_template;
        return {
            'init': function(full_size_img_src) {
                use_template = false;
                initial_image_preview = $("#image-preview").html();
                // Reset options selector to first item:
                $($("#resize select option")[0]).attr("selected", "true");         
                var self = this;
                // Observe change in crop options selector:
               var url = full_size_img_src;
               $("#crop-options").change(function() {
                    url = $(this).val()
                    if (url === 'default') { 
                        $("#image-preview").html(initial_image_preview);
                        active_image = full_size_image;
                    }
                    else $.get(url, {}, self.resize_preview_callback);
                });
                // Set full_size_image to full size image:
                $.get(full_size_img_src, {}, function(data) { 
                    active_image = data; 
                    full_size_image = $(data);
                });
                // Fix container image container height and width
                $("#image-preview").css('height', $("#image-preview").height());
                $("#image-preview").css('width', $("#image-preview").width());
                // show_template_fields control
                $("#show_template_fields").attr("checked", false).click(self.template_display)
                // Register form submission behavior:
                $("form#resize button").click(function(evt) {
                    evt.preventDefault();
                    if (use_template) {
                        var MB = new MediaBrowser()
                        var params = MB.Template().get_params();
                        $.get(url, params, function(data, status) {
                            //this will set active_image:
                            self.resize_preview_callback.apply(self, arguments);
                            // which we then insert into the editor:
                            window.parent.ActiveMediaBrowser.Editor.add_image(active_image);
                        });
                        return;
                    }
                    window.parent.MediaBrowser.Editor.add_image(active_image);
                });
            },
            'resize_preview_callback': function(data, status) {
                active_image = data;
                $("#image-preview").html(active_image);
                if ($("#image-preview img").width() > $("#image-preview").width()) {
                    $("#image-preview").css('width', $("#image-preview img").width());
                }
                if ($("#image-preview img").height() > $("#image-preview").height()) {
                    $("#image-preview").css('height', $("#image-preview img").height());
                }
            },
            'template_display': function() {
                if ($(this).attr("checked")) {
                    $("#resize fieldset").show();
                    use_template = true;
                }
                else {
                    $("#resize fieldset").hide();
                    use_template = false;
                }

            }
        }
    }();
    
    this._CK_EDITOR = null;
    
    this.Editor = function() {
        var dialog_src, dialog_id;
        return {
            dialog_options: {
                'title': "Image Manager",
                'width': 1200,
                'height': 600,
                'autoOpen': false,
                'draggable': false,
                'modal': true,                
                'position': ['center', 20],
                'resizeable': true
            },
            'init': function(src, id, opts) {
                var self = this;
                dialog_src = src;
                dialog_id = "#" + id;
                if (arguments[2]) {
                    for (var property in opts) {
                        if (opts.hasOwnProperty(property)) {
                            this.dialog_options[property] = opts[property];
                        }
                    }
                }
                // Setup JQuery UI dialog:
                $(dialog_id).dialog(self.dialog_options);
                // Register dialog handler:
                $(dialog_id).click(function(evt) {
                    evt.preventDefault();
                    self.launch_browser();
                });
                
            },
            'launch_browser': function(editor_args) {
                ActiveDialog = $(dialog_id);
                ActiveMediaBrowser._CK_EDITOR = editor_args[0]; 
                $(dialog_id + " .modalIframe").attr("src", dialog_src);
                $(dialog_id).dialog('open');
            },
            'add_image': function(tag) {
                if (!tag) return false;
                try {
                    ActiveDialog.dialog('close');
                }
                catch (e) { return; } 
                ActiveMediaBrowser._CK_EDITOR.insertHtml(tag);
            }
        }
    }();
};
