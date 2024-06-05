// loader files
function showLoader() {
    document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

function uploadFiles() {
    showLoader();

    const fileInput = document.getElementById('file-input');
    const files = fileInput.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    fetch('http://localhost:8000/upload', { // Update this URL if your FastAPI server is running on a different host/port
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        // Handle the response from the server
        alert("Files successfully uploaded");
        console.log(data);
        fileInput.value = ''; // Reset the file input
        fetchFiles(); // Refresh the file list
    })
    .catch(error => {
        hideLoader();
        console.error('Error uploading files:', error);
    });
}

function addFileToMenu(fileName) {
    var fileList = document.getElementById('file-list');
    var listItem = document.createElement('li');
    listItem.textContent = fileName;
    fileList.appendChild(listItem);
}

function fetchFiles() {
    fetch('http://localhost:8000/files') // Update this URL if your FastAPI server is running on a different host/port
    .then(response => response.json())
    .then(data => {
        var fileList = document.getElementById('file-list');
        fileList.innerHTML = ''; // Clear the current list
        data.files.forEach(fileName => {
            addFileToMenu(fileName);
        });
    })
    .catch(error => {
        console.error('Error fetching files:', error);
    });
}

document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Fetch the files when the page loads
window.onload = function() {
    fetchFiles();
};
