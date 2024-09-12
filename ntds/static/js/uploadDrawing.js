document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('saveDrawing').addEventListener('submit', function(event) {
        event.preventDefault();

        const url = 'create/';
        const dataURL = canvas.toDataURL('image/png');
        const blob = dataURLToBlob(dataURL);

        const formData = new FormData();
        formData.append('image', blob, 'drawing.png');
        formData.append('title', document.getElementById('title').value);
        formData.append('description', document.getElementById('description').value);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('uploadMessage');
            
            if (data.message === 'Image') {
                messageElement.textContent = 'Image uploaded!';
                messageElement.style.display = 'block';

                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            } else {
                messageElement.textContent = 'Upload failed, try again later.';
                messageElement.style.display = 'block';
            }
        })
        .catch(error => {
            const messageElement = document.getElementById('uploadMessage');
            messageElement.textContent = 'Upload failed, try again later.';
            messageElement.style.display = 'block';
            console.error('Image not uploaded:', error);
        });
    });

    function dataURLToBlob(dataURL) {
        const [header, data] = dataURL.split(',');
        const mime = header.match(/:(.*?);/)[1];
        const binary = atob(data);
        const array = [];
        for (let i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        return new Blob([new Uint8Array(array)], { type: mime });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});