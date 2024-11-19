// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // Code to load uploaded files list and handle other dynamic actions
    loadUploadedFiles();
});

function loadUploadedFiles() {
    fetch('/api/account/uploads')
        .then(response => response.json())
        .then(data => {
            const uploadedFilesList = document.getElementById('uploaded-files');
            uploadedFilesList.innerHTML = '';
            data.forEach(file => {
                let listItem = document.createElement('li');
                listItem.textContent = file.title;
                uploadedFilesList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error loading uploaded files:', error);
        });
}
