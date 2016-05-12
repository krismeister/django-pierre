CKEDITOR.plugins.add('glossary',{
    init:function(editor){
        var cmd = editor.addCommand('glossary', {exec:glossary_onclick})
        cmd.canUndo=false
        editor.ui.addButton('Glossary',{ label:'Mark a glossary term...', command:'glossary', icon:this.path+'images/icon.png' })
    }
})

function glossary_onclick(editor) {
    var href, selection, text, anchor, glossary_link
    if (typeof GLOSSARY_PREFIX === 'undefined') {
        href = '/glossary/';
    } else {
        href = GLOSSARY_PREFIX + '/glossary/';
    }
    selection = editor.getSelection();
    text = String(selection.getNative());
    anchor = "#" + text.toLowerCase().replace(" ", "-")
    glossary_link = $("<a>").attr({
        'href': href + anchor,
        'class': 'glossary'
    });
    glossary_link.html(text);
    glossary_link = new CKEDITOR.dom.element(glossary_link[0]);
    selection.getNative().deleteFromDocument();
    editor.insertElement(glossary_link);
}