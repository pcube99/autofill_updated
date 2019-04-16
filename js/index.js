chrome.storage.local.get('email', function (items) {
    login(items.updateTextTo);
    chrome.storage.local.remove('updateTextTo');
});
function login(newText){
    if (typeof newText === 'string') {
        Array.from(document.querySelectorAll('textarea.comments')).forEach(el => {
            el.value = newText;
        });
    }
}