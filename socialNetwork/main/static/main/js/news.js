function viewNews() {
    var newsElements = document.getElementsByClassName('news-p');

    for (var i = 0; i < newsElements.length; i++) {
        var content = newsElements[i].textContent;
        var cutContent = content.substring(0, 1000);
        var fullContent = content;

        if (content.length > 1000) {
            newsElements[i].textContent = cutContent;

            var readAll = document.createElement('a');
            readAll.textContent = 'Читать новость ...';
            readAll.href = '#';
            readAll.setAttribute('class', 'status-link');

            readAll.onclick = (function(elem, fullText) {
                return function(event) {
                    event.preventDefault();
                    elem.textContent = fullText;
                    this.style.display = 'none';
                }
            })(newsElements[i], fullContent);

            var parent = newsElements[i].parentNode;
            parent.appendChild(readAll);
        } else {
            console.log('новость короткая');
        }
    }
}

document.addEventListener('DOMContentLoaded', function(){
    viewNews()
});