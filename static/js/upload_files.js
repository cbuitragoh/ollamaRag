
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
        console.log(data);
    })
    .catch(error => {
        hideLoader();
        console.error('Error uploading files:', error);
    });
}

